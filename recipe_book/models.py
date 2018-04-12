from django.db import models
from .utils import FilePathGenerator

class IngredientType(models.Model):
    name = models.CharField(max_length=63)


class RecipeType(models.Model):
    name = models.CharField(max_length=63)


class Instruction(models.Model):
    id_recipe = models.ForeignKey(to='Recipe', on_delete=models.CASCADE)
    step = models.IntegerField()
    text = models.CharField(max_length=1023)


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1023, blank=True)
    preparation_time = models.DurationField()
    image = models.FileField(upload_to=FilePathGenerator(), null=True,
        blank=True)
    id_type = models.ForeignKey(to=RecipeType, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField('Ingredient',
        through='Recipe_ingredient', related_name='recipes')


class Ingredient(models.Model):
    name = models.CharField(max_length=63)
    image = models.FileField(upload_to=FilePathGenerator(), null=True,
        blank=True)
    id_type = models.ForeignKey(to=IngredientType, on_delete=models.CASCADE)


class Recipe_ingredient(models.Model):
    id_recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE)
    id_ingredient = models.ForeignKey(to=Ingredient, on_delete=models.CASCADE)
    amount = models.CharField(max_length=63)