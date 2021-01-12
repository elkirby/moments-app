from django.contrib.auth import authenticate, forms, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def index(request):
    template_name = 'splash' if not request.user.is_authenticated else 'welcome'
    return render(request, f'{template_name}.html', {})


def sign_up(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Home'))

    elif request.method == 'POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('Home'))
    else:
        form = forms.UserCreationForm()
    return render(request, 'sign-up.html', {'signup_form': form})


def user_login(request):
    form = AuthenticationForm(request=request)
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Home'))
    elif request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('Home'))

    return render(request, 'login.html', {'login_form': form})
