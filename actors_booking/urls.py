from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("actors/", include("actors.urls")),
]
handler404 = "homepage.views.page_not_found"