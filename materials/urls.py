from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('materials', views.materials, name="materials"),
    path('literature/<str:literature_type>', views.literature, name="literature"),
    path('ipho', views.ipho, name="ipho"),
    path('materials/<int:theme_id>/<str:task_type>', views.material_page, name="material"),

    # API

    path('material/<int:theme_id>/<str:task_type>', views.material, name="task"),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)