from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserActivityLogViewSet

router = DefaultRouter()
router.register(r'activity', UserActivityLogViewSet, basename='activity')

urlpatterns = [
    path('', include(router.urls)),
]
