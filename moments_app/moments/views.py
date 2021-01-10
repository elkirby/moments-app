from django.shortcuts import render


def index(request):
    template_name = 'splash' if not request.user.is_authenticated else 'welcome'
    return render(request, f'{template_name}.html', {})
