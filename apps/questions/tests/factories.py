# apps/questions/tests/factories.py
"""
Factory Boy definitions for Question and Choice models.
Ensures consistent data generation for testing trivia logic.
"""
import factory

from apps.questions.models.choice import Choice
from apps.questions.models.question import Question


class QuestionFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating Question instances.
    Expected: A Question object with a random sentence and EASY difficulty by default.
    """

    class Meta:
        model = Question
        skip_postgeneration_save = True

    text = factory.Faker("sentence")
    difficulty = "EASY"

    @factory.post_generation
    def with_choices(self, create, extracted, **kwargs):
        """
        Post-generation hook to add choices to a question.
        Expected: If 'with_choices' is True, creates 3 incorrect and 1 correct choice.
        """
        if not create or not extracted:
            return

        # Create 3 incorrect choices
        ChoiceFactory.create_batch(3, question=self, is_correct=False)
        # Create 1 correct choice
        ChoiceFactory.create(question=self, is_correct=True)


class ChoiceFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating Choice instances linked to questions.
    Expected: A Choice object linked to a Question, marked as incorrect by default.
    """

    class Meta:
        model = Choice
        skip_postgeneration_save = True

    question = factory.SubFactory(QuestionFactory)
    text = factory.Faker("word")
    is_correct = False
