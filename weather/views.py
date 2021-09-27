from django.shortcuts import render
# import json to load json data to python dictionary
import json
# urllib.request to make a request to api
import urllib.request
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

class WeatherView(LoginRequiredMixin, View):
    template_name = 'weather/weather.html'

    def index(self,request):
        if request.method == 'POST':
        
            city = request.POST['city']
            # source contain JSON data from API

            source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+ city + '&appid=8bb4beff142be8db1dc25398732921fe').read()
  
            # converting JSON data to a dictionary
            list_of_data = json.loads(source)
  
            # data for variable list_of_data
            data = {
                "country_code": str(list_of_data['sys']['country']),
                "coordinate": str(list_of_data['coord']['lon']) + ' '
                            + str(list_of_data['coord']['lat']),
                "temp": str(list_of_data['main']['temp']) + 'k',
                "pressure": str(list_of_data['main']['pressure']),
                "humidity": str(list_of_data['main']['humidity']),
            }
            print(data)
        else:
            data ={}
        return render(request, "weather/weather.html", data)

    def get(self, request):
       return self.index(request)

    def post(self, request):
       return self.index(request)

