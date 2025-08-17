from django.shortcuts import render
from django.contrib import messages
import requests
import datetime
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
import requests
import datetime


def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'indore'

    # Weather API
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.OPENWEATHER_KEY}'
    PARAMS = {'units': 'metric'}

    # Google Custom Search API
    API_KEY = settings.GOOGLE_API_KEY
    SEARCH_ENGINE_ID = settings.GOOGLE_SEARCH_ENGINE_ID
    query = city + " 1920x1080"
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&searchType=image&imgSize=large"

    # Default fallback image
    image_url = "https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg"

    try:
        # Get city image
        img_data = requests.get(city_url).json()
        search_items = img_data.get("items")
        if search_items and len(search_items) > 0:
            image_url = search_items[0]['link']

        # Get weather data
        weather_data = requests.get(url, params=PARAMS).json()
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })

    except Exception as e:
        messages.error(request, "City information is not available to our API")
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'indore',
            'exception_occurred': True,
            'image_url': image_url
        })
