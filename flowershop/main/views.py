from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Flower, Order


def home(request):
    return render(request, 'main/home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})

def catalog(request):
    flowers = Flower.objects.all()
    return render(request, 'main/catalog.html', {'flowers': flowers})

@login_required
def order(request):
    if request.method == 'POST':
        flower_ids = request.POST.getlist('flowers')
        flowers = Flower.objects.filter(id__in=flower_ids)
        order = Order.objects.create(user=request.user)
        order.flowers.set(flowers)
        return redirect('home')
    else:
        flowers = Flower.objects.all()
    return render(request, 'main/order.html', {'flowers': flowers})