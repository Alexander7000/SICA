from decimal import Decimal


from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

@login_required
def inicio(request):
    return render(request, 'paginas/inicio.html')


@login_required
def catalogo(request):
    clases = Clase.objects.all()
    grupos = Grupo.objects.all()
    cuentas = Cuenta.objects.all()
    subCuentas = SubCuenta.objects.all()

    return render(request, 'catalogo/index.html', {'clases': clases, 'grupos': grupos, 'cuentas': cuentas, 'subCuentas': subCuentas})


@login_required
def partidas(request):
    partidas = Partida.objects.all()

    return render(request, 'partidas/index.html', {'partidas': partidas})


@login_required
def crear_partida(request):
    formulario = PartidaForm(request.POST or None)

    if formulario.is_valid():
        partida = formulario.save()

        return redirect('transacciones', partida.id_partida)

    return render(request, 'partidas/crear.html', {'formulario': formulario})


@login_required
def editar_partida(request, id_partida):
    partida = Partida.objects.get(id_partida=id_partida)
    formulario = PartidaForm(request.POST or None, instance=partida)

    if formulario.is_valid() and request.POST:
        formulario.save()

        messages.success(request, "Se edito exitosamente!")

        return redirect('partidas')

    return render(request, 'partidas/editar.html', {'formulario': formulario})


@login_required
def eliminar_partida(request, id_partida):
    partida = Partida.objects.get(id_partida=id_partida)
    temp = partida.id_partida.__str__()
    partida.delete()
    messages.success(request, "Se ha eliminado la partida N°: " + temp)

    return redirect('partidas')


@login_required
def transacciones(request, id_partida):
    transacciones = Transaccion.objects.filter(id_partida=id_partida)

    suma_debe = 0
    suma_haber = 0

    for transaccion in transacciones:
        if transaccion.id_tipoTransaccion.id_tipoTransaccion == 1:
            suma_debe += transaccion.monto

        if transaccion.id_tipoTransaccion.id_tipoTransaccion == 2:
            suma_haber += transaccion.monto

    diferencia = abs(suma_debe-suma_haber)

    return render(request, 'transacciones/index.html', {'transacciones': transacciones,
                                                        'id_partida': id_partida,
                                                        'suma_debe': suma_debe,
                                                        'suma_haber': suma_haber,
                                                        'diferencia': diferencia})


@login_required
def crear_transaccion(request, id_partida):
    formulario = TransaccionForm(request.POST or None)

    if formulario.is_valid():
        transaccion = formulario.save(commit=False)
        partida = Partida.objects.get(id_partida=id_partida)

        transaccion.id_partida = partida

        transaccion.save()

        return redirect('transacciones', id_partida)

    return render(request, 'transacciones/crear.html', {'formulario': formulario, 'id_partida': id_partida})

@login_required
def editar_transaccion(request, id_partida, id_transaccion):
    transaccion = Transaccion.objects.get(id_transaccion=id_transaccion)
    formulario = TransaccionForm(request.POST or None, instance=transaccion)

    #cambia el formato para poderse presentar
    fechaTransaccion = transaccion.fecha_transaccionT
    fechaTransaccion.__format__('%Y/%m/%d')

    formulario.initial['fecha_transaccionT'] = fechaTransaccion.__str__()

    if formulario.is_valid() and request.POST:
        formulario.save()

        messages.success(request, "Se almacenaron los cambios exitosamente!")

        return redirect('transacciones', id_partida)

    return render(request, 'transacciones/editar.html', {'formulario': formulario, 'id_partida': id_partida})


@login_required
def eliminar_transaccion(request, id_partida, id_transaccion):
    transaccion = Transaccion.objects.get(id_transaccion=id_transaccion)
    temp = transaccion.fecha_transaccionT.__str__()
    transaccion.delete()
    messages.success(request, "Se ha eliminado la transaccion con fecha: " + temp)

    return redirect('transacciones', id_partida)

@login_required
def transaccion_IVA(request, id_partida):
    formulario = TransaccionIVAForm(request.POST or None)

    formulario.fields['transaccion_iva'].queryset = Transaccion.objects.filter(id_partida=id_partida).exclude(Q(id_subCuenta="1106.01") | Q(id_subCuenta="2105.01"))

    if formulario.is_valid() and request.POST:
        transaccion = formulario.cleaned_data['transaccion_iva']

        return redirect('calculo_IVA', id_partida, transaccion.id_transaccion)

    return render(request, 'transacciones/transaccion_IVA.html', {'formulario': formulario, 'id_partida': id_partida})


