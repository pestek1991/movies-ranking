from django.conf.urls import url, include
from movies import views



urlpatterns = [

    url(r'^movies/$', views.movies_list),
    url(r'^movies2/$', views.MoviesList.as_view()),
    url(r'^movies/edit/(\d{1,5})$', views.movie_edit, name="movie-edit"),
    url(r'^movies/add/$', views.movie_add),
    url(r'^movies/details/(\d{1,5})$', views.movie_details, name="movie-details"),
    url(r'^movies/remove/$', views.movie_remove),
    url(r'^movies/celer/$', views.celer),
    url(r'^login/$', views.login_user),
    url(r'^logout/$', views.logout_user),
]