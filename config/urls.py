from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("boxes.urls")),
    path("api/", include("boxes.urls")),
]