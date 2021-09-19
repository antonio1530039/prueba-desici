from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.inicio, name='inicio'),
    path("contacto/nuevo/", views.contacto_nuevo, name='contacto_nuevo'),
    path("contacto/<int:pk>/editar/", views.contacto_editar, name='contacto_editar'),
    path("contacto/<int:pk>/eliminar/", views.contacto_eliminar, name='contacto_eliminar'),
    path("telefono/<int:pk>/eliminar/", views.telefono_eliminar, name='telefono_eliminar')
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)