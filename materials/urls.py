from django.urls import path, re_path

from . import views

urlpatterns = [
    path('literature/<str:literature_type>', views.literature_page, name="literature"),
    path('materials', views.materials_page, name="materials"),
    path('materials/<int:theme_id>/<str:task_type>', views.material_page, name="material"),

    # API
    re_path('^materials_api/(?P<theme_id>[0-9]+)/(?P<task_type>[a-z]+)$', views.material),
    path('materials_api', views.materials),
    re_path('^literature_api/(?P<literature_type>[a-z]+)$', views.literature),
]
