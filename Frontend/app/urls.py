from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('subirXML/', views.subirXML, name='subirXML'),
    path('leerArchivoXML/', views.leerArchivoXML, name='leerArchivoXML'),
]


#path('mostrar/', views.mostrar, name='mostrar'),
    #path('subirXML/', views.subirXML, name='subirXML'),