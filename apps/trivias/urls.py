# apps/trivias/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.participation_viewset import ParticipationViewSet
from .views.ranking_view import TriviaRankingView
from .views.trivia_viewset import TriviaViewSet
from .views.user_answer_viewset import UserAnswerViewSet

router = DefaultRouter()
router.register(r"trivias", TriviaViewSet, basename="trivia")
router.register(r"participations", ParticipationViewSet, basename="participation")
router.register(r"user-answers", UserAnswerViewSet, basename="user-answer")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "trivias/<int:trivia_id>/ranking/",
        TriviaRankingView.as_view(),
        name="trivia-ranking",
    ),
]
