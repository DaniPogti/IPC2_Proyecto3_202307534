from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/ConsultarDatos', views.mostrar, name='mostrar'),
    path('/subirXML', views.subirXML, name='subirXML'),
    
]
