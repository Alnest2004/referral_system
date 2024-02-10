from django.contrib import admin
from django.urls import path, include

from referral_system.yasg import urlpatterns as doc_urls

urlpatterns = [
    path("api/", include("main.urls")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
]

urlpatterns += doc_urls
