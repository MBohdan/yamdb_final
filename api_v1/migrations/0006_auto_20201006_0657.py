# Generated by Django 3.1.2 on 2020-10-06 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0005_auto_20201005_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='3KYR7G8484', max_length=100, null=True, verbose_name='Код подтверждения'),
        ),
    ]