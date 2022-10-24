from django.urls import path, include
from .views import *

# enlaces para mostrar las vistas (URLS)

urlpatternsTransaccion = [
    path('ver_transacciones', transacciones, name='transacciones'),
    path('crear_transaccion', crear_transaccion, name='crear_transaccion'),
    path('editar/<int:id_transaccion>', editar_transaccion, name='editar_transaccion'),
    path('eliminar/<int:id_transaccion>', eliminar_transaccion, name='eliminar_transaccion'),
    path('transaccion_IVA', transaccion_IVA, name='transaccion_IVA'),
    path('calculo_IVA/<int:id_transaccion>', calculo_IVA, name='calculo_IVA'),

]

urlpatterns = [
    path('', inicio, name='inicio'),
    path('catalogo', catalogo, name='catalogo'),

    path('partidas', partidas, name='partidas'),
    path('partidas/crear_partida', crear_partida, name='crear_partida'),
    path('partidas/editar/<int:id_partida>', editar_partida, name='editar_partida'),
    path('partidas/eliminar/<int:id_partida>', eliminar_partida, name='eliminar_partida'),

    path('transacciones/<int:id_partida>/', include(urlpatternsTransaccion)),
    path('HojadeTrabajo', HojadeTrabajo, name='HojadeTrabajo'),
    path('HojadeTrabajo/BalanceGeneral', BalanceGeneral, name='BalanceGeneral'),
    path('ContabilidadCostos', ContabilidadCostos, name='ContabilidadCostos'),
    path('ContabilidadCostos/OrdenProduccion.html', OrdenProduccion, name='OrdenProduccion'),
    path('ContabilidadCostos/verOrdenes.html', verOrdenes, name='verOrdenes'),
    path('ContabilidadCostos/ManodeObra.html/<int:id_OrdendeProduccion>', ManodeObra, name='ManodeObra'),
]