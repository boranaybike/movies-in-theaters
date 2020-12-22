import requests
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import Http404
from . import config
from datetime import date, timedelta, datetime
from .models import Movie, Comment
from .forms import CommentModelForm

dt = date.today() - timedelta(7)
prevDt = dt.strftime("%Y-%m-%d")
today = date.today()
todayStr = today.strftime("%Y-%m-%d")


# Create your views here.
def index(request):
    movies = Movie.objects.filter(playing_now=True)
    context = {
        'movies': movies,
        'loggedin': request.user.is_authenticated
    }
    return render(request, 'movies/list.html', context)


def search(request):
    return render(request, 'movies/search.html')


def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    comment_form = None
    if request.user.is_authenticated:
        instance = Comment.objects.filter(user=request.user, movie=movie).first()
        comment_form = CommentModelForm(request.POST or None, instance=instance)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.movie = movie
            comment.user = request.user
            comment.save()
            return redirect('homepage')

    context = {
        'movie': movie,
        'comment_form': comment_form,
        'isLoggedin': request.user.is_authenticated
    }
    return render(request, 'movies/detail.html', context)

def prev(request):
    movies = Movie.objects.filter(playing_now=False)
    context = {
        'movies': movies,
        'loggedin': request.user.is_authenticated
    }
    return render(request, 'movies/list.html', context)