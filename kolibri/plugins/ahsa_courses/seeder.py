"""
Course Blueprint Seeder
=======================

Imports course blueprint data into the database.
"""
import json
import logging

from django.db import transaction

from .models import Assessment
from .models import CourseBlueprint
from .models import GradeCategory
from .models import LessonPlan
from .models import Semester
from .models import Week
from .validators import validate_blueprint

logger = logging.getLogger(__name__)


class CourseBlueprintSeeder:
    """
    Handles importing course blueprint data into the database.
    """

    def __init__(self, dry_run=False, update_existing=False):
        """
        Initialize the seeder.

        Args:
            dry_run (bool): If True, validate but don't save to database
            update_existing (bool): If True, update existing courses instead of skipping
        """
        self.dry_run = dry_run
        self.update_existing = update_existing
        self.stats = {"created": 0, "updated": 0, "skipped": 0, "errors": 0}

    def seed_from_dict(self, blueprint_data):
        """
        Seed a course blueprint from a dictionary.

        Args:
            blueprint_data (dict): Course blueprint data

        Returns:
            tuple: (success, message, course_blueprint)
        """
        # Validate the blueprint
        is_valid, errors = validate_blueprint(blueprint_data)
        if not is_valid:
            error_msg = f"Validation errors: {', '.join(errors)}"
            logger.error(error_msg)
            self.stats["errors"] += 1
            return False, error_msg, None

        course_id = blueprint_data["course_id"]

        # Check if course already exists
        try:
            existing_course = CourseBlueprint.objects.get(course_id=course_id)
            if not self.update_existing:
                msg = f"Course {course_id} already exists, skipping"
                logger.info(msg)
                self.stats["skipped"] += 1
                return True, msg, existing_course
            else:
                msg = f"Updating existing course {course_id}"
                logger.info(msg)
                return self._update_course(existing_course, blueprint_data)
        except CourseBlueprint.DoesNotExist:
            msg = f"Creating new course {course_id}"
            logger.info(msg)
            return self._create_course(blueprint_data)

    def _create_course(self, data):
        """Create a new course blueprint."""
        if self.dry_run:
            msg = f"[DRY RUN] Would create course: {data['course_id']}"
            logger.info(msg)
            return True, msg, None

        try:
            with transaction.atomic():
                # Extract nested data
                weeks_data = data.pop("weeks", [])
                semesters_data = data.pop("semesters", [])
                grade_categories_data = data.pop("grade_categories", [])

                # Create course blueprint
                course = CourseBlueprint.objects.create(**data)

                # Create semesters
                for semester_data in semesters_data:
                    semester_weeks = semester_data.pop("weeks", [])
                    semester = Semester.objects.create(course=course, **semester_data)

                # Create weeks
                for week_data in weeks_data:
                    lesson_plans_data = week_data.pop("lesson_plans", [])
                    assessments_data = week_data.pop("assessments", [])

                    # Find semester if specified
                    semester_number = week_data.pop("semester_number", None)
                    semester = None
                    if semester_number:
                        try:
                            semester = course.semesters.get(
                                semester_number=semester_number
                            )
                        except Semester.DoesNotExist:
                            pass

                    week = Week.objects.create(
                        course=course, semester=semester, **week_data
                    )

                    # Create lesson plans
                    for lesson_data in lesson_plans_data:
                        LessonPlan.objects.create(week=week, **lesson_data)

                    # Create assessments
                    for assessment_data in assessments_data:
                        Assessment.objects.create(
                            course=course, week=week, **assessment_data
                        )

                # Create grade categories
                for category_data in grade_categories_data:
                    GradeCategory.objects.create(course=course, **category_data)

                self.stats["created"] += 1
                msg = f"Successfully created course: {course.course_id}"
                logger.info(msg)
                return True, msg, course

        except Exception as e:
            self.stats["errors"] += 1
            error_msg = f"Error creating course {data.get('course_id')}: {str(e)}"
            logger.error(error_msg)
            return False, error_msg, None

    def _update_course(self, course, data):
        """Update an existing course blueprint."""
        if self.dry_run:
            msg = f"[DRY RUN] Would update course: {data['course_id']}"
            logger.info(msg)
            return True, msg, course

        try:
            with transaction.atomic():
                # Extract nested data
                weeks_data = data.pop("weeks", [])
                semesters_data = data.pop("semesters", [])
                grade_categories_data = data.pop("grade_categories", [])

                # Update course fields
                for field, value in data.items():
                    setattr(course, field, value)
                course.save()

                # Clear and recreate nested objects
                course.weeks.all().delete()
                course.semesters.all().delete()
                course.grade_categories.all().delete()

                # Recreate semesters
                for semester_data in semesters_data:
                    semester_data.pop("weeks", [])
                    Semester.objects.create(course=course, **semester_data)

                # Recreate weeks
                for week_data in weeks_data:
                    lesson_plans_data = week_data.pop("lesson_plans", [])
                    assessments_data = week_data.pop("assessments", [])
                    semester_number = week_data.pop("semester_number", None)

                    semester = None
                    if semester_number:
                        try:
                            semester = course.semesters.get(
                                semester_number=semester_number
                            )
                        except Semester.DoesNotExist:
                            pass

                    week = Week.objects.create(
                        course=course, semester=semester, **week_data
                    )

                    for lesson_data in lesson_plans_data:
                        LessonPlan.objects.create(week=week, **lesson_data)

                    for assessment_data in assessments_data:
                        Assessment.objects.create(
                            course=course, week=week, **assessment_data
                        )

                # Recreate grade categories
                for category_data in grade_categories_data:
                    GradeCategory.objects.create(course=course, **category_data)

                self.stats["updated"] += 1
                msg = f"Successfully updated course: {course.course_id}"
                logger.info(msg)
                return True, msg, course

        except Exception as e:
            self.stats["errors"] += 1
            error_msg = f"Error updating course {course.course_id}: {str(e)}"
            logger.error(error_msg)
            return False, error_msg, None

    def seed_from_file(self, file_path):
        """
        Seed a course blueprint from a JSON or YAML file.

        Args:
            file_path (str): Path to the blueprint file

        Returns:
            tuple: (success, message, course_blueprint)
        """
        try:
            with open(file_path, "r") as f:
                if file_path.endswith(".json"):
                    data = json.load(f)
                elif file_path.endswith((".yaml", ".yml")):
                    import yaml

                    data = yaml.safe_load(f)
                else:
                    msg = f"Unsupported file format: {file_path}"
                    logger.error(msg)
                    self.stats["errors"] += 1
                    return False, msg, None

            return self.seed_from_dict(data)

        except FileNotFoundError:
            msg = f"File not found: {file_path}"
            logger.error(msg)
            self.stats["errors"] += 1
            return False, msg, None
        except Exception as e:
            msg = f"Error reading file {file_path}: {str(e)}"
            logger.error(msg)
            self.stats["errors"] += 1
            return False, msg, None

    def get_stats(self):
        """Get seeding statistics."""
        return self.stats

    def print_stats(self):
        """Print seeding statistics."""
        print("\n" + "=" * 50)
        print("Course Seeding Summary")
        print("=" * 50)
        print(f"Created:  {self.stats['created']}")
        print(f"Updated:  {self.stats['updated']}")
        print(f"Skipped:  {self.stats['skipped']}")
        print(f"Errors:   {self.stats['errors']}")
        print("=" * 50 + "\n")
