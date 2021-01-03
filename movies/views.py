import requests
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from user.models import Profile
from . import config
from datetime import date, timedelta, datetime
from .models import Movie, Comment
from .forms import CommentModelForm
from django.core.paginator import Paginator


def index(request):
    movies = Movie.objects.filter(playing_now=True)
    query = request.GET.get('q')
    if query:
        movies = movies.filter(name__icontains=query)
    m_paginator = Paginator(movies, 3)
    page_num = request.GET.get('page')
    page = m_paginator.get_page(page_num)
    context = {
        'movies': movies,
        'loggedin': request.user.is_authenticated,
        'count': m_paginator.count,
        'page': page
    }
    return render(request, 'movies/list.html', context)


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
    query = request.GET.get('q')
    if query:
        movies = movies.filter(name__icontains=query)
    m_paginator = Paginator(movies, 3)
    page_num = request.GET.get('page')
    page = m_paginator.get_page(page_num)
    context = {
        'movies': movies,
        'loggedin': request.user.is_authenticated,
        'count': m_paginator.count,
        'page': page
    }

    return render(request, 'movies/list.html', context)