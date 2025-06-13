from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenBlacklistView



urlpatterns = [
    path("admin/", admin.site.urls),

    path('api/accounts/', include('accounts.urls')),
    path('api/actions/', include('actions.urls')),
]
