from django.shortcuts import render
import requests
import datetime
from django.conf import settings

def home(request):
    city = 'Lagos'  # Default city

    if request.method == 'POST':  # Check if the form was submitted
        city = request.POST.get('city', 'Lagos')  # Get city from input field

    api_key = settings.OPENWEATHER_API_KEY  # Store API key in settings
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    params = {'units': 'metric'}

    # Google Search API for city images
    SEARCH_API_KEY = settings.SEARCHBAR_API_KEY
    SEARCH_ENGINE_ID = '058335013793a409d'
    query = f"{city} skyline"  # More descriptive query for better images
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={SEARCH_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    image_url = ""  # Default empty image URL
    try:
        data = requests.get(city_url).json()
        search_items = data.get('items', [])
        if search_items:
            image_url = search_items[0]['link']  # Get the first image
    except Exception as e:
        print("Error fetching image:", e)

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
    else:
        description, icon, temp = "City not found", "", ""

    day = datetime.date.today()

    return render(request, 'weatherapp/index.html', {
        'description': description,
        'icon': icon,
        'temp': temp,
        'day': day,
        'city': city.upper(),  # Make city name uppercase
        'image_url': image_url  # Pass the image URL to the template
    })
