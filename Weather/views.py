from django.shortcuts import render,HttpResponse, HttpResponseRedirect
import urllib.error,urllib.parse,urllib.request
from django.http import HttpRequest
from .forms import HomeForm,BasicForm


import ssl
import json

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

api_address='http://api.openweathermap.org/data/2.5/weather?appid=7d1433ffc1ad9f4b05ed906cceb2e1cc&q='
base_url = 'http://api.ipstack.com/'
#this function is used first time accessing the website using GET
def get(request):
    form = HomeForm()
    return render(request,'Weather/Home.html',{'form':form})

#this function is used using POST to get the weather
def post(request):
    info = {}
    form = HomeForm(request.POST)
    if form.is_valid():
        city = form.cleaned_data['City_Name']
        form = HomeForm()
        url = api_address + city
#if city if not found set info = NONE
        try:
            uh = urllib.request.urlopen(url, context=ctx)
            data = uh.read().decode()
            info = json.loads(data)
        except:
            info = None
        if info != None:
            info['main']['temp_min'] = info['main']['temp_min'] - 273.15 ;
            info['main']['temp_max'] = info['main']['temp_max'] - 273.15 ;
            info['main']['temp'] = info['main']['temp'] - 273.15 ;
            return render(request, 'Weather/WeatherTemplate.html', {'info':info,'form': form})
        else:
            return render(request,'Weather/CityNF.html',{'form':form})

#getting client ip using django inbuilt tools
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
#client ip -> get city -> get weather
def post_using_ip(request):
     ip = get_client_ip(request)
     ip_json = {}
     form = BasicForm()
     Final_url = base_url + ip + '?access_key=bcc55a4f4c10f71f001c37b65d83c37f'
     print(base_url)
     try:
         gettingip = urllib.request.urlopen(Final_url, context=ctx)
         dataip = gettingip.read().decode()
         ip_json = json.loads(dataip)
     except:
         ip_json = None
     city = ip_json['city']
     post(request)
     if ip_json != None and city!= null:
         return render(request,'Weather/CityIP.html',{'form':form,'ip_json':ip_json})
     else:
            return render(request,'Weather/CityNF.html',{'form':form})
