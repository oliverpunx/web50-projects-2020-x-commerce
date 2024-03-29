# Generated by Django 4.2.4 on 2024-01-08 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_comentarios_usuariocreacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentarios',
            name='idProducto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auctions.listado'),
        ),
        migrations.AlterField(
            model_name='listado',
            name='idCategoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auctions.categorias'),
        ),
        migrations.AlterField(
            model_name='ofertas',
            name='idProducto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auctions.listado'),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='idProducto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auctions.listado'),
        ),
    ]
