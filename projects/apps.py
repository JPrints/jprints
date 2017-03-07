from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    name = 'projects'

    def ready(self):
        from core import signals
        print("ProjectsConfig ready called")

