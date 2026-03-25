"""
AHSA Course Blueprint Models
============================

Models for structured course blueprints aligned with Florida standards
and designed to support NCAA course approval workflows.
"""
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models

from kolibri.core.auth.models import AbstractFacilityDataModel
from kolibri.core.auth.models import Collection
from kolibri.core.auth.models import FacilityUser
from kolibri.core.auth.permissions.base import RoleBasedPermissions
from kolibri.core.fields import DateTimeTzField
from kolibri.core.fields import JSONField
from kolibri.utils.time_utils import local_now


# Grade band choices
GRADE_BAND_CHOICES = [
    ("middle", "Middle School (6-8)"),
    ("high", "High School (9-12)"),
]

# Subject choices
SUBJECT_CHOICES = [
    ("ela", "English Language Arts"),
    ("math", "Mathematics"),
    ("science", "Science"),
    ("social_studies", "Social Studies"),
    ("world_language", "World Language"),
    ("elective", "Elective"),
]

# NCAA core area choices
NCAA_CORE_AREA_CHOICES = [
    ("english", "English"),
    ("mathematics", "Mathematics"),
    ("natural_science", "Natural/Physical Science"),
    ("social_science", "Social Science"),
    ("additional", "Additional Core"),
    ("none", "Not NCAA Core"),
]

# Course duration choices
DURATION_CHOICES = [
    ("full_year", "Full Year (36 weeks)"),
    ("semester", "Semester (18 weeks)"),
    ("quarter", "Quarter (9 weeks)"),
]


class CourseBlueprint(AbstractFacilityDataModel):
    """
    A course blueprint defines the structure and metadata for a complete course.

    Courses are designed to be:
    - Florida standards-aligned
    - NCAA approval-ready (with appropriate metadata)
    - Structured for online/hybrid learning
    - Paced for consistent instructional minutes
    """

    permissions = RoleBasedPermissions(
        target_field="collection",
        can_be_created_by=("admin", "coach"),
        can_be_read_by=("admin", "coach", "learner"),
        can_be_updated_by=("admin", "coach"),
        can_be_deleted_by=("admin",),
    )

    # Basic course information
    course_id = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique identifier for the course (e.g., 'ahsa_alg1')",
    )
    title = models.CharField(max_length=200, help_text="Course title")
    description = models.TextField(
        blank=True, help_text="Detailed course description"
    )
    grade_band = models.CharField(
        max_length=20, choices=GRADE_BAND_CHOICES, help_text="Grade level band"
    )
    grade_level = models.IntegerField(
        validators=[MinValueValidator(6), MaxValueValidator(12)],
        help_text="Specific grade level (6-12)",
    )
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)

    # Standards and compliance
    florida_standard_set = models.CharField(
        max_length=100,
        blank=True,
        help_text="Florida state standards reference (e.g., 'NGSSS-MA.912')",
    )
    ncaa_core_area = models.CharField(
        max_length=50,
        choices=NCAA_CORE_AREA_CHOICES,
        default="none",
        help_text="NCAA core academic area classification",
    )
    is_ncaa_approved = models.BooleanField(
        default=False,
        help_text="Whether this course has been submitted for NCAA approval",
    )

    # Course structure
    duration = models.CharField(
        max_length=20,
        choices=DURATION_CHOICES,
        default="full_year",
        help_text="Course duration",
    )
    credit_value = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=1.00,
        help_text="Credit value (e.g., 1.0 for full year, 0.5 for semester)",
    )
    total_weeks = models.IntegerField(
        default=36, help_text="Total weeks in the course"
    )
    weekly_minutes = models.IntegerField(
        default=225,  # 45 min/day x 5 days/week
        help_text="Expected instructional minutes per week",
    )

    # Academic rigor and categorization
    is_honors = models.BooleanField(
        default=False, help_text="Whether this is an honors-level course"
    )
    is_ap = models.BooleanField(
        default=False, help_text="Whether this is an AP course"
    )
    requires_lab = models.BooleanField(
        default=False,
        help_text="Whether course requires lab work (for science courses)",
    )

    # Course materials and resources
    syllabus = models.TextField(blank=True, help_text="Complete course syllabus")
    pacing_guide = models.TextField(blank=True, help_text="Week-by-week pacing guide")
    required_materials = JSONField(
        default=list,
        blank=True,
        help_text="List of required materials/resources (textbooks, software, etc.)",
    )
    teacher_notes = models.TextField(
        blank=True, help_text="Notes for instructors teaching this course"
    )

    # NCAA/Compliance metadata
    teacher_led = models.BooleanField(
        default=True,
        help_text="Whether course requires active teacher oversight (for NCAA)",
    )
    academic_integrity_policy = models.TextField(
        blank=True, help_text="Academic integrity and proctoring requirements"
    )

    # Linking to Kolibri's existing system
    collection = models.ForeignKey(
        Collection,
        related_name="course_blueprints",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Optional link to a Kolibri classroom/collection",
    )

    # Metadata
    created_by = models.ForeignKey(
        FacilityUser,
        related_name="course_blueprints_created",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    date_created = DateTimeTzField(default=local_now, editable=False)
    date_modified = DateTimeTzField(default=local_now)
    is_active = models.BooleanField(
        default=True, help_text="Whether this course is currently offered"
    )

    # Version tracking for blueprint updates
    version = models.CharField(
        max_length=20, default="1.0", help_text="Blueprint version"
    )

    morango_model_name = "courseblueprint"

    class Meta:
        verbose_name = "Course Blueprint"
        verbose_name_plural = "Course Blueprints"
        ordering = ["grade_level", "subject", "title"]

    def __str__(self):
        return f"{self.title} (Grade {self.grade_level})"

    def save(self, *args, **kwargs):
        # Update modification timestamp
        self.date_modified = local_now()
        super().save(*args, **kwargs)

    @property
    def total_instructional_minutes(self):
        """Calculate total instructional minutes for the course."""
        return self.total_weeks * self.weekly_minutes


class Semester(models.Model):
    """
    A semester within a course (for full-year courses divided into semesters).
    """

    course = models.ForeignKey(
        CourseBlueprint, related_name="semesters", on_delete=models.CASCADE
    )
    semester_number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2)],
        help_text="Semester number (1 or 2)",
    )
    title = models.CharField(max_length=200, help_text="Semester title")
    description = models.TextField(blank=True)
    credit_value = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.50,
        help_text="Credit value for this semester",
    )
    weeks = models.IntegerField(default=18, help_text="Number of weeks in semester")

    class Meta:
        verbose_name = "Semester"
        verbose_name_plural = "Semesters"
        unique_together = ("course", "semester_number")
        ordering = ["course", "semester_number"]

    def __str__(self):
        return f"{self.course.title} - Semester {self.semester_number}"


