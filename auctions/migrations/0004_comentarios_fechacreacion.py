# Generated by Django 4.2.4 on 2024-01-08 17:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_ofertas_fechainicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentarios',
            name='fechaCreacion',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
