from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('materials', views.materials, name="materials"),
    re_path( r'^olympiads/(?P<olymp_type>[a-z]+)(?:/(?P<static_location>[a-zA-Z_]+))?/$', views.olympiads, name="olympiads"),
    path('literature/<str:literature_type>', views.literature, name="literature"),
    path('ipho', views.ipho, name="ipho"),
    path('materials/<int:theme_id>/<str:task_type>', views.material, name="material"),

    # API

    path('tasks/<int:theme_id>/<str:task_type>', views.tasks, name='task'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)