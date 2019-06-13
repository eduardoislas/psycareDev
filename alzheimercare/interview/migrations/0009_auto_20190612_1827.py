# Generated by Django 2.2.2 on 2019-06-12 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0008_auto_20190503_1144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='caregiver',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='caregiver',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]