from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError
from smart_selects.db_fields import ChainedForeignKey


# Create your models here.


def validar_fecha(fecha_transaccion):
    fecha_actual = date.today()
    anio_contable = fecha_actual.year - 1
    anio_actual = fecha_transaccion.year

    if anio_contable <= anio_actual <= fecha_actual.year:
        return anio_actual
    else:
        raise ValidationError("Digite una fecha valida")


class Clase(models.Model):
    id_clase = models.CharField(primary_key=True, max_length=1)
    nombre_clase = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = 'clase'
        ordering = ["id_clase"]

    def __str__(self):
        return self.id_clase + " - " + self.nombre_clase


class Grupo(models.Model):
    id_grupo = models.CharField(primary_key=True, max_length=2, null=False, blank=False)
    nombre_grupo = models.CharField(max_length=50, null=False, blank=False)
    id_clase = models.ForeignKey(Clase, verbose_name="Clase", on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        db_table = 'grupo'
        ordering = ["id_grupo"]

    def __str__(self):
        return self.id_grupo + " - " + self.nombre_grupo


class Cuenta(models.Model):
    id_cuenta = models.CharField(primary_key=True, max_length=4, null=False, blank=False)
    nombre_cuenta = models.CharField(max_length=50, null=False, blank=False)
    id_grupo = models.ForeignKey(Grupo, verbose_name="Grupo", on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        db_table = 'cuenta'
        ordering = ["id_cuenta"]

    def __str__(self):
        return self.id_cuenta + " - " + self.nombre_cuenta


class SubCuenta(models.Model):
    id_subCuenta = models.CharField(primary_key=True, max_length=7, null=False, blank=False)
    nombre_subCuenta = models.CharField(max_length=50, null=False, blank=False)
    debe = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    haber = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    id_cuenta = models.ForeignKey(Cuenta, verbose_name="Cuenta", on_delete=models.PROTECT, null=False, blank=False)

    class Meta:
        db_table = 'subCuenta'
        ordering = ["id_subCuenta"]

    def __str__(self):
        return self.id_subCuenta + " - " + self.nombre_subCuenta


class TipoTransaccion(models.Model):
    id_tipoTransaccion = models.AutoField(primary_key=True)
    nombre_tipoTransaccion = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        db_table = 'TipoTransaccion'

    def __str__(self):
        return self.nombre_tipoTransaccion


class Partida(models.Model):
    id_partida = models.IntegerField("N° de partida", primary_key=True, null=False, blank=False)
    descripcion_partida = models.CharField("Descripcion", max_length=50, null=True, blank=False)

    class Meta:
        db_table = 'partidas'
        ordering = ["id_partida"]

    def __str__(self):
        return self.id_partida.__str__() + self.descripcion_partida


class Transaccion(models.Model):
    id_transaccion = models.AutoField(primary_key=True, null=False, blank=False)
    id_partida = models.ForeignKey(Partida, on_delete=models.CASCADE, null=False, blank=False)
    fecha_transaccionT = models.DateField("Fecha de Transaccion", null=False, blank=False,
                                          help_text="Consejo: <em>Presione en el calendario</em>.",
                                          validators=[validar_fecha])
    id_clase = models.ForeignKey(Clase, verbose_name="Clase", on_delete=models.PROTECT, null=False, blank=False,
                                 default=1)
    id_grupo = ChainedForeignKey(Grupo, chained_field="id_clase", chained_model_field='id_clase', auto_choose=True,
                                 show_all=False, verbose_name="Grupo", on_delete=models.PROTECT, null=False,
                                 blank=False)
    id_cuenta = ChainedForeignKey(Cuenta, chained_field="id_grupo", chained_model_field='id_grupo', auto_choose=True,
                                  show_all=False, verbose_name="Cuenta", on_delete=models.PROTECT, null=False,
                                  blank=False)
    id_subCuenta = ChainedForeignKey(SubCuenta, chained_field="id_cuenta", chained_model_field='id_cuenta',
                                     auto_choose=True, show_all=False, verbose_name="Sub-Cuenta",
                                     on_delete=models.PROTECT, null=False, blank=False)
    descripcion_transaccionT = models.CharField("Descripcion", max_length=80, null=True, blank=False)
    id_tipoTransaccion = models.ForeignKey(TipoTransaccion, default=1, on_delete=models.PROTECT,
                                           verbose_name="Tipo de Transacción", null=False, blank=False)
    monto = models.DecimalField(null=False, blank=False, validators=[MinValueValidator(0)], max_digits=10,
                                decimal_places=2)

    class Meta:
        db_table = 'transaccion'
        ordering = ["id_transaccion"]

    def __str__(self):
        return self.fecha_transaccionT.__format__(
            '%d/%m/%Y').__str__() + " - " + self.id_subCuenta.id_subCuenta + " - " + self.id_subCuenta.nombre_subCuenta + " - " + self.id_tipoTransaccion.nombre_tipoTransaccion + " - $" + self.monto.__str__()


class Ajuste(models.Model):
    id_ajuste = models.AutoField(primary_key=True, null=False, blank=False)
    fecha_ajuste = models.DateField(auto_now_add=True, null=False, blank=False)
    id_clase = models.ForeignKey(Clase, verbose_name="Clase", on_delete=models.PROTECT, null=False, blank=False,
                                 default=1)
    id_grupo = ChainedForeignKey(Grupo, chained_field="id_clase", chained_model_field='id_clase', auto_choose=True,
                                 show_all=False, verbose_name="Grupo", on_delete=models.PROTECT, null=False,
                                 blank=False)
    id_cuenta = ChainedForeignKey(Cuenta, chained_field="id_grupo", chained_model_field='id_grupo',
                                  auto_choose=True, show_all=False, verbose_name="Cuenta", on_delete=models.PROTECT,
                                  null=False, blank=False)
    id_subCuenta = ChainedForeignKey(SubCuenta, chained_field="id_cuenta", chained_model_field='id_cuenta',
                                     auto_choose=True, show_all=False, verbose_name="Sub-Cuenta",
                                     on_delete=models.PROTECT, null=False, blank=False)
    descripcion_ajuste = models.CharField("Descripcion", max_length=80, null=True, blank=False)
    id_tipoTransaccion = models.ForeignKey(TipoTransaccion, default=1, on_delete=models.PROTECT,
                                           verbose_name="Tipo de Transacción", null=False, blank=False)
    monto = models.DecimalField(null=False, blank=False, validators=[MinValueValidator(0)], max_digits=10,
                                decimal_places=2)

    class Meta:
        db_table = 'ajuste'
        ordering = ["id_ajuste"]

    def __str__(self):
        return self.fecha_ajuste.__str__() + " - " + self.id_subCuenta.id_subCuenta.__str__() + " - " + self.descripcion_ajuste + " - " + self.id_tipoTransaccion.nombre_tipoTransaccion + " - $" + self.monto.__str__()

