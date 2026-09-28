from django.urls import path

from .views import ProductListView, RecommendBoxView, home


urlpatterns = [
    path("", home, name="home"),
    path("products/", ProductListView.as_view(), name="products"),
    path("recommend-box/", RecommendBoxView.as_view(), name="recommend-box"),
]