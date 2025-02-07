from django.shortcuts import render, redirect
from .forms import PaysForm
from .models import Pays
import requests
from bs4 import BeautifulSoup
import csv

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

def pays_details_view(request, pays):
    
    datas = {
        "population": 0,
        "superficie": 0,
        "langue": "",
        "capitale": "",
        "habitant": ""
    }
    
    url1 = "https://fr.wikipedia.org/wiki/Liste_des_pays_par_population"
    url2 = "https://fr.wikipedia.org/wiki/"+pays
    url3 = "https://fr.wikipedia.org/wiki/Tokyo"

    response1 = requests.get(url2)
    soup1 = BeautifulSoup(response1.content, "html.parser")

    #population
    try:
        population = soup1.findAll(string='Population totale')
        population = population[0].parent.parent.parent
        population = population.findAll("td")
        population = population[0].text
    except:
        population = soup1.findAll(string='Population')
        population = population[0].parent.parent.parent
        population = population.findAll("td")
        population = population[0].text
    datas["population"] = population
    print(population)

    #superficie
    try:
        superficie = soup1.findAll(string='Superficie totale')
        superficie = superficie[0].parent.parent
        superficie = superficie.findAll("td")
        superficie = superficie[0].text
    except:
        superficie = soup1.findAll(string='Superficie')
        superficie = superficie[0].parent.parent
        superficie = superficie.findAll("td")
        print(superficie)
        # superficie = superficie[0].text
    datas["superficie"] = superficie
    print(superficie)

    #langue
    try:
        langue = soup1.findAll(string='Langue officielle')   
        langue = langue[0].parent.parent.parent
        langue = langue.findAll("td")
        langue = langue[0].text
    except:
        langue = soup1.findAll(string='Langues officielles') 
        langue = langue[0].parent.parent.parent
        langue = langue.findAll("td")
        langue = langue[0].text
    # finally:
    #     langue = soup1.findAll(string='Langue') 
    #     langue = langue[0].parent.parent.parent
    #     langue = langue.findAll("td")
    #     langue = langue[0].text
        
    datas["langue"] = langue
    print(langue)

    #capitale
    capitale = soup1.findAll(string='Capitale')
    capitale = capitale[0].parent.parent.parent
    capitale = capitale.findAll("td")
    capitale = capitale[0].text
    datas["capitale"] = capitale
    print(capitale)

    #gentilé
    try:
        habitant = soup1.findAll(string='Gentilé')
        habitant = habitant[0].parent.parent.parent
        habitant = habitant.findAll("td")
        habitant = habitant[0].text
    except:
        habitant = ""
    datas["habitant"] = habitant
    print(habitant)

    return render(request, "app/pays_details.html", {'datas': datas})

