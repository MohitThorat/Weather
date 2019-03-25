from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart

from django.shortcuts import render,redirect
import urllib.error,urllib.parse,urllib.request
from django.http import HttpRequest
from .forms import HomeForm,BasicForm
import requests

import ssl
import json

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Api address for current weather
api_address='http://api.openweathermap.org/data/2.5/weather?appid=7d1433ffc1ad9f4b05ed906cceb2e1cc&q='
#Api address for getting ip of user
base_url = 'http://api.ipstack.com/'
#Api address for forecast
forecast_url = 'http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=7d1433ffc1ad9f4b05ed906cceb2e1cc&q='
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
        url_current = api_address + city
#if city is not found then set info = None
        try:
            uh = urllib.request.urlopen(url_current, context=ctx)
            data = uh.read().decode()
            info = json.loads(data)
        except:
            info = None
        if info != None:
            info['main']['temp_min'] = info['main']['temp_min'] - 273.15 ;
            info['main']['temp_max'] = info['main']['temp_max'] - 273.15 ;
            info['main']['temp'] = info['main']['temp'] - 273.15;
            return render(request, 'Weather/WeatherTemplate.html', {'info':info,'form': form})
        else:
            return render(request,'Weather/CityNF.html')
    else:
        return redirect('get')
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
     form = HomeForm(request.POST)
     Final_url = base_url + ip + '?access_key=bcc55a4f4c10f71f001c37b65d83c37f'
     try:
         gettingip = urllib.request.urlopen(Final_url, context=ctx)
         dataip = gettingip.read().decode()
         ip_json = json.loads(dataip)
     except:
         ip_json = None
     city = ip_json['city']
     info = {}
     if ip_json != None and city!= None:
         form = HomeForm()
         Current_url = api_address + city
         Final_url = forecast_url + city
         try:
             uh = urllib.request.urlopen(Current_url, context=ctx)
             data = uh.read().decode()
             info = json.loads(data)
         except:
             info = None
         if info != None:
             info['main']['temp_min'] = info['main']['temp_min'] - 273.15
             info['main']['temp_max'] = info['main']['temp_max'] - 273.15
             info['main']['temp'] = info['main']['temp'] - 273.15
             return render(request, 'Weather/WeatherTemplate.html', {'info':info,'form': form})
         else:
             return render(request,'Weather/CityNF.html')
     else:
         return render(request,'Weather/CityNF.html')

def homeforecast(request):
    form = HomeForm()
    return render(request,'Weather/HomeForecast.html',{'form':form})
def getforecast(request):
    info1 = {}
    form = HomeForm(request.POST)
    if form.is_valid():
        city = form.cleaned_data['City_Name']
        form = HomeForm()
        url_forecast = forecast_url + city
        maindata = list()
        data1 = list()
        data2 = list()
        data3 = list()
        data4 = list()
        data5 = list()
#if city is not found then set info = None
        try:
            uh = urllib.request.urlopen(url_forecast, context=ctx)
            data = uh.read().decode()
            info1 = json.loads(data)
        except:
            info1 = None
        if info1 != None:
            for days in info1['list']:
                days['main']['temp'] = days['main']['temp'] - 273.15;
                days['main']['temp_min'] = days['main']['temp_min'] - 273.15;
                days['main']['temp_max'] = days['main']['temp_max'] - 273.15;
            graph_index = 0
            l = len(info1['list'])
            for i in range(0,l):
                if  ((info1['list'][i]['dt_txt'].split()[0]) != (info1['list'][i+1]['dt_txt'].split()[0])):
                    graph_index = i+1
                    break
            data1 = [
                    ['Time','Temperature']
                    ]
            data2 = [
                    ['Time','Temperature']
                    ]
            data3 = [
                    ['Time','Temperature']
                    ]
            data4 = [
                    ['Time','Temperature']
                    ]
            date_1 = info1['list'][graph_index]['dt_txt'].split()[0]
            date_2 = info1['list'][graph_index+8]['dt_txt'].split()[0]
            date_3 = info1['list'][graph_index+16]['dt_txt'].split()[0]
            date_4 = info1['list'][graph_index+24]['dt_txt'].split()[0]
            for i in range(graph_index,graph_index+8):
                data1.append([info1['list'][i]['dt_txt'].split()[1],info1['list'][i]['main']['temp']])
            for i in range(graph_index+8,graph_index+16):
                data2.append([info1['list'][i]['dt_txt'].split()[1],info1['list'][i]['main']['temp']])
            for i in range(graph_index+16,graph_index+24):
                data3.append([info1['list'][i]['dt_txt'].split()[1],info1['list'][i]['main']['temp']])
            for i in range(graph_index+24,graph_index+32):
                data4.append([info1['list'][i]['dt_txt'].split()[1],info1['list'][i]['main']['temp']])
            data_source1 = SimpleDataSource(data=data1)
            chart1 = LineChart(data_source1)
            data_source2 = SimpleDataSource(data=data2)
            chart2 = LineChart(data_source2)
            data_source3 = SimpleDataSource(data=data3)
            chart3 = LineChart(data_source3)
            data_source4 = SimpleDataSource(data=data4)
            chart4 = LineChart(data_source4)
            return render(request, 'Weather/ForecasteTemplate.html',
                                    {'info1':info1,'form': form,
                                    'chart1':chart1,'chart2':chart2,'chart3':chart3,'chart4':chart4,
                                    'date_1':date_1,'date_2':date_2,'date_3':date_3,'date_4':date_4,
                                    })
        else:
            return render(request,'Weather/CityNF.html')
    else:
        return redirect('homeforecast')