class Week(models.Model):
    """
    A weekly unit within a course or semester.
    Represents one week of instruction with specific objectives and activities.
    """

    course = models.ForeignKey(
        CourseBlueprint, related_name="weeks", on_delete=models.CASCADE
    )
    semester = models.ForeignKey(
        Semester,
        related_name="weeks",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text="Optional semester grouping",
    )

    week_number = models.IntegerField(
        validators=[MinValueValidator(1)], help_text="Week number in course sequence"
    )
    title = models.CharField(max_length=200, help_text="Week title/topic")
    description = models.TextField(blank=True, help_text="Week overview")

    # Learning objectives
    objectives = JSONField(
        default=list,
        blank=True,
        help_text="List of learning objectives for this week",
    )

    # Standards alignment
    standards_alignment = JSONField(
        default=list,
        blank=True,
        help_text="List of Florida standards covered this week",
    )

    # Time allocation
    estimated_minutes = models.IntegerField(
        default=225,  # 45 min/day x 5 days
        help_text="Estimated instructional minutes for this week",
    )

    # Teacher interaction requirements (for NCAA compliance)
    requires_teacher_interaction = models.BooleanField(
        default=True, help_text="Whether this week requires teacher touchpoints"
    )
    teacher_interaction_notes = models.TextField(
        blank=True, help_text="Description of required teacher interactions"
    )

    class Meta:
        verbose_name = "Week"
        verbose_name_plural = "Weeks"
        unique_together = ("course", "week_number")
        ordering = ["course", "week_number"]

    def __str__(self):
        return f"{self.course.course_id} - Week {self.week_number}: {self.title}"


class LessonPlan(models.Model):
    """
    A lesson plan within a weekly unit.
    Represents a single lesson with specific content and activities.
    """

    week = models.ForeignKey(
        Week, related_name="lesson_plans", on_delete=models.CASCADE
    )
    lesson_number = models.IntegerField(
        validators=[MinValueValidator(1)], help_text="Lesson number within the week"
    )
    title = models.CharField(max_length=200, help_text="Lesson title")
    description = models.TextField(blank=True, help_text="Lesson description")

    # Content resources (placeholders for OER content)
    video_url = models.URLField(
        blank=True,
        help_text="URL to video content (Khan Academy, YouTube, etc.) - placeholder",
    )
    video_provider = models.CharField(
        max_length=50, blank=True, help_text="Video provider (e.g., 'Khan Academy')"
    )
    reading_resource = JSONField(
        default=dict,
        blank=True,
        help_text="Reading resource metadata (title, source, URL, type)",
    )
    additional_resources = JSONField(
        default=list, blank=True, help_text="Additional learning resources"
    )

    # Instructional content
    guided_notes = models.TextField(
        blank=True, help_text="Guided notes or outline for students"
    )
    practice_activity = models.TextField(
        blank=True, help_text="Practice activity description"
    )

    # Time estimate
    estimated_minutes = models.IntegerField(
        default=45, help_text="Estimated time for this lesson in minutes"
    )

    # Kolibri content node link (optional)
    contentnode_id = models.CharField(
        max_length=32,
        blank=True,
        help_text="Link to Kolibri content node if content is imported",
    )

    class Meta:
        verbose_name = "Lesson Plan"
        verbose_name_plural = "Lesson Plans"
        unique_together = ("week", "lesson_number")
        ordering = ["week", "lesson_number"]

    def __str__(self):
        return f"{self.week} - Lesson {self.lesson_number}: {self.title}"


class Assessment(models.Model):
    """
    An assessment within a course (quiz, test, exam, project, written assignment).
    """

    ASSESSMENT_TYPE_CHOICES = [
        ("weekly_quiz", "Weekly Quiz"),
        ("unit_test", "Unit Test"),
        ("midterm", "Midterm Exam"),
        ("final", "Final Exam"),
        ("project", "Project"),
        ("written_assignment", "Written Assignment"),
        ("discussion", "Discussion/Forum"),
        ("lab_report", "Lab Report"),
    ]

    course = models.ForeignKey(
        CourseBlueprint, related_name="assessments", on_delete=models.CASCADE
    )
    week = models.ForeignKey(
        Week,
        related_name="assessments",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text="Associated week (if applicable)",
    )

    assessment_type = models.CharField(max_length=50, choices=ASSESSMENT_TYPE_CHOICES)
    title = models.CharField(max_length=200, help_text="Assessment title")
    description = models.TextField(blank=True, help_text="Assessment description")

    # Assessment metadata
    points_possible = models.IntegerField(
        default=100, help_text="Maximum points for this assessment"
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.00,
        help_text="Weight in final grade calculation",
    )
    estimated_minutes = models.IntegerField(
        default=30, help_text="Estimated time to complete (minutes)"
    )

    # Proctoring and academic integrity (for NCAA)
    is_proctored = models.BooleanField(
        default=False, help_text="Whether assessment requires proctoring"
    )
    proctoring_requirements = models.TextField(
        blank=True, help_text="Proctoring requirements/instructions"
    )

    # Grading
    rubric = JSONField(
        default=dict, blank=True, help_text="Grading rubric or criteria"
    )
    has_teacher_grading = models.BooleanField(
        default=False,
        help_text="Whether this requires manual teacher grading (vs. auto-graded)",
    )

    # Kolibri exam link (optional)
    exam_id = models.CharField(
        max_length=32,
        blank=True,
        help_text="Link to Kolibri exam if created in system",
    )

    class Meta:
        verbose_name = "Assessment"
        verbose_name_plural = "Assessments"
        ordering = ["course", "week__week_number", "assessment_type"]

    def __str__(self):
        week_str = f" (Week {self.week.week_number})" if self.week else ""
        return f"{self.course.course_id} - {self.title}{week_str}"


class GradeCategory(models.Model):
    """
    Grading categories for a course (e.g., Homework 30%, Tests 40%, Final 30%).
    """

    course = models.ForeignKey(
        CourseBlueprint, related_name="grade_categories", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100, help_text="Category name (e.g., 'Quizzes')")
    description = models.TextField(blank=True)
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage weight in final grade (0-100)",
    )
    drop_lowest = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Number of lowest scores to drop in this category",
    )

    class Meta:
        verbose_name = "Grade Category"
        verbose_name_plural = "Grade Categories"
        unique_together = ("course", "name")

    def __str__(self):
        return f"{self.course.title} - {self.name} ({self.weight}%)"
