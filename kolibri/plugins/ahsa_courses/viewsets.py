"""
API Viewsets for AHSA Course Blueprint models.
"""
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from kolibri.core.auth.api import KolibriAuthPermissions
from .models import Assessment
from .models import CourseBlueprint
from .models import GradeCategory
from .models import LessonPlan
from .models import Semester
from .models import Week
from .reports import NCAAComplianceReporter
from .reports import NCAASyllabusExporter
from .reports import PacingGuideExporter
from .reports import StandardsAlignmentReporter
from .serializers import AssessmentSerializer
from .serializers import CourseBlueprintListSerializer
from .serializers import CourseBlueprintSerializer
from .serializers import GradeCategorySerializer
from .serializers import LessonPlanSerializer
from .serializers import SemesterSerializer
from .serializers import WeekSerializer


class CourseBlueprintFilter(filters.FilterSet):
    """Filter for CourseBlueprint queryset."""

    grade_level = filters.NumberFilter()
    subject = filters.CharFilter()
    grade_band = filters.CharFilter()
    ncaa_core_area = filters.CharFilter()
    is_active = filters.BooleanFilter()
    is_honors = filters.BooleanFilter()
    is_ap = filters.BooleanFilter()

    class Meta:
        model = CourseBlueprint
        fields = [
            "grade_level",
            "subject",
            "grade_band",
            "ncaa_core_area",
            "is_active",
            "is_honors",
            "is_ap",
        ]


class CourseBlueprintViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CourseBlueprint model.

    Provides CRUD operations and filtering for course blueprints.
    """

    permission_classes = [KolibriAuthPermissions]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CourseBlueprintFilter

    def get_queryset(self):
        """Get all course blueprints, optionally filtered."""
        return CourseBlueprint.objects.all()

    def get_serializer_class(self):
        """Use lightweight serializer for list view, full serializer for detail."""
        if self.action == "list":
            return CourseBlueprintListSerializer
        return CourseBlueprintSerializer

    @action(detail=True, methods=["get"])
    def syllabus(self, request, pk=None):
        """
        Export course syllabus.

        Returns formatted syllabus data for NCAA submission or parent review.
        """
        course = self.get_object()
        syllabus_data = {
            "course_title": course.title,
            "course_id": course.course_id,
            "grade_level": course.grade_level,
            "subject": course.get_subject_display(),
            "credit_value": str(course.credit_value),
            "duration": course.get_duration_display(),
            "florida_standards": course.florida_standard_set,
            "ncaa_core_area": course.get_ncaa_core_area_display(),
            "total_weeks": course.total_weeks,
            "weekly_minutes": course.weekly_minutes,
            "total_instructional_minutes": course.total_instructional_minutes,
            "syllabus_text": course.syllabus,
            "pacing_guide": course.pacing_guide,
            "required_materials": course.required_materials,
            "teacher_led": course.teacher_led,
            "is_honors": course.is_honors,
            "is_ap": course.is_ap,
            "requires_lab": course.requires_lab,
        }
        return Response(syllabus_data)

    @action(detail=True, methods=["get"])
    def pacing_summary(self, request, pk=None):
        """
        Get week-by-week pacing summary.

        Useful for NCAA documentation and parent/student planning.
        """
        course = self.get_object()
        weeks = course.weeks.all().order_by("week_number")

        pacing_data = {
            "course_title": course.title,
            "total_weeks": course.total_weeks,
            "weekly_minutes": course.weekly_minutes,
            "weeks": [
                {
                    "week_number": week.week_number,
                    "title": week.title,
                    "objectives": week.objectives,
                    "standards": week.standards_alignment,
                    "estimated_minutes": week.estimated_minutes,
                    "lesson_count": week.lesson_plans.count(),
                    "assessment_count": week.assessments.count(),
                }
                for week in weeks
            ],
        }
        return Response(pacing_data)

    @action(detail=True, methods=["get"])
    def standards_alignment(self, request, pk=None):
        """
        Get complete standards alignment report.

        Shows which Florida standards are covered in which weeks.
        """
        course = self.get_object()
        report = StandardsAlignmentReporter.generate_alignment_report(course)
        return Response(report)

    @action(detail=True, methods=["get"])
    def ncaa_compliance(self, request, pk=None):
        """
        Generate NCAA compliance report.

        Returns comprehensive checklist of NCAA requirements.
        """
        course = self.get_object()
        report = NCAAComplianceReporter.generate_compliance_report(course)
        return Response(report)

    @action(detail=True, methods=["get"])
    def download_syllabus(self, request, pk=None):
        """
        Download formatted syllabus as text file.

        Returns NCAA-compliant syllabus document.
        """
        course = self.get_object()
        return NCAASyllabusExporter.export_to_http_response(course)

    @action(detail=True, methods=["get"])
    def download_pacing_guide(self, request, pk=None):
        """
        Download pacing guide as CSV file.

        Returns week-by-week breakdown with standards and assessments.
        """
        course = self.get_object()
        return PacingGuideExporter.export_to_http_response(course)


class SemesterViewSet(viewsets.ModelViewSet):
    """ViewSet for Semester model."""

    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = [KolibriAuthPermissions]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["course", "semester_number"]


class WeekViewSet(viewsets.ModelViewSet):
    """ViewSet for Week model."""

    queryset = Week.objects.all()
    serializer_class = WeekSerializer
    permission_classes = [KolibriAuthPermissions]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["course", "semester", "week_number"]


class LessonPlanViewSet(viewsets.ModelViewSet):
    """ViewSet for LessonPlan model."""

    queryset = LessonPlan.objects.all()
    serializer_class = LessonPlanSerializer
    permission_classes = [KolibriAuthPermissions]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["week"]


class AssessmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Assessment model."""

    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    permission_classes = [KolibriAuthPermissions]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["course", "week", "assessment_type", "is_proctored"]


class GradeCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for GradeCategory model."""

    queryset = GradeCategory.objects.all()
    serializer_class = GradeCategorySerializer
    permission_classes = [KolibriAuthPermissions]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["course"]
