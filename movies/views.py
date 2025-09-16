from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, MovieRequest
from django.contrib.auth.decorators import login_required

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    template_data['average_rating'] = movie.average_rating()
    return render(request, 'movies/show.html', {'template_data': template_data})


@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment']!= '' and request.POST['rating']!= '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.rating = int(request.POST['rating'])
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    
@login_required
def edit_review(request, id, review_id):

    review = get_object_or_404(Review, id=review_id)

    if request.user != review.user:
        return redirect('movies.show', id=id)

    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})

    elif request.method == 'POST' and request.POST['comment'] != '' and request.POST['rating'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.rating = int(request.POST['rating'])
        review.save()
        return redirect('movies.show', id=id)

    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,user=request.user)
    review.delete()
    
    return redirect('movies.show', id=id)

def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')

@login_required
def movie_requests(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        
        if title:
            movie_request = MovieRequest()
            movie_request.title = title
            movie_request.description = description
            movie_request.requested_by = request.user
            movie_request.save()
            return redirect('movies.requests')
    
    requests = MovieRequest.objects.filter(requested_by=request.user).order_by('-date_requested')
    
    template_data = {}
    template_data['title'] = 'My Movie Requests'
    template_data['requests'] = requests
    return render(request, 'movies/requests.html', {'template_data': template_data})

@login_required
def delete_request(request, request_id):
    movie_request = get_object_or_404(MovieRequest, id=request_id, requested_by=request.user)
    movie_request.delete()
    return redirect('movies.requests')