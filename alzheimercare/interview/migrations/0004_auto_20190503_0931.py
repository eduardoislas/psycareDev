# Generated by Django 2.1.7 on 2019-05-03 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0003_auto_20190503_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caregiver',
            name='can_locate',
            field=models.CharField(choices=[('si', 'Si'), ('no', 'No')], max_length=2),
        ),
        migrations.AlterField(
            model_name='caregiver',
            name='is_helped',
            field=models.CharField(choices=[('si', 'Si'), ('no', 'No')], max_length=2),
        ),
        migrations.AlterField(
            model_name='caregiver',
            name='is_regular',
            field=models.CharField(choices=[('si', 'Si'), ('no', 'No')], max_length=2),
        ),
        migrations.AlterField(
            model_name='caregiver',
            name='leave_caregiver',
            field=models.CharField(choices=[('si', 'Si'), ('no', 'No')], max_length=2),
        ),
        migrations.AlterField(
            model_name='context',
            name='when_know',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='process',
            name='atention',
            field=models.CharField(choices=[('1', 'Temprana'), ('2', 'Intermedia'), ('3', 'Tardía')], max_length=2),
        ),
        migrations.AlterField(
            model_name='process',
            name='reunion',
            field=models.CharField(choices=[('si', 'Si'), ('no', 'No')], max_length=2),
        ),
        migrations.AlterField(
            model_name='process',
            name='talk',
            field=models.CharField(choices=[('si', 'Si'), ('no', 'No')], max_length=2),
        ),
        migrations.AlterField(
            model_name='process',
            name='therapy',
            field=models.CharField(choices=[('si', 'Si'), ('no', 'No')], max_length=2),
        ),
    ]
