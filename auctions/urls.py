from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("list", views.createList, name="list"),
    path("create/<str:user>", views.create, name="create"), 
    path("listado/<str:id>", views.listado, name="listado"),
    path("category/<str:cat>", views.category, name="category"),
    path("watchlist-user/<str:user>", views.watchlistUser, name="watchlist-user")  ,
    path("categories", views.categories, name="categories")  ,
    path("watchlist/<str:id>/<str:user>/<str:action>", views.watchlist, name="watchlist") ,   
    path("close-auction/<str:id>", views.closeAuction, name="close-auction")  ,
    path("ofertar/<str:id>", views.ofertar, name="ofertar"),
    path("do-bid/<str:user>/<str:id>", views.creaOferta, name="do-bid"),
    path("comments", views.comments, name="comments")
]
