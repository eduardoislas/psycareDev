# Generated by Django 2.1.7 on 2019-04-04 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruments', '0002_auto_20190404_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrument',
            name='instrucciones',
            field=models.TextField(blank=True, max_length=400, null=True),
        ),
    ]