def getforecastip(request):
    ip = get_client_ip(request)
    Final_url = base_url + ip + '?access_key=bcc55a4f4c10f71f001c37b65d83c37f'
    try:
        gettingip = urllib.request.urlopen(Final_url, context=ctx)
        dataip = gettingip.read().decode()
        ip_json = json.loads(dataip)
    except:
        ip_json = None
    city = ip_json['city']
    info1 = {}
    if ip_json != None and city!= None:
        form = HomeForm()
        Final_url = forecast_url + city
        try:
            uh = urllib.request.urlopen(Final_url, context=ctx)
            data = uh.read().decode()
            info1 = json.loads(data)
        except:
            info1 = None
        if info1 != None:
            for days in info1['list']:
                days['main']['temp'] = days['main']['temp'] - 273.15
                days['main']['temp_min'] = days['main']['temp_min'] - 273.15
                days['main']['temp_max'] = days['main']['temp_max'] - 273.15
                graph_index = 0
                l = len(info1['list'])
                for i in range(0,l):
                    if  ((info1['list'][i]['dt_txt'].split()[0]) != (info1['list'][i+1]['dt_txt'].split()[0])):
                        graph_index = i+1
                        break
                data1 = [
                        ['Time','Temperature']
                        ]
                data2 = [
                        ['Time','Temperature']
                        ]
                data3 = [
                        ['Time','Temperature']
                        ]
                data4 = [
                        ['Time','Temperature']
                        ]
                date_1 = info1['list'][graph_index]['dt_txt'].split()[0]
                date_2 = info1['list'][graph_index+8]['dt_txt'].split()[0]
                date_3 = info1['list'][graph_index+16]['dt_txt'].split()[0]
                date_4 = info1['list'][graph_index+24]['dt_txt'].split()[0]
                for i in range(graph_index,graph_index+8):
                    data1.append([info1['list'][i]['dt_txt'].split()[1],info1['list'][i]['main']['temp']])
                for i in range(graph_index+8,graph_index+16):
                    data2.append([info1['list'][i]['dt_txt'].split()[1],info1['list'][i]['main']['temp']])
                for i in range(graph_index+16,graph_index+24):
                    data3.append([info1['list'][i]['dt_txt'].split()[1],info1['list'][i]['main']['temp']])
                for i in range(graph_index+24,graph_index+32):
                    data4.append([info1['list'][i]['dt_txt'].split()[1],info1['list'][i]['main']['temp']])
                data_source1 = SimpleDataSource(data=data1)
                chart1 = LineChart(data_source1)
                data_source2 = SimpleDataSource(data=data2)
                chart2 = LineChart(data_source2)
                data_source3 = SimpleDataSource(data=data3)
                chart3 = LineChart(data_source3)
                data_source4 = SimpleDataSource(data=data4)
                chart4 = LineChart(data_source4)
            return render(request, 'Weather/ForecasteTemplate.html',
                                   {'form': form,'info1':info1,
                                   'chart1':chart1,'chart2':chart2,'chart3':chart3,'chart4':chart4,
                                   'date_1':date_1,
                                   'date_2':date_2,
                                   'date_3':date_3,
                                   'date_4':date_4,
                                    })
        else:
            return render(request,'Weather/CityNF.html')
    else:
        return render(request,'Weather/CityNF.html')
