from django.contrib import admin

from .models import *

admin.site.register([RecipeType, Instruction, Recipe, Ingredient, Recipe_ingredient])