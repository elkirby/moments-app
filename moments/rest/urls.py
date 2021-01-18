from django.urls import include, path
from rest_framework import routers

from rest.views import AlbumViewSet

router = routers.DefaultRouter()
router.register('', AlbumViewSet, basename='album')

urlpatterns = (
    path('<slug>', include((router.urls, 'rest'))),
)
