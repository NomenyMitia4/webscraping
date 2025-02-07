from django.shortcuts import render, redirect
from .forms import PaysForm
from .models import Pays
import requests
from bs4 import BeautifulSoup
import csv
import folium
from folium import plugins
from translate import Translator
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


def create_map(latitude, longitude, zoom_start=1, loc=""):
    """
    Create an interactive map with a custom marker at specified coordinates.
    
    Parameters:
    latitude (float): Latitude of the location
    longitude (float): Longitude of the location
    zoom_start (int): Initial zoom level of the map (default: 12)
    
    Returns:
    folium.Map: Interactive map object
    """
    # Create a map centered at the specified location
    m = folium.Map(location=[latitude, longitude], 
                   zoom_start=6,
                   tiles='OpenStreetMap')
    
    # Add a marker with a popup
    folium.Marker(
        [latitude, longitude],
        popup=loc,
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    # Add a circle around the marker
    folium.Circle(
        radius=1000,  # 1000 meters radius
        location=[latitude, longitude],
        color='crimson',
        fill=True,
    ).add_to(m)
    
    # Add fullscreen button
    plugins.Fullscreen().add_to(m)
    
    # Add location finder
    plugins.LocateControl().add_to(m)
    
    return m


def pays_details_view(request, pays):
    
    datas = {
        "pays": "",
        "population": 0,
        "superficie": 0,
        "langue": "",
        "capitale": "",
        "habitant": "",
        "map": "",
        "latitude": 0,
        "longitude": 0
    }
    
    datas["pays"] = pays
    
    url1 = "https://gist.github.com/ofou/df09a6834a8421b4f376c875194915c9"
    url2 = "https://fr.wikipedia.org/wiki/"+pays
    url3 = "https://developers.google.com/public-data/docs/canonical/countries_csv?hl=fr"

    response1 = requests.get(url2)
    soup1 = BeautifulSoup(response1.content, "html.parser")
    
    response2 = requests.get(url1)
    soup2 = BeautifulSoup(response2.content, "html.parser")
       
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


    # response1 = requests.get(url1)
    # soup2 = BeautifulSoup(response1.content, "html.parser")
    # lat = soup2.findAll(string="France") 
    # lat = lat[0].parent.parent.findAll("td")
    # latitude = lat[3].text
    # longitude = lat[4].text

    #latitude longitude
    translator = Translator(to_lang="en", from_lang="fr")
    translation = translator.translate(pays)
    lat = soup2.findAll(string=translation) 
    lat = lat[0].parent.parent.findAll("td")

    
    latitude = float(lat[3].text)
    longitude = float(lat[4].text)
    
    datas["latitude"] = latitude
    datas["longitude"] = longitude
    
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
    
    # New York City coordinates
    # latitude = -18.9100122
    # longitude = 47.5255809

    # Create and display the map
    my_map = create_map(latitude, longitude, 6, capitale)
    my_map.render()
    datas["map"] = my_map._repr_html_

    return render(request, "app/pays_details.html", {'datas': datas})

