from django.contrib.auth.models import AbstractUser
from django.shortcuts import render
from django.db import models


class User(AbstractUser):
    pass

class Categorias(models.Model):
      idCategoria = models.IntegerField(primary_key=True )
      descripcion = models.CharField(max_length=120)
      imagen = models.CharField(max_length=1000)
      
      def __str__(self):
          return self.descripcion
      

class Listado(models.Model):
      idProducto = models.CharField(max_length=50,primary_key=True )
      titulo = models.CharField(max_length=200)
      descripcion = models.CharField(max_length=500)
      fechaCreacion = models.DateField(auto_now_add=True)
      usuarioCreacion =models.CharField(max_length=30)
      ofertaInicial =models.DecimalField(max_digits=11, decimal_places=2)
      imagen = models.CharField(max_length=1000)
      idCategoria = models.ForeignKey(Categorias,related_name='listadoCategoria', on_delete=models.PROTECT)
      estado = models.CharField(max_length=1)

class Watchlist(models.Model):
      idSecuencia = models.AutoField(primary_key=True,auto_created=True,serialize=False,verbose_name='ID')
      idProducto = models.ForeignKey(Listado,related_name='watchlistListado',on_delete=models.PROTECT)
      fechaCreacion = models.DateTimeField(auto_now_add=True )
      usuarioCreacion = models.CharField(max_length=30)    

class Ofertas(models.Model):
      idSecuencia = models.AutoField(primary_key=True,auto_created=True,serialize=False,verbose_name='ID')
      idProducto = models.ForeignKey(Listado,related_name='ofertasListado',on_delete=models.PROTECT)
      fechaInicio = models.DateTimeField(auto_now_add=True)
      valorOferta = models.DecimalField(max_digits=11, decimal_places=2)
      usuarioOferta = models.CharField(max_length=30)
      estado = models.CharField(max_length=1)   

      def retornaOferta(self,id):
          return self.objects.filter(idProducto=id).order_by("-valorOferta").order_by("-fechaInicio") .first
      
      def __str__(self):
         return str(self.idSecuencia)+"/"+str(self.idProducto.titulo)+"/"+str(self.valorOferta)

class Comentarios(models.Model):
      idSecuencia = models.AutoField(primary_key=True,auto_created=True,serialize=False,verbose_name='ID')
      idProducto = models.ForeignKey(Listado,related_name='comentariosListado',on_delete=models.PROTECT)
      mensaje = models.CharField(max_length=500)
      fechaCreacion = models.DateTimeField(auto_now_add=True)
      usuarioCreacion = models.CharField(max_length=30)
      estado =models.CharField(max_length=1)    

          
