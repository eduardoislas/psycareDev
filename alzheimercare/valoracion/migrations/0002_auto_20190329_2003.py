# Generated by Django 2.1.7 on 2019-03-29 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('valoracion', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='valoracion',
            old_name='fecha_inicio',
            new_name='begin_date',
        ),
        migrations.RenameField(
            model_name='valoracion',
            old_name='fecha_final',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='valoracion',
            old_name='nombre',
            new_name='name',
        ),
    ]
