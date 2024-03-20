from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Recipe
from django.http.response import Http404
from django.db.models import Q
from utils.pagination import make_pagination_range


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by('-id')
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page=1
    
    paginator = Paginator(recipes, 9)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        4,
        current_page
    )

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range' : pagination_range
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

def search(request):
    search_term = request.GET.get('q', '').strip()
    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
      Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        is_published=True
    ).order_by('-id')

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'recipes': recipes,
    })