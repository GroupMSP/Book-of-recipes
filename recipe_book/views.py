from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import views

from . import models

class IngredientsListView(views.generic.ListView):
    model = models.Ingredient
    template_name = 'recipe_book/ingredient_list.html'
    context_object_name = 'ingredients'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = models.IngredientType.objects.all().values()
        return context


class RecipesListView(views.generic.ListView):
    template_name = 'recipe_book/recipe_list.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return models.Recipe.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = list(models.RecipeType.objects.all().values())
        return context


class IngredientSearchListView(views.generic.TemplateView):
    template_name = 'recipe_book/ingredient_saerch_result.html'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('ingredients'))

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def get_queryset(self, ids):
        if ids == '':
            return []
        return models.Recipe.get_by_ingredients_ids(list(map(int,ids.split(','))))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ids = self.request.POST.get('ids')
        context['object_list'] = self.get_queryset(ids)
        return context


class RecipeSearchListView(views.generic.TemplateView):
    template_name = 'recipe_book/recipes_search_result.html'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('recipes'))

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def get_queryset(self, q):
        return models.Recipe.objects.filter(name__icontains=q.lower())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.POST.get('q')
        context['recipes'] = self.get_queryset(q)
        context['q']=q
        return context


class RecipeView(views.generic.DetailView):
    template_name = 'recipe_book/recipe.html'
    model = models.Recipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategorizedRecipeView(RecipesListView):
    def get_queryset(self):
        return models.Recipe.objects.filter(id_type=self.kwargs['type'])


class MoreRecipesView(views.View):
    template_name = 'recipe_book/null'

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def get_queryset(self, type_id, offset, amount):
        if type_id is None:
            return models.Recipe.objects.all()[offset:offset + amount]
        else:
            return models.Recipe.objects.filter(id_type=type_id)[offset:offset + amount]

    def get_context_data(self, **kwargs):
        context = {}
        type_id = int(self.request.GET.get('type_id'))
        offset = int(self.request.GET.get('offset', default=0))
        amount = int(self.request.GET.get('amount', default=30))
        context['recipes'] = self.get_queryset(type_id, offset, amount)
        return context
