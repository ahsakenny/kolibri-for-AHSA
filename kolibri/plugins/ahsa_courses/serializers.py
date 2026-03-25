"""
Serializers for AHSA Course Blueprint models.
"""
from rest_framework import serializers

from .models import Assessment
from .models import CourseBlueprint
from .models import GradeCategory
from .models import LessonPlan
from .models import Semester
from .models import Week


class AssessmentSerializer(serializers.ModelSerializer):
    """Serializer for Assessment model."""

    class Meta:
        model = Assessment
        fields = [
            "id",
            "course",
            "week",
            "assessment_type",
            "title",
            "description",
            "points_possible",
            "weight",
            "estimated_minutes",
            "is_proctored",
            "proctoring_requirements",
            "rubric",
            "has_teacher_grading",
            "exam_id",
        ]


class LessonPlanSerializer(serializers.ModelSerializer):
    """Serializer for LessonPlan model."""

    class Meta:
        model = LessonPlan
        fields = [
            "id",
            "week",
            "lesson_number",
            "title",
            "description",
            "video_url",
            "video_provider",
            "reading_resource",
            "additional_resources",
            "guided_notes",
            "practice_activity",
            "estimated_minutes",
            "contentnode_id",
        ]


class WeekSerializer(serializers.ModelSerializer):
    """Serializer for Week model with nested lessons and assessments."""

    lesson_plans = LessonPlanSerializer(many=True, read_only=True)
    assessments = AssessmentSerializer(many=True, read_only=True)

    class Meta:
        model = Week
        fields = [
            "id",
            "course",
            "semester",
            "week_number",
            "title",
            "description",
            "objectives",
            "standards_alignment",
            "estimated_minutes",
            "requires_teacher_interaction",
            "teacher_interaction_notes",
            "lesson_plans",
            "assessments",
        ]


class SemesterSerializer(serializers.ModelSerializer):
    """Serializer for Semester model with nested weeks."""

    weeks = WeekSerializer(many=True, read_only=True)

    class Meta:
        model = Semester
        fields = [
            "id",
            "course",
            "semester_number",
            "title",
            "description",
            "credit_value",
            "weeks",
        ]


class GradeCategorySerializer(serializers.ModelSerializer):
    """Serializer for GradeCategory model."""

    class Meta:
        model = GradeCategory
        fields = ["id", "course", "name", "description", "weight", "drop_lowest"]


class CourseBlueprintSerializer(serializers.ModelSerializer):
    """
    Serializer for CourseBlueprint model.
    Includes nested semesters, weeks, and grade categories.
    """

    semesters = SemesterSerializer(many=True, read_only=True)
    weeks = WeekSerializer(many=True, read_only=True)
    grade_categories = GradeCategorySerializer(many=True, read_only=True)
    assessments = AssessmentSerializer(many=True, read_only=True)
    total_instructional_minutes = serializers.ReadOnlyField()

    class Meta:
        model = CourseBlueprint
        fields = [
            "id",
            "course_id",
            "title",
            "description",
            "grade_band",
            "grade_level",
            "subject",
            "florida_standard_set",
            "ncaa_core_area",
            "is_ncaa_approved",
            "duration",
            "credit_value",
            "total_weeks",
            "weekly_minutes",
            "total_instructional_minutes",
            "is_honors",
            "is_ap",
            "requires_lab",
            "syllabus",
            "pacing_guide",
            "required_materials",
            "teacher_notes",
            "teacher_led",
            "academic_integrity_policy",
            "collection",
            "created_by",
            "date_created",
            "date_modified",
            "is_active",
            "version",
            "semesters",
            "weeks",
            "grade_categories",
            "assessments",
        ]
        read_only_fields = [
            "date_created",
            "date_modified",
            "total_instructional_minutes",
        ]


class CourseBlueprintListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing course blueprints (without nested data).
    """

    total_instructional_minutes = serializers.ReadOnlyField()

    class Meta:
        model = CourseBlueprint
        fields = [
            "id",
            "course_id",
            "title",
            "description",
            "grade_band",
            "grade_level",
            "subject",
            "ncaa_core_area",
            "is_ncaa_approved",
            "duration",
            "credit_value",
            "total_weeks",
            "total_instructional_minutes",
            "is_honors",
            "is_ap",
            "is_active",
            "date_created",
            "date_modified",
        ]
