from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("filter-category", views.filter_category, name="filter-category"),
    path("listing/<int:id>", views.listing_view, name="listing"),
    path("listing/<int:id>/watchlist-add", views.watchlist_add, name="watchlist-add"),
    path("listing/<int:id>/watchlist-remove", views.watchlist_remove, name="watchlist-remove"),
    path("watchlist", views.watchlist_display, name="watchlist"),
    path("listing/<int:id>/add-comment", views.add_comment, name="add-comment"),
    path("listing/<int:id>/add-bid", views.add_bid, name="add-bid")

]
