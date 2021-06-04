from django.urls import path

from . import views

urlpatterns = [

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("", views.activelistings, name="activelistings"),
    path("home/<str:title>", views.entry, name="entry"),
    path("watchlist/", views.watchlist, name='watchlist'),
    path("add/<str:title>", views.add, name='add'),
    path("remove/<str:title>", views.remove, name='remove'),
    path("edit/<str:title>", views.edit, name='edit'),
    path("addcomment/<str:title>", views.addcomment, name='addcomment'),
    path("addbid/<str:title>", views.bid, name='addbid'),
    path("closebid/<str:title>", views.close_bid, name='closebid'),
    path("categories", views.categories, name="categories"),
    path("categories/<str:title>", views.category, name="category"),
path("test", views.test, name="test"),
]
