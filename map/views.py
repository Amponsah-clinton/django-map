from django.shortcuts import render, redirect
import folium
import geocoder
from .forms import SearchForm
from .models import Search

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else: 
        form = SearchForm()
    address = Search.objects.all()
    location = geocoder.osm(address)
    #geocoder compute longitude and latitude
    lat = location.lat
    lng = location.lng
    country = location.country
#   check for gibberish location
    # if lat == None or lng == None:
    #     address.delete()
    #     return HttpResponse('Invalid Address')
    # create map object with exact zoom and position information
    m = folium.Map(location=[19,-12], zoom_start = 2)
    # getting marker to point a location
    folium.Marker([lat, lng], tooltip = 'click for more', popup = country).add_to(m)
    # get html representation of map
    m = m._repr_html_()
    return render(request, 'index.html',{'m': m, 'form': form})