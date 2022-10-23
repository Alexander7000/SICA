from django.urls import path
from .views import *

# enlaces para mostrar las vistas (URLS)
# path(para pasar parametros, llamado a las  views, nombre de la url)

urlpatterns = [
    path('signup/', VistaRegistrarse.as_view(), name="signup"),
    path('logout/', salir, name='logout'),
    path('login/', entrar, name='login'),
    path('', entrar, name='login2'),
]
