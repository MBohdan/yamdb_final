# Generated by Django 3.1.2 on 2020-10-13 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0014_auto_20201013_0620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='Псевдоним'),
        ),
    ]