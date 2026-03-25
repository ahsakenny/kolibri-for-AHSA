"""
Django management command for seeding AHSA course blueprints.

Usage:
    python manage.py seed_ahsa_courses --all
    python manage.py seed_ahsa_courses --course algebra_1
    python manage.py seed_ahsa_courses --subject math --grade 9
    python manage.py seed_ahsa_courses --file /path/to/blueprint.json
"""
import glob
import logging
import os

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from kolibri.plugins.ahsa_courses.seeder import CourseBlueprintSeeder

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Seed AHSA course blueprints into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--all",
            action="store_true",
            help="Seed all course blueprints from blueprints directory",
        )

        parser.add_argument(
            "--course",
            type=str,
            help="Seed a specific course by course_id (e.g., 'ahsa_alg1')",
        )

        parser.add_argument(
            "--subject",
            type=str,
            choices=["math", "ela", "science", "social_studies", "elective"],
            help="Seed all courses for a specific subject",
        )

        parser.add_argument(
            "--grade",
            type=int,
            help="Seed all courses for a specific grade level (6-12)",
        )

        parser.add_argument(
            "--file", type=str, help="Seed from a specific blueprint file"
        )

        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Validate blueprints without saving to database",
        )

        parser.add_argument(
            "--update",
            action="store_true",
            help="Update existing courses instead of skipping them",
        )

    def handle(self, *args, **options):
        """Execute the command."""
        dry_run = options["dry_run"]
        update_existing = options["update"]

        self.stdout.write(
            self.style.WARNING(
                "\n" + "=" * 60 + "\nAHSA Course Blueprint Seeding\n" + "=" * 60
            )
        )

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    "DRY RUN MODE: Validating blueprints without saving\n"
                )
            )

        seeder = CourseBlueprintSeeder(dry_run=dry_run, update_existing=update_existing)

        # Determine blueprints directory
        plugin_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )  # Go up two levels from commands/
        blueprints_dir = os.path.join(plugin_dir, "blueprints")

        if options["file"]:
            # Seed from specific file
            file_path = options["file"]
            self.stdout.write(f"Seeding from file: {file_path}\n")
            success, message, course = seeder.seed_from_file(file_path)

            if success:
                self.stdout.write(self.style.SUCCESS(f"✓ {message}"))
            else:
                self.stdout.write(self.style.ERROR(f"✗ {message}"))

        elif options["all"]:
            # Seed all blueprints
            self.stdout.write(f"Seeding all blueprints from: {blueprints_dir}\n")
            blueprint_files = glob.glob(os.path.join(blueprints_dir, "*.json")) + glob.glob(
                os.path.join(blueprints_dir, "*.yaml")
            )

            if not blueprint_files:
                raise CommandError(
                    f"No blueprint files found in {blueprints_dir}"
                )

            for file_path in sorted(blueprint_files):
                filename = os.path.basename(file_path)
                self.stdout.write(f"\nProcessing: {filename}")
                success, message, course = seeder.seed_from_file(file_path)

                if success:
                    self.stdout.write(self.style.SUCCESS(f"  ✓ {message}"))
                else:
                    self.stdout.write(self.style.ERROR(f"  ✗ {message}"))

        elif options["course"]:
            # Seed specific course
            course_id = options["course"]
            file_path = os.path.join(blueprints_dir, f"{course_id}.json")

            if not os.path.exists(file_path):
                # Try YAML
                file_path = os.path.join(blueprints_dir, f"{course_id}.yaml")

            if not os.path.exists(file_path):
                raise CommandError(
                    f"Blueprint file not found for course: {course_id}"
                )

            self.stdout.write(f"Seeding course: {course_id}\n")
            success, message, course = seeder.seed_from_file(file_path)

            if success:
                self.stdout.write(self.style.SUCCESS(f"✓ {message}"))
            else:
                self.stdout.write(self.style.ERROR(f"✗ {message}"))

        elif options["subject"] or options["grade"]:
            # Filter by subject and/or grade
            blueprint_files = glob.glob(os.path.join(blueprints_dir, "*.json")) + glob.glob(
                os.path.join(blueprints_dir, "*.yaml")
            )

            if not blueprint_files:
                raise CommandError(
                    f"No blueprint files found in {blueprints_dir}"
                )

            # This is a simple name-based filter
            # For more sophisticated filtering, we'd need to load each file
            subject = options.get("subject")
            grade = options.get("grade")

            filtered_files = blueprint_files
            if subject:
                filtered_files = [
                    f for f in filtered_files if subject in os.path.basename(f).lower()
                ]
            if grade:
                filtered_files = [
                    f for f in filtered_files if f"g{grade}" in os.path.basename(f).lower()
                ]

            if not filtered_files:
                self.stdout.write(
                    self.style.WARNING(
                        f"No blueprints found matching filters (subject={subject}, grade={grade})"
                    )
                )
            else:
                self.stdout.write(f"Found {len(filtered_files)} matching blueprints\n")
                for file_path in sorted(filtered_files):
                    filename = os.path.basename(file_path)
                    self.stdout.write(f"\nProcessing: {filename}")
                    success, message, course = seeder.seed_from_file(file_path)

                    if success:
                        self.stdout.write(self.style.SUCCESS(f"  ✓ {message}"))
                    else:
                        self.stdout.write(self.style.ERROR(f"  ✗ {message}"))

        else:
            raise CommandError(
                "Please specify --all, --course, --file, or --subject/--grade"
            )

        # Print statistics
        stats = seeder.get_stats()
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.WARNING("Seeding Summary"))
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS(f"Created:  {stats['created']}"))
        self.stdout.write(self.style.SUCCESS(f"Updated:  {stats['updated']}"))
        self.stdout.write(self.style.WARNING(f"Skipped:  {stats['skipped']}"))
        self.stdout.write(self.style.ERROR(f"Errors:   {stats['errors']}"))
        self.stdout.write("=" * 60 + "\n")

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    "DRY RUN COMPLETE: No changes were made to the database\n"
                )
            )
