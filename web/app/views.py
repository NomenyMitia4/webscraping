from django.shortcuts import render, redirect
from .forms import PaysForm
from .models import Pays

# Create your views here.

def home_view(request):
    return render(request, 'app/home.html')

def pays_create_view(request):
    form = PaysForm()
    if request.method == 'POST':
        form = PaysForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pays_list')
    
    return render(request, 'app/pays_form.html', {'form': form})

def pays_list_view(request):
    pays = Pays.objects.all()
    return render(request, 'app/pays_list.html', {'pays':pays})

