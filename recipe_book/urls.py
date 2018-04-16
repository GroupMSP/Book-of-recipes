from django.urls import path

from . import views

urlpatterns = [
    path('', views.IngredientsListView.as_view()),
    path('ingredients/', views.IngredientsListView.as_view(), name='ingredients'),
    path('recipes/', views.RecipesListView.as_view(), name='recipes'),
    path('ingredients_search/', views.IngredientSearchListView.as_view(),
        name='ingredients_search'),
    path('recipes_search/', views.RecipeSearchListView.as_view(),
        name='recipes_search'),
    path('recipe/<int:pk>/', views.RecipeView.as_view(), name='recipe'),
    path('categorized_recipe/<int:type>/', views.CategorizedRecipeView.as_view(), name='categorized_recipe'),
]