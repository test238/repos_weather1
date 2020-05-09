from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
from .unit_converter import parse_dms
from datetime import datetime
import re

def index(request):
    City.objects.all().delete()
    cities = City.objects.all() #return all the cities in the database
    #url_weather = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=f3d77950bc7cc4a4899f21e0e491ecd3'
    url_weather_forecast = 'https://api.weatherbit.io/v2.0/forecast/daily?lat={}&lon={}&key=eb37c9d0e8204376a376ae29539d8fec&units=M&days=7'
    url_weather_current = 'https://api.weatherbit.io/v2.0/current?lat={}&lon={}&key=eb37c9d0e8204376a376ae29539d8fec&units=M'
    url_geodata = 'https://api.opencagedata.com/geocode/v1/json?q={}&key=1e73e20428e54172a2795c05a59cafab'

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate
    form = CityForm()

    weather_data_current = []
    weather_data_plus1d = []
    weather_data_plus2d = []
    weather_data_plus3d = []
    weather_data_plus4d = []
    
    for city in cities:
        city_geodata = requests.get(url_geodata.format(city)).json() #request the API data and convert the JSON to Python data types
        city_countrycode = city_geodata["results"][0]["components"]["ISO_3166-1_alpha-3"]
        lat_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lat"])
        lng_param = parse_dms(city_geodata["results"][0]["annotations"]["DMS"]["lng"])

        city_weather_forecast = requests.get(url_weather_forecast.format(lat_param,lng_param)).json()
        city_weather_current = requests.get(url_weather_current.format(lat_param,lng_param)).json()
        
        current_weather = {
            'city' : city,
            'countrycode' : city_countrycode,           
            'utc_time' : datetime.utcfromtimestamp(float(city_weather_current['data'][0]['ts'])).strftime('%Y-%m-%d %H:%M:%S'),
            'time_zone' : city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"],
            'local_time' : datetime.utcfromtimestamp(float(city_weather_current['data'][0]['ts']+city_geodata["results"][0]["annotations"]["timezone"]["offset_sec"])).strftime('%Y-%m-%d %H:%M:%S'),
            'pressure' : city_weather_current['data'][0]['pres'],
            'humidity' : city_weather_current['data'][0]['rh'],
            'temperature' : city_weather_current['data'][0]['temp'],
            'description' : city_weather_current['data'][0]['weather']['description'],
            'icon' : city_weather_current['data'][0]['weather']['icon'],
        }

        plus1d_weather = {
            'city' : city,
            'countrycode' : city_countrycode,      
            'time' : city_weather_forecast['data'][1]['ts'],
            'pressure' : city_weather_forecast['data'][1]['pres'],
            'humidity' : city_weather_forecast['data'][1]['rh'],
            'max_temp' : city_weather_forecast['data'][1]['max_temp'],
            'min_temp' : city_weather_forecast['data'][1]['min_temp'],
            'temperature' : city_weather_forecast['data'][1]['temp'],
            'description' : city_weather_forecast['data'][1]['weather']['description'],
            'icon' : city_weather_forecast['data'][1]['weather']['icon'],
        }

        plus2d_weather = {
            'city' : city,
            'countrycode' : city_countrycode,      
            'time' : city_weather_forecast['data'][2]['ts'],
            'pressure' : city_weather_forecast['data'][2]['pres'],
            'humidity' : city_weather_forecast['data'][2]['rh'],
            'max_temp' : city_weather_forecast['data'][2]['max_temp'],
            'min_temp' : city_weather_forecast['data'][2]['min_temp'],
            'temperature' : city_weather_forecast['data'][2]['temp'],
            'description' : city_weather_forecast['data'][2]['weather']['description'],
            'icon' : city_weather_forecast['data'][2]['weather']['icon'],
        }

        plus3d_weather = {
            'city' : city,
            'countrycode' : city_countrycode,      
            'time' : city_weather_forecast['data'][3]['ts'],
            'pressure' : city_weather_forecast['data'][3]['pres'],
            'humidity' : city_weather_forecast['data'][3]['rh'],
            'max_temp' : city_weather_forecast['data'][3]['max_temp'],
            'min_temp' : city_weather_forecast['data'][3]['min_temp'],
            'temperature' : city_weather_forecast['data'][3]['temp'],
            'description' : city_weather_forecast['data'][3]['weather']['description'],
            'icon' : city_weather_forecast['data'][3]['weather']['icon'],
        }

        plus4d_weather = {
            'city' : city,
            'countrycode' : city_countrycode,      
            'time' : city_weather_forecast['data'][4]['ts'],
            'pressure' : city_weather_forecast['data'][4]['pres'],
            'humidity' : city_weather_forecast['data'][4]['rh'],
            'max_temp' : city_weather_forecast['data'][4]['max_temp'],
            'min_temp' : city_weather_forecast['data'][4]['min_temp'],
            'temperature' : city_weather_forecast['data'][4]['temp'],
            'description' : city_weather_forecast['data'][4]['weather']['description'],
            'icon' : city_weather_forecast['data'][4]['weather']['icon'],
        }

        weather_data_current.append(current_weather) #add the data for the current city into our list
        weather_data_plus1d.append(plus1d_weather) #add the data for the current city into our list
        weather_data_plus2d.append(plus2d_weather) #add the data for the current city into our list
        weather_data_plus3d.append(plus3d_weather) #add the data for the current city into our list
        weather_data_plus4d.append(plus4d_weather) #add the data for the current city into our list
        
    context = {'weather_data_current' : weather_data_current, 'weather_data_plus1d' : weather_data_plus1d, 'weather_data_plus2d' : weather_data_plus2d, 'weather_data_plus3d' : weather_data_plus3d, 'weather_data_plus4d' : weather_data_plus4d, 'form' : form}  
    return render(request, 'weather_api2_nextdays/index.html', context) #returns the index.html template