@login_required
def calculo_IVA(request, id_partida, id_transaccion):
    # objetos de los que depende la nueva transaccion IVA
    transaccion_iva = Transaccion.objects.get(id_transaccion=id_transaccion)
    partida = Partida.objects.get(id_partida=id_partida)

    # se crea una nueva transaccion
    transaccionNueva = Transaccion()

    # se procede a llenar los campos de la nueva transaccion
    transaccionNueva.fecha_transaccionT = transaccion_iva.fecha_transaccionT
    transaccionNueva.monto = round(transaccion_iva.monto * Decimal(0.13), 2)
    transaccionNueva.id_partida = partida

    # se crea el formulario con algunos campos ya llenos
    formulario = CalculoIVAForm(request.POST or None, instance=transaccionNueva)

    # cambia el formato para poderse presentar
    fechaFormato = transaccionNueva.fecha_transaccionT
    fechaFormato.__format__('%Y/%m/%d')

    # se definen algunos valores del formulario
    formulario.initial['fecha_transaccionT'] = fechaFormato.__str__()
    formulario.fields['subCuenta_id'].queryset = SubCuenta.objects.filter(Q(id_subCuenta="1106.01") | Q(id_subCuenta="2105.01"))

    if formulario.is_valid() and request.POST:
        # asignamos el objeto subCuenta de la transaccion a una variable
        id_subCuenta = formulario.cleaned_data['subCuenta_id']

        # guardamos el objeto transaccion que viene del formulario (sin meterlo a la DB)
        transaccion = formulario.save(commit=False)

        # se introduce el objeto sub cuenta recien almacenado por el formulario, al objeto trnasaccion
        transaccion.id_subCuenta = SubCuenta.objects.get(id_subCuenta=id_subCuenta.id_subCuenta)

        # id de sub-cuenta en forma de texto, servira para sacar la clase, grupo y cuenta
        id_subCuentaTexto = transaccion.id_subCuenta.id_subCuenta

        # agregamos los id que faltan
        transaccion.id_clase = Clase.objects.get(id_clase=id_subCuentaTexto[0:1])
        transaccion.id_grupo = Grupo.objects.get(id_grupo=id_subCuentaTexto[0:2])
        transaccion.id_cuenta = Cuenta.objects.get(id_cuenta=id_subCuentaTexto[0:4])

        transaccion.save()

        return redirect('transacciones', id_partida)

    return render(request, 'transacciones/calculo_IVA.html', {'formulario': formulario, 'id_partida': id_partida})


@login_required
def HojadeTrabajo(request):

    return render(request, 'HojadeTrabajo/index.html')
@login_required
def BalanceGeneral(request):
    transacciones = Transaccion.objects.all()

    suma_debe = 0
    suma_haber = 0

    for transaccion in transacciones:
        if transaccion.id_tipoTransaccion.id_tipoTransaccion == 1:
            suma_debe += transaccion.monto

        if transaccion.id_tipoTransaccion.id_tipoTransaccion == 2:
            suma_haber += transaccion.monto

    diferencia = abs(suma_debe-suma_haber)

    return render(request, 'HojadeTrabajo/BalanceGeneral.html', {'transacciones': transacciones,

                                                        'suma_debe': suma_debe,
                                                        'suma_haber': suma_haber,
                                                        'diferencia': diferencia})
@login_required
def ContabilidadCostos(request):

    return render(request, 'ContabilidadCostos/index.html')

@login_required
def OrdenProduccion(request):
    formulario = OrdendeProduccionForm(request.POST or None)

    if formulario.is_valid():
        produccion = formulario.save(commit=False)

        produccion.save()

        return redirect('ManodeObra',produccion.id_OrdendeProduccion)

    return render(request, 'ContabilidadCostos/OrdenProduccion.html', {'formulario': formulario})


@login_required
def verOrdenes(request):
    ordenes = OrdendeProduccion.objects.all()
    return render(request, 'ContabilidadCostos/verOrdenes.html', {'ordenes': ordenes})

@login_required
def ManodeObraVista(request,id_OrdendeProduccion):
    formulario = ManodeObraForm(request.POST or None)

    orden = OrdendeProduccion.objects.get(id_OrdendeProduccion=id_OrdendeProduccion)
    if formulario.is_valid():

        manoObra = formulario.save(commit=False)
        manoObra.id_OrdendeProduccion=orden
        manoObra.costo = manoObra.horas_manodeObra * manoObra.salario_manodeObra
        manoObra.save()

        return redirect('inicio')

    return render(request, 'ContabilidadCostos/ManodeObra.html', {'formulario': formulario})

@login_required
def Prorrateo(request,id_OrdendeProduccion):
    formulario = ProrrateoForm(request.POST or None)

    orden = OrdendeProduccion.objects.get(id_OrdendeProduccion=id_OrdendeProduccion)
    if formulario.is_valid():

        prorrateo = formulario.save(commit=False)
        prorrateo.id_OrdendeProduccion=orden
        prorrateo.totalCIF = prorrateo.manodeObraIndirecta+\
                          prorrateo.alquiler+\
                          prorrateo.segurosEquipo+\
                          prorrateo.depreciacion+\
                          prorrateo.energia+\
                          prorrateo.amortizacion+\
                          prorrateo.otrosGastos
        prorrateo.tasapredeterminadaCIF = prorrateo.totalCIF/prorrateo.aplicacionHMOD
        prorrateo.save()

        return redirect('inicio')

    return render(request, 'ContabilidadCostos/Prorrateo.html', {'formulario': formulario})

@login_required
def verManodeObra(request):
    obras = ManodeObra.objects.all()
    return render(request, 'ContabilidadCostos/verManodeObra.html',{'obras' : obras})
