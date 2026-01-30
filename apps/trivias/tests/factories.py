# apps/trivias/tests/factories.py
"""
Factory Boy definitions for the Trivias app.
Includes factories for Trivia, Participation, and UserAnswer models.
"""
import factory

from apps.questions.tests.factories import ChoiceFactory, QuestionFactory
from apps.trivias.models.participation import Participation
from apps.trivias.models.trivia import Trivia
from apps.trivias.models.user_answer import UserAnswer
from apps.users.tests.factories import UserFactory


class TriviaFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating Trivia sessions.
    Expected: A Trivia instance with a randomized name.
    """

    class Meta:
        model = Trivia
        skip_postgeneration_save = True

    name = factory.Faker("sentence")


class ParticipationFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating a user's participation in a trivia.
    Expected: A link between a User and a Trivia instance.
    """

    class Meta:
        model = Participation
        skip_postgeneration_save = True

    user = factory.SubFactory(UserFactory)
    trivia = factory.SubFactory(TriviaFactory)


class UserAnswerFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating a specific answer provided by a user during a trivia.
    Expected: A UserAnswer linked to a valid participation, question,
    and one of its choices.
    """

    class Meta:
        model = UserAnswer
        skip_postgeneration_save = True

    participation = factory.SubFactory(ParticipationFactory)
    question = factory.SubFactory(QuestionFactory)

    # Ensures the chosen choice belongs to the specified question
    chosen_choice = factory.SubFactory(
        ChoiceFactory, question=factory.SelfAttribute("..question")
    )

    # Automatically determines correctness based on the choice attributes
    is_correct = factory.LazyAttribute(lambda o: o.chosen_choice.is_correct)
