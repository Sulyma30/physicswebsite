from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    re_path( r'^olympiads/(?P<olymp_type>[a-z]+)(?:/(?P<static_location>[a-zA-Z_]+))?/$', views.olympiads, name="olympiads")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)