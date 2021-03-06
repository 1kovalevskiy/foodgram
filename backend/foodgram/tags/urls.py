from django.urls import include, path
from rest_framework.routers import SimpleRouter

from tags.views import TagViewSet


app_name = 'tag'

router = SimpleRouter()
router.register(r'tags', TagViewSet, basename='tags')

urlpatterns = [
    path(r'', include(router.urls)),
]
