# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from movies.models import Movie
import time
import random
from django.core.serializers import serialize, deserialize


@shared_task
def add(x, y):
    time.sleep(5)
    return x + y


@shared_task
def random_movies():
    movie = random.choice(Movie.objects.all())
    time.sleep(5)
    return movie.id
