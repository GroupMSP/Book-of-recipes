from django.db import models
from .utils import FilePathGenerator
from collections import namedtuple


RecipeRequiredIngredientsTuple = namedtuple('RecipeRequiredIngredientsTuple',
    'recipe required')


class IngredientType(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return '(%d) %s' % (self.id, self.name)


class RecipeType(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return '(%d) %s' % (self.id, self.name)


class Instruction(models.Model):
    id_recipe = models.ForeignKey(to='Recipe', on_delete=models.CASCADE)
    step = models.IntegerField()
    text = models.CharField(max_length=1023)

    def __str__(self):
        return '(%d) step %d: %s' % (self.id, self.step, self.text[:80])


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1023, blank=True)
    preparation_time = models.DurationField()
    image = models.FileField(upload_to=FilePathGenerator(), null=True,
        blank=True)
    id_type = models.ForeignKey(to=RecipeType, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField('Ingredient',
        through='Recipe_ingredient', related_name='recipes')

    def __str__(self):
        return '(%d) %s' % (self.id, self.name)

    def get_by_ingredients_ids(ids):
        """
        ids: list of numeric id ingredients, e.g. [1,2,3,...]
        return list of tuple:
        [(recipe_object, required_ingredients_count), ...]
        """
        recipe_ids = Recipe_ingredient.objects.filter(id_ingredient__in=ids).select_related('id_recipe').distinct().values_list('id_recipe', flat=True)

        query = Recipe.objects.filter(id__in=recipe_ids).prefetch_related('ingredients')

        result = [
            RecipeRequiredIngredientsTuple(
                recipe,
                sum(# need count of ids
                    1 for ingredient_id in
                    recipe.ingredients.values_list('id',flat=True)
                    if ingredient_id not in ids
                )
            )
            for recipe in query
        ]
        return result


class Ingredient(models.Model):
    name = models.CharField(max_length=63)
    image = models.FileField(upload_to=FilePathGenerator(), null=True,
        blank=True)
    id_type = models.ForeignKey(to=IngredientType, on_delete=models.CASCADE)

    def __str__(self):
        return '(%d) %s' % (self.id, self.name)


class Recipe_ingredient(models.Model):
    id_recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE)
    id_ingredient = models.ForeignKey(to=Ingredient, on_delete=models.CASCADE)
    amount = models.CharField(max_length=63)

    def __str__(self):
        return '(%d) %s <-> %s' % (self.id, self.id_recipe.name, self.id_ingredient.name)
