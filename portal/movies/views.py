# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from movies.models import Movie, MovieForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django.views.generic import ListView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from movies.tasks import random_movies, add

# Create your views here.

@login_required
def movies_list(request, alert_remove = False):
    movies = Movie.objects.all()
    length = len(movies)
    page = request.GET.get('page', 1)
    paginator = Paginator(movies, 3)
    try:
        moviess = paginator.page(page)
    except PageNotAnInteger:
        moviess = paginator.page(1)
    except EmptyPage:
        moviess = paginator.page(paginator.num_pages)
    return render(request, 'movies/list.html', {'movies': moviess, 'movies_len': length, 'alert_remove':alert_remove})


@login_required
def movie_edit(request, param_id):
    try:
        movie = Movie.objects.get(id=param_id)
    except Movie.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            alert = True
            form = MovieForm(instance=movie)
            return render(request, 'movies/edit.html', locals())
    else:
        form = MovieForm(instance = movie)
    return render(request, 'movies/edit.html', locals())

@login_required
def movie_details(request, param_id):
    try:
        movie = Movie.objects.get(id=param_id)
    except Movie.DoesNotExist:
        raise Http404
    movie.trailer_url = movie.trailer_url.replace("watch?v=", "embed/")
    return render(request, 'movies/details.html', locals())

@login_required
def movie_add(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = MovieForm()
            alert = True
    else:
        form = MovieForm()
    return render(request, 'movies/add.html', locals())

@login_required
def movie_remove(request):
    if request.method == 'POST':
        try:
            item_id = int(request.POST.get('item_id', -1))
            item = Movie.objects.get(id=item_id)
        except Movie.DoesNotExist:
            raise Http404
        item.delete()
        return movies_list(request, True)
    raise Http404

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if "next" in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
                else:
                    return HttpResponseRedirect("/movies")
            else:
                alert_error = "Konto zablokowane"
        else:
            alert_error = "Zły login lub hasło"
        form = AuthenticationForm()
        return render(request, 'login/login.html', locals())

    else:
        form = AuthenticationForm()
        if "next" in request.GET:
            alert = True
        return render(request, 'login/login.html', locals())


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required
def celer(request):
    movie = random_movies.delay()
    id = movie.get()
    movie = Movie.objects.get(id=id)
    movie.trailer_url = movie.trailer_url.replace("watch?v=", "embed/")
    return render(request, 'movies/celer.html', locals())


@method_decorator(login_required, name='dispatch')
class MoviesList(ListView):
    template_name = "movies/list.html"
    model = Movie
    context_object_name = 'movies'











