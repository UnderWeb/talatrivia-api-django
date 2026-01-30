# apps/questions/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.question_viewset import QuestionViewSet

router = DefaultRouter()
router.register(r"questions", QuestionViewSet, basename="question")

urlpatterns = [
    path("", include(router.urls)),
]
