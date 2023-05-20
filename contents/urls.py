from rest_framework import routers
from .views import PostViewSet, CommentViewSet


urlpatterns = [
]

router = routers.SimpleRouter()
router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)

urlpatterns += router.urls