# Generated by Django 3.1.2 on 2020-10-06 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0007_auto_20201006_0739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='TYKVCWOCWQ', max_length=100, null=True, verbose_name='Код подтверждения'),
        ),
    ]
