from django.urls import include, path
from rest_framework import routers

from rest.views import AlbumViewSet, PhotoViewSet

router = routers.DefaultRouter()
router.register('', AlbumViewSet, basename='user')
router.register('.*/albums', PhotoViewSet, basename='album')

urlpatterns = (
    path('<slug>', include((router.urls, 'rest'))),
)
