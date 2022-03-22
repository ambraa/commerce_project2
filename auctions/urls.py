from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("newbid/<str:product_id>", views.newbid, name="newbid"),
    path("category/<str:category>", views.category, name="category"),
    path("addwatchlist/<str:product_id>", views.addwatchlist, name="addwatchlist"),
    path("<int:product_id>", views.listing, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]