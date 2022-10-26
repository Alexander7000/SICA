from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Clase)

admin.site.register(Grupo)

admin.site.register(Cuenta)

admin.site.register(SubCuenta)

admin.site.register(TipoTransaccion)

admin.site.register(Partida)

admin.site.register(Transaccion)

admin.site.register(Producto)

admin.site.register(OrdendeProduccion)

admin.site.register(ManodeObra)

admin.site.register(Prorrateo)

admin.site.register(CostosIndirectos)

admin.site.register(Ajuste)