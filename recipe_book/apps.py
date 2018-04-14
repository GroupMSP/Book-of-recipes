from django.apps import AppConfig


class RecipeBookConfig(AppConfig):
    name = 'recipe_book'

    def ready(self):
        from . import signals