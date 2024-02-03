from django.contrib import admin
from .models import Categorias,Ofertas,Listado,Comentarios,Watchlist

# Register your models here.

admin.site.register(Categorias)
admin.site.register(Ofertas)
admin.site.register(Listado)
admin.site.register(Comentarios)
admin.site.register(Watchlist)
