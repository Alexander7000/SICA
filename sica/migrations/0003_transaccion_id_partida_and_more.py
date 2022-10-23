# Generated by Django 4.1.2 on 2022-10-22 02:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sica', '0002_partida'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaccion',
            name='id_partida',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sica.partida'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='partida',
            name='descripcion_partida',
            field=models.CharField(max_length=50, null=True, verbose_name='Descripcion'),
        ),
        migrations.AlterField(
            model_name='transaccion',
            name='id_transaccion',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
