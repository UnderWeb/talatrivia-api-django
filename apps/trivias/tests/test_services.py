# apps/trivias/tests/test_services.py
import pytest
from django.core.exceptions import ValidationError

from apps.questions.enums.difficulty_level import DifficultyLevel
from apps.questions.tests.factories import ChoiceFactory, QuestionFactory
from apps.trivias.models.trivia_question import TriviaQuestion
from apps.trivias.models.user_answer import UserAnswer
from apps.trivias.services.participation_service import ParticipationService


@pytest.mark.django_db
class TestParticipationService:
    """Tests for ParticipationService logic."""

    def test_submit_answer_success(self, participation):
        """
        Test that the service correctly validates and saves a new UserAnswer instance.
        Expected: is_valid() returns True and the saved instance matches the input data.
        """
        service = ParticipationService()
        question = QuestionFactory(difficulty=DifficultyLevel.HARD)

        TriviaQuestion.objects.create(
            trivia=participation.trivia, question=question, order=1
        )

        choice = ChoiceFactory(question=question, is_correct=True)

        user_answer = service.submit_answer(
            participation=participation, question=question, chosen_choice=choice
        )

        assert isinstance(user_answer, UserAnswer)
        assert user_answer.is_correct is True
        assert participation.total_score == 3

    def test_submit_answer_invalid_question(self, participation):
        """
        Test that the service prevents answering a question not belonging
        to the trivia.
        Expected: Raises ValidationError with "Question does not belong
        to this trivia.".
        """
        service = ParticipationService()
        question = QuestionFactory()
        choice = ChoiceFactory(question=question)

        with pytest.raises(ValidationError) as exc:
            service.submit_answer(participation, question, choice)

        assert "Question does not belong to this trivia" in str(exc.value)

    def test_submit_answer_invalid_choice(self, participation):
        """
        Test that the service prevents using a choice that doesn't belong
        to the question.
        Expected: Raises ValidationError with "Invalid choice for this question.".
        """
        service = ParticipationService()
        question = QuestionFactory()
        TriviaQuestion.objects.create(
            trivia=participation.trivia, question=question, order=1
        )

        other_choice = ChoiceFactory()

        with pytest.raises(ValidationError) as exc:
            service.submit_answer(participation, question, other_choice)

        assert "Invalid choice for this question" in str(exc.value)

    def test_submit_answer_already_answered(self, participation):
        """
        Test that the service prevents answering the same question twice.
        Expected: Raises ValidationError with "Question already answered.".
        """
        service = ParticipationService()
        question = QuestionFactory()
        TriviaQuestion.objects.create(
            trivia=participation.trivia, question=question, order=1
        )
        choice = ChoiceFactory(question=question)

        service.submit_answer(participation, question, choice)

        with pytest.raises(ValidationError) as exc:
            service.submit_answer(participation, question, choice)

        assert "Question already answered" in str(exc.value)

    def test_finish_participation_sets_end_time(self, participation):
        """
        Test that finishing a participation records the end time correctly.
        Expected: end_time is not None and the participation is marked as finished.
        """
        service = ParticipationService()

        assert participation.end_time is None

        finished_p = service.finish_participation(participation)

        assert finished_p.end_time is not None
        assert finished_p.is_finished is True
