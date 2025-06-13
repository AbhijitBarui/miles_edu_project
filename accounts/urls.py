from django.urls import path
from .views import CustomLoginView, CustomLogoutView, UserRegistrationView

urlpatterns = [
    path("custom-login/", CustomLoginView.as_view(), name="custom_login"),
    path("custom-logout/", CustomLogoutView.as_view(), name="custom_logout"),
    path('register/', UserRegistrationView.as_view(), name='register'),
]
