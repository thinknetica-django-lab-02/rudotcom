from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        import main.signals
        print('Starting Scheduler...')
        from main.schedule import weekly_update
        weekly_update.start()
