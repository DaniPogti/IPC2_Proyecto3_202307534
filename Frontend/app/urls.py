from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('subirXML/', views.subirXML, name='subirXML'),
    path('leerArchivoXML/', views.leerArchivoXML, name='leerArchivoXML'),
    path('mandarXML/', views.mandarXML, name='mandarXML'),
    path('Ayuda/', views.Ayuda, name='Ayuda'),
]


#path('mostrar/', views.mostrar, name='mostrar'),
    #path('subirXML/', views.subirXML, name='subirXML'),