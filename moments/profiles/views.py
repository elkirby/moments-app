from django.contrib.auth.models import User
from django.views.generic import DetailView


class UserDetailView(DetailView):
    model = User
    slug_field = 'username'
    context_object_name = 'current_user'

