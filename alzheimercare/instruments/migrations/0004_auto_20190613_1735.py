# Generated by Django 2.2.2 on 2019-06-13 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruments', '0003_instrumentrank'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrumentrank',
            name='is_active',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='instrumentrank',
            name='severity',
            field=models.IntegerField(null=True),
        ),
    ]
