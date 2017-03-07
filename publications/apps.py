from django.apps import AppConfig


class PublicationsConfig(AppConfig):
    name = 'publications'

    def ready(self):
        from publications import signals
        print("PublicationsConfig ready called")

