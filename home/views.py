from django.shortcuts import render
from movies.models import Movie
from django.db.models import Avg

def index(request):
    # Get movies with their average ratings, ordered by highest rating
    movies_with_ratings = Movie.objects.annotate(
        avg_rating=Avg('review__rating')
    ).order_by('-avg_rating', 'name')[:6]  # Get top 6 highest rated movies
    
    template_data = {}
    template_data['title'] = 'GT Movie Store'
    template_data['top_movies'] = movies_with_ratings
    return render(request, 'home/index.html', {'template_data': template_data})

def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html', {'template_data': template_data})