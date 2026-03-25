from kolibri.plugins import KolibriPluginBase


class AHSACoursesPlugin(KolibriPluginBase):
    """
    Main plugin class for AHSA Courses system.
    Provides course blueprint models and seeding functionality.
    """

    # API URLs for course management
    untranslated_view_urls = "api_urls"
