from django.urls import path

from .views import UserDetailView, get_album

urlpatterns = [
    path('', UserDetailView.as_view(), name='user-detail'),
    path('albums/<name>', get_album, name='album-detail'),

]
