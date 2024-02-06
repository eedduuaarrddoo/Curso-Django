from django.shortcuts import render, get_object_or_404
#from utils.recipes.factory import make_recipe
from django.http import HttpResponse
from .models import Recipe



def home(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })


def category(request, category_id):
    recipes = Recipe.objects.filter(
        category__id=category_id,
         is_published=True,
    ).order_by('-id')
    
    if not recipes:
        return HttpResponse ('NOT FOUND', status=404)
    
    
    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes.first().category.name}- Category |'
        
    })


def recipe(request, id):
   
    """ recipe = Recipe.objects.filter(
        pk=id,
        is_published=True,
    ).order_by('-id').first() 
    """
    
    recipe = get_object_or_404(Recipe, pk=id, is_published=True,)
    
    return render(request, 'recipes/pages/recipe-view.html', context={
        'is_detail_page': True,
        'recipe': recipe,
    })