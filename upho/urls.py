from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    re_path( r'^olympiads/(?P<olymp_type>[a-z]+)(?:/(?P<static_location>[a-zA-Z_]+))?/$', views.olympiad_page, name="olympiads"),

    # API
    re_path( r'^olympiads_api/(?P<olymp_type>[a-z]+)(?:/(?P<static_location>[a-zA-Z_]+))?/$', views.olympiad)
]
