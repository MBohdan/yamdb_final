# Generated by Django 3.1.2 on 2020-10-06 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0006_auto_20201006_0657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='HVSVKNE2YZ', max_length=100, null=True, verbose_name='Код подтверждения'),
        ),
    ]