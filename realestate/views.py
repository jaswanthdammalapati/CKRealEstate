from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .models import Event, Property


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


def omaha_events(request):
    events = Event.objects.all()
    return render(request, 'omaha_events.html', {'events': events})


def property_listings(request):
    properties = Property.objects.all()
    return render(request, 'property_listings.html', {'properties': properties})


def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    return render(request, 'property_detail.html', {'property': property})
