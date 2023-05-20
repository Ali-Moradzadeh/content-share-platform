from django.urls import path
from .views import UserProfileViewSet, UserViewSet
from rest_framework import routers

urlpatterns = [
]

router = routers.SimpleRouter()
router.register("users", UserViewSet)
router.register("profiles", UserProfileViewSet)

urlpatterns += router.urls
