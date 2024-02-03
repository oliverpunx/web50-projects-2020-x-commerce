from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from .models import User,Comentarios,Categorias,Listado,Ofertas,Watchlist
from django.db.models import Count


def index(request):
        list= Listado.objects.all()
        offerClosed=Ofertas.objects.filter(estado="F")
        ofertas=Ofertas.objects.all()
        
        return render(request, "auctions/index.html",{
        "listado": list,
        "bidClosed": offerClosed,
        "ofertas": ofertas
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def createList(request):
    categorias=Categorias.objects.all()

    return render(request,"auctions/createList.html",{
        "category": categorias
 })
      
def create(request,user):
    categorias=Categorias.objects.all()
    
    msgError=""
    msgOk=""

    if request.method == "POST":
       title=request.POST["titulo"]
       descrip=request.POST["descripcion"]
       ofertaIni=request.POST["ofertaInicial"]
       
       idProduct=request.POST["idProducto"]
       img=request.POST["imagen"]
       usuario=user
       estadoList="A"

       msgError="No se pudo crear Lista"
       msgOk="Lista Creada"
       
       try:
            crear = Listado.objects.create(idProducto=idProduct,titulo=title, descripcion= descrip, ofertaInicial= ofertaIni, imagen= img,idCategoria=Categorias(idCategoria=request.POST["category"]),usuarioCreacion=usuario,estado=estadoList)
            crear.save()
            msgError=""

       except Exception as er:
              error=type(er).__name__

              msgOk=""
              msgError="Error al crear nueva lista: "+error
                
              return render(request,"auctions/createList.html",{
                    "error": msgError,
                    "creado": msgOk,
                    "selected": "",
                    "category": categorias
              })             

       return render(request,"auctions/createList.html",{
            "error": msgError,
            "creado": msgOk,
            "selected": "selected",
            "category": categorias
        })          

    return render(request,"auctions/createList.html",{
        "error": msgError,
        "creado": msgOk,
        "selected": "selected",
        "category": categorias
    })  

def listado(request,id):
    if request.method=="GET":
        idProduct=id;   

        try:
            item=Listado.objects.filter(idProducto=idProduct)
            comments=Comentarios.objects.filter(idProducto=idProduct).order_by('-fechaCreacion')
            category=Categorias.objects.filter(idCategoria=item[0].idCategoria.idCategoria)
            ofertas=Ofertas.objects.filter(idProducto=idProduct).order_by('-valorOferta').first
            watchlist=Watchlist.objects.filter(idProducto=idProduct)

        except Exception as er:
               error=type(er).__name__

               if error=="DoesNotExist":
                    return render(request,"auctions/listado.html",{
                        "listado": item,
                        "comentarios": comments,
                        "idProducto": id,
                        "categoria": category,
                        "watchlist": watchlist,
                        "ofertas": ofertas
                    })                    
               else:
                    return render(request,"auctions/index.html",{
                        "errorW": "Request cant be realized. "+error
                    })
    
        return render(request,"auctions/listado.html",{
            "listado": item,
            "comentarios": comments,
            "idProducto": id,
            "categoria": category,
            "watchlist": watchlist,
            "ofertas": ofertas
        })
    else:
        return render(request,"auctions/index.html")
    
def watchlist(request,id,user,action):
    if request.method=="GET" and action=="add":
       idProduct=id;   

       try:
            item=Listado.objects.filter(idProducto=idProduct)

            if ( item ):
                #revisa si ya existe en la lista
                try:
                    buscar = Watchlist.objects.filter(idProducto=idProduct,usuarioCreacion=user)
                
                except Exception as er:
                       error=type(er).__name__

                       return render(request,"auctions/index.html",{
                                    "errorW": "Item cant be founded in the watchlist. "+error
                       })                        

                if (buscar):
                   return render(request,"auctions/index.html",{
                        "errorW": "Item cant be added  in the watchlist. Item is already added."
                   })                    
                else:
                   try:
                        crear = Watchlist.objects.create(idProducto=Listado(idProducto=idProduct),usuarioCreacion=user)
                        
                        try:
                             miLista = Watchlist.objects.filter(usuarioCreacion=user)
                        
                        except Exception as er:
                               error=type(er).__name__

                               return render(request,"auctions/index.html",{
                                    "errorW": "0.- Item cant be added in the watchlist. "+error
                               })                                 

                        return render(request,"auctions/index.html",{
                            "msgOK": "Added to Watchlist",
                            "miListado": miLista
                        })
                   except Exception as er:
                          error=type(er).__name__

                          return render(request,"auctions/index.html",{
                            "errorW": "1.- Item cant be added in the watchlist. "+error
                          })  
                

       except Exception as er:
              error=type(er).__name__

              return render(request,"auctions/index.html",{
                 "errorW": "2.- Item cant be added in the watchlist. "+error
              })
            
       return render(request,"auctions/index.html",{
                    "errorW": "3.- Item cant be added in the watchlist."
                })
    elif request.method=="GET" and action=="remove":
         try:
             quitar=Watchlist.objects.filter(idProducto=id,usuarioCreacion=user)
             contRecords=quitar.count()
             
             if contRecords>0 :
                eliminar=quitar.delete()
                
                if eliminar:
                   miLista = Watchlist.objects.filter(usuarioCreacion=user)
                   
                   return render(request,"auctions/index.html",{
                            "msgOK": "Removed out to the Watchlist.",
                            "miListado": miLista
                        })  
                else:
                    return render(request,"auctions/index.html",{
                    "errorW": "4.- Item cant be removed out to the watchlist. "
                })    
             else:
                return render(request,"auctions/index.html",{
                    "errorW": "5.- Item cant be removed out to the watchlist. Tot. Records: "+str(contRecords)
                })      
                             
         except Exception as er:
                error=type(er).__name__

                return render(request,"auctions/index.html",{
                    "errorW": "6.- Item cant be removed out to the watchlist. "+error
                })                        
         
    else:
        return render(request,"auctions/index.html",{
            "errorW": "Item cant be added  in the watchlist. No valid Id."
        })     

def watchlistUser(request,user): 
    if request.method=="GET":
       lista=Watchlist.objects.filter(usuarioCreacion=user)

       return render(request,"auctions/watchlist-user.html",{
        "miListado": lista
       }) 
        
def closeAuction(request,id):
    if request.method=="GET":
       try:
            oferta=Ofertas.objects.filter(idProducto=id,estado='A').order_by("-valorOferta")
                   
            try:
                    try:
                        inactivar=Listado.objects.filter(idProducto=id).update(estado='I')
                        secuencia=""

                        for winner in oferta:
                            secuencia=winner.idSecuencia
                            break
                        
                        try: 
                            #offerWinner=oferta.objects.update(estado='F')#Estado F Oferta declarada ganadora
                            if secuencia:
                               offerWinner=Ofertas.objects.filter(idSecuencia=secuencia).update(estado='F')
                            
                            return render(request,"auctions/index.html",{
                            "maxOferta": oferta,
                            "msgOK": "Auction was closed successfully."
                            })                             

                        except Exception as er:
                               error=type(er).__name__

                               return render(request,"auctions/index.html",{
                                    "errorW": "Offer cant be declared as winner. "+error
                               })                                 
                    
                    except Exception as er:
                           error=type(er).__name__

                           return render(request,"auctions/index.html",{
                            "errorW": "Auction cant be desactived. "+error
                           })                          
                
            except Exception as er:
                      error=type(er).__name__

                      return render(request,"auctions/index.html",{
                       "errorW": "1.- Auction cant be closed. "+error
                      })  
                            
               
       except Exception as er:
              error=type(er).__name__
              
              if error=="DoesNotExist":
                 try:
                        inactivar=Listado.objects.filter(idProducto=id).update(estado='I')

                        return render(request,"auctions/index.html",{
                                    "errorW": "Auction was closed successfully."
                        })                           
                
                 except Exception as er:
                        error=type(er).__name__

                        return render(request,"auctions/index.html",{
                        "errorW": "4.- Auction cant be closed."+error
                 })    
              else:
                 return render(request,"auctions/index.html",{
                            "errorW": "3.- Auction cant be closed. "+error
                 })                    

def ofertar(request,id):
       producto=Listado.objects.filter(idProducto=id)
       
       try:
            if producto:
                return render(request,"auctions/ofertar.html",{
                        "Producto": producto
                    })
            else:
                return HttpResponseRedirect("/")      
        
       except Exception as er:     
              error=type(er).__name__
              return render(request,"auctions/index.html",{
              "errorW": "Item do not exist. Id: "+id+" "+error
              })              

def creaOferta(request,user,id):
    if request.method=="POST":
       maxOferta=0
       
       ofertas=Ofertas.objects.filter(idProducto=id,estado='A').order_by("-valorOferta")
       
       if ofertas:
          maxOferta=ofertas.first().valorOferta
       else:
          maxOferta=0
       
       miOferta=float(request.POST["oferta"])
       maxOferta=float(maxOferta)

       if maxOferta==0 or maxOferta<=miOferta:
            try:
                    now=datetime.now()
                    oferta=Ofertas.objects.create(idProducto=Listado(idProducto=id),fechaInicio=now,valorOferta=miOferta,usuarioOferta=user,estado="A")
                    
                    if oferta:
                       return render(request,"auctions/ofertar.html",{
                            "msgOK": "Bid for item with ID # "+id+" was created successfully. Bid: $ "+str(miOferta)
                       })                     
                    else:
                       return render(request,"auctions/ofertar.html",{
                            "error": "1.- Bid was not created."
                       })                         
                
            except Exception as er:            
                    errorOf=type(er).__name__
                    return render(request,"auctions/ofertar.html",{
                            "error": "2.- Bid was not created."+errorOf  
                    })    
       else:
           if maxOferta>miOferta:
              return render(request,"auctions/ofertar.html",{
                            "error": "3.- Bid was not created. Bid must be greater than "+str(maxOferta)
              })                
    else:   
        return render(request,"auctions/ofertar.html",{
                     "error": "4.- Bid was not created."
        })             
       
def comments(request):
    if request.method=="POST":
       try:
            comentario=Comentarios.objects.create(idProducto=Listado(idProducto=request.POST["idProducto"]), mensaje=request.POST["comment"], usuarioCreacion=request.POST["userComment"], estado='A')
            
            item=Listado.objects.filter(idProducto=request.POST["idProducto"])
            comments=Comentarios.objects.filter(idProducto=request.POST["idProducto"]).order_by('-fechaCreacion')
            category=Categorias.objects.filter(idCategoria=item[0].idCategoria.idCategoria)
            ofertas=Ofertas.objects.filter(idProducto=request.POST["idProducto"]).order_by('-valorOferta').first
            watchlist=Watchlist.objects.filter(idProducto=request.POST["idProducto"])

            return HttpResponseRedirect(reverse("listado/"+request.POST["idProducto"]),{
                        "idProducto": request.POST["idProducto"],
                        "comentarios": comments,
                        "idProducto": id,
                        "categoria": category,
                        "watchlist": watchlist,
                        "ofertas": ofertas
              })

       except Exception as er:
              error=type(er).__name__

              return render(request,"auctions/listado.html",{
                        "listado": item,
                        "comentarios": comments,
                        "idProducto": id,
                        "categoria": category,
                        "watchlist": watchlist,
                        "ofertas": ofertas,                   
                        "error": "Comment was not created."+error
              })             

def categories(request):
    categorias=Categorias.objects.all().order_by("descripcion")
  
    return render(request,"auctions/categories.html",{
         "categorias": categorias
    }) 

def category(request,cat):
    if request.method=="GET":
       try:
            categoria=Categorias.objects.filter(idCategoria=cat)
            list= Listado.objects.filter(idCategoria=Categorias(idCategoria=cat))
            offerClosed=Ofertas.objects.filter(estado="F")
            ofertas=Ofertas.objects.all()   

            if categoria: 
                return render(request,"auctions/category.html",{
                    "listado": list,
                    "bidClosed": offerClosed,
                    "ofertas": ofertas,
                    "categoria": categoria
                })  
            else:
                return HttpResponseRedirect(reverse("categories"))
         
       except Exception as er:
            return HttpResponseRedirect(reverse("categories"))
                     
              