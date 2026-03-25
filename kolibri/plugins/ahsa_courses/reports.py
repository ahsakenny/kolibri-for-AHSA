"""
NCAA Compliance and Reporting Tools
===================================

Tools for generating NCAA documentation and compliance reports.
"""
import csv
import io
from datetime import datetime

from django.http import HttpResponse


class NCAASyllabusExporter:
    """
    Generate NCAA-compliant syllabus exports.
    """

    @staticmethod
    def export_to_text(course):
        """
        Export course syllabus as formatted text document.

        Args:
            course (CourseBlueprint): The course to export

        Returns:
            str: Formatted syllabus text
        """
        lines = []
        lines.append("=" * 80)
        lines.append(f"{course.title}")
        lines.append(f"Course ID: {course.course_id}")
        lines.append("=" * 80)
        lines.append("")

        # Course Information
        lines.append("COURSE INFORMATION")
        lines.append("-" * 80)
        lines.append(f"Grade Level: {course.grade_level}")
        lines.append(f"Subject Area: {course.get_subject_display()}")
        lines.append(f"Credit Value: {course.credit_value}")
        lines.append(f"Duration: {course.get_duration_display()}")
        lines.append(f"Florida Standards: {course.florida_standard_set}")
        lines.append(f"NCAA Core Area: {course.get_ncaa_core_area_display()}")
        lines.append("")

        # Course Description
        lines.append("COURSE DESCRIPTION")
        lines.append("-" * 80)
        lines.append(course.description)
        lines.append("")

        # Instructional Time
        lines.append("INSTRUCTIONAL TIME")
        lines.append("-" * 80)
        lines.append(f"Total Weeks: {course.total_weeks}")
        lines.append(f"Weekly Minutes: {course.weekly_minutes}")
        lines.append(
            f"Total Instructional Minutes: {course.total_instructional_minutes}"
        )
        lines.append(
            f"Total Instructional Hours: {course.total_instructional_minutes / 60:.1f}"
        )
        lines.append("")

        # Course Requirements
        lines.append("COURSE REQUIREMENTS")
        lines.append("-" * 80)
        lines.append(f"Teacher-Led Instruction: {'Yes' if course.teacher_led else 'No'}")
        lines.append(f"Honors Course: {'Yes' if course.is_honors else 'No'}")
        lines.append(f"AP Course: {'Yes' if course.is_ap else 'No'}")
        lines.append(f"Lab Required: {'Yes' if course.requires_lab else 'No'}")
        lines.append("")

        # Required Materials
        if course.required_materials:
            lines.append("REQUIRED MATERIALS")
            lines.append("-" * 80)
            for material in course.required_materials:
                lines.append(f"- {material.get('title', 'N/A')}")
                if "source" in material:
                    lines.append(f"  Source: {material['source']}")
                if "url" in material:
                    lines.append(f"  URL: {material['url']}")
            lines.append("")

        # Grading Policy
        categories = course.grade_categories.all()
        if categories:
            lines.append("GRADING POLICY")
            lines.append("-" * 80)
            for category in categories:
                drop_text = (
                    f" (Drop lowest {category.drop_lowest})"
                    if category.drop_lowest > 0
                    else ""
                )
                lines.append(f"{category.name}: {category.weight}%{drop_text}")
            lines.append("")

        # Pacing Guide
        if course.pacing_guide:
            lines.append("PACING GUIDE")
            lines.append("-" * 80)
            lines.append(course.pacing_guide)
            lines.append("")

        # Weekly Schedule
        weeks = course.weeks.all().order_by("week_number")
        if weeks:
            lines.append("WEEKLY SCHEDULE")
            lines.append("-" * 80)
            for week in weeks:
                lines.append(f"Week {week.week_number}: {week.title}")
                if week.objectives:
                    lines.append("  Objectives:")
                    for obj in week.objectives:
                        lines.append(f"    - {obj}")
            lines.append("")

        # Academic Integrity
        if course.academic_integrity_policy:
            lines.append("ACADEMIC INTEGRITY POLICY")
            lines.append("-" * 80)
            lines.append(course.academic_integrity_policy)
            lines.append("")

        # Footer
        lines.append("=" * 80)
        lines.append(f"Syllabus generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("AHSA Learning Network")
        lines.append("=" * 80)

        return "\n".join(lines)

    @staticmethod
    def export_to_http_response(course):
        """
        Generate HTTP response with syllabus as downloadable text file.
        """
        content = NCAASyllabusExporter.export_to_text(course)
        response = HttpResponse(content, content_type="text/plain")
        response["Content-Disposition"] = (
            f'attachment; filename="{course.course_id}_syllabus.txt"'
        )
        return response


class NCAAComplianceReporter:
    """
    Generate NCAA compliance documentation.
    """

    @staticmethod
    def generate_compliance_report(course):
        """
        Generate NCAA compliance checklist report.

        Returns:
            dict: Compliance report with status indicators
        """
        report = {
            "course_id": course.course_id,
            "course_title": course.title,
            "ncaa_core_area": course.get_ncaa_core_area_display(),
            "checks": [],
        }

        # Check: NCAA core area classification
        report["checks"].append(
            {
                "category": "Core Classification",
                "requirement": "Course classified in NCAA core area",
                "status": course.ncaa_core_area != "none",
                "details": f"Classified as: {course.get_ncaa_core_area_display()}",
            }
        )

        # Check: Teacher-led instruction
        report["checks"].append(
            {
                "category": "Instruction",
                "requirement": "Teacher-led instruction required",
                "status": course.teacher_led,
                "details": "Teacher-led instruction is enabled"
                if course.teacher_led
                else "WARNING: Not teacher-led",
            }
        )

        # Check: Minimum instructional time (typically 140+ hours for full year)
        min_hours = 140
        actual_hours = course.total_instructional_minutes / 60
        report["checks"].append(
            {
                "category": "Instructional Time",
                "requirement": f"Minimum {min_hours} hours of instruction",
                "status": actual_hours >= min_hours,
                "details": f"{actual_hours:.1f} hours total",
            }
        )

        # Check: Proctored assessments
        proctored_assessments = course.assessments.filter(is_proctored=True).count()
        report["checks"].append(
            {
                "category": "Assessments",
                "requirement": "Proctored exams for midterm and final",
                "status": proctored_assessments >= 2,
                "details": f"{proctored_assessments} proctored assessments",
            }
        )

        # Check: Academic integrity policy
        report["checks"].append(
            {
                "category": "Academic Integrity",
                "requirement": "Academic integrity policy documented",
                "status": bool(course.academic_integrity_policy),
                "details": "Policy documented"
                if course.academic_integrity_policy
                else "WARNING: No policy documented",
            }
        )

        # Check: Teacher interaction checkpoints
        weeks_with_interaction = course.weeks.filter(
            requires_teacher_interaction=True
        ).count()
        total_weeks = course.weeks.count()
        interaction_percentage = (
            (weeks_with_interaction / total_weeks * 100) if total_weeks > 0 else 0
        )
        report["checks"].append(
            {
                "category": "Teacher Interaction",
                "requirement": "Regular teacher interaction throughout course",
                "status": interaction_percentage >= 75,
                "details": f"{weeks_with_interaction}/{total_weeks} weeks ({interaction_percentage:.0f}%)",
            }
        )

        # Overall compliance status
        all_passed = all(check["status"] for check in report["checks"])
        report["overall_status"] = "COMPLIANT" if all_passed else "NEEDS REVIEW"
        report["compliance_percentage"] = (
            sum(1 for check in report["checks"] if check["status"])
            / len(report["checks"])
            * 100
        )

        return report


class PacingGuideExporter:
    """
    Export detailed pacing guides for NCAA documentation.
    """

    @staticmethod
    def export_to_csv(course):
        """
        Export week-by-week pacing guide to CSV.

        Returns:
            str: CSV content
        """
        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(
            [
                "Week",
                "Title",
                "Objectives",
                "Standards",
                "Estimated Minutes",
                "Lessons",
                "Assessments",
                "Teacher Interaction Required",
            ]
        )

        # Data rows
        weeks = course.weeks.all().order_by("week_number")
        for week in weeks:
            objectives_str = "; ".join(week.objectives) if week.objectives else ""
            standards_str = (
                "; ".join(week.standards_alignment)
                if week.standards_alignment
                else ""
            )
            lesson_count = week.lesson_plans.count()
            assessment_count = week.assessments.count()

            writer.writerow(
                [
                    week.week_number,
                    week.title,
                    objectives_str,
                    standards_str,
                    week.estimated_minutes,
                    lesson_count,
                    assessment_count,
                    "Yes" if week.requires_teacher_interaction else "No",
                ]
            )

        return output.getvalue()

    @staticmethod
    def export_to_http_response(course):
        """
        Generate HTTP response with pacing guide as downloadable CSV.
        """
        content = PacingGuideExporter.export_to_csv(course)
        response = HttpResponse(content, content_type="text/csv")
        response["Content-Disposition"] = (
            f'attachment; filename="{course.course_id}_pacing_guide.csv"'
        )
        return response


class StandardsAlignmentReporter:
    """
    Generate standards alignment reports.
    """

    @staticmethod
    def generate_alignment_report(course):
        """
        Generate comprehensive standards alignment report.

        Returns:
            dict: Standards alignment data
        """
        weeks = course.weeks.all().order_by("week_number")

        # Build standards map
        standards_coverage = {}
        for week in weeks:
            for standard in week.standards_alignment or []:
                if standard not in standards_coverage:
                    standards_coverage[standard] = []
                standards_coverage[standard].append(
                    {
                        "week_number": week.week_number,
                        "week_title": week.title,
                        "objectives": week.objectives,
                    }
                )

        report = {
            "course_id": course.course_id,
            "course_title": course.title,
            "florida_standard_set": course.florida_standard_set,
            "total_standards": len(standards_coverage),
            "total_weeks": weeks.count(),
            "standards": [
                {"standard": standard, "coverage": coverage}
                for standard, coverage in sorted(standards_coverage.items())
            ],
        }

        return report
