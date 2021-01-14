from django.contrib.auth.forms import AuthenticationForm


def get_login_form(request):
    return dict(login_nav_form=AuthenticationForm(request))
