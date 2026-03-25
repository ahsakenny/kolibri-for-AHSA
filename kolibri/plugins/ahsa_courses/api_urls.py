"""
API URLs for AHSA Courses Plugin.
"""
from django.urls import include
from django.urls import path
from rest_framework import routers

from .viewsets import AssessmentViewSet
from .viewsets import CourseBlueprintViewSet
from .viewsets import GradeCategoryViewSet
from .viewsets import LessonPlanViewSet
from .viewsets import SemesterViewSet
from .viewsets import WeekViewSet

router = routers.DefaultRouter()
router.register(r"courseblueprint", CourseBlueprintViewSet, basename="courseblueprint")
router.register(r"semester", SemesterViewSet, basename="semester")
router.register(r"week", WeekViewSet, basename="week")
router.register(r"lessonplan", LessonPlanViewSet, basename="lessonplan")
router.register(r"assessment", AssessmentViewSet, basename="assessment")
router.register(r"gradecategory", GradeCategoryViewSet, basename="gradecategory")

urlpatterns = [
    path("", include(router.urls)),
]
