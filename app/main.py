from flask import Blueprint, render_template, request, jsonify, url_for
from flask_login import login_required, current_user
import requests
from dotenv import load_dotenv
import google.generativeai as genai
import os
from .models import History
from datetime import datetime
from flask_login import current_user
import json
from . import db

load_dotenv()

# Load town data when the app starts
towns = []
with open('app/static/place-town.ndjson', 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue  # Skip empty lines
        try:
            town = json.loads(line)
            towns.append(town)
        except json.JSONDecodeError:
            continue  # Skip invalid JSON lines

def page_not_found(e):
    return render_template('404.html', e=e), 404

main = Blueprint('main', __name__)

@main.route('/index')
@main.route('/')
def index():
    latitude = request.args.get('latitude', '41.3081')
    longitude = request.args.get('longitude', '-72.9282')
    location = request.args.get('location', 'New Haven, Connecticut')
    
    api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&temperature_unit=fahrenheit"


    try:
        response = requests.get(api_url)
        response.raise_for_status()
        weather_data = response.json()
        temp = weather_data['current_weather']['temperature']
        weather_code = weather_data['current_weather']['weathercode']
    except requests.RequestException as e:
        temp = None
        weather_code = None

    if weather_code in [61, 63, 65, 80, 81, 82]:  # rain 
        weather_icon = "../static/rain.svg"
    elif weather_code in [45, 48, 95]:  # windy or stormy conditions
        weather_icon = "../static/windy.svg"
    else:
        weather_icon = "../static/sun_cloud.svg"  # sunny weather    
    
    user_name = current_user.name if current_user.is_authenticated else None

    return render_template('index.html', temp=temp, selected_location=f"{latitude},{longitude}", image=weather_icon, latitude=latitude, longitude=longitude, location=location, user_name=user_name)


@main.route('/profile')
@login_required
def profile():
    user = current_user  # Get the current logged-in user
    history = History.query.filter_by(user_id=user.id).order_by(History.timestamp.desc()).all()
    return render_template('profile.html', name=user.name, current_user=user, history=history)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/explore')
def explore():
    import requests  # Ensure the requests library is imported.

    locations = {
        "Chicago": {"latitude": "41.8781", "longitude": "-87.6298"},
        "San Francisco": {"latitude": "37.7749", "longitude": "-122.4194"},
        "New York": {"latitude": "40.7128", "longitude": "-74.0060"},
        "Washington, D.C.": {"latitude": "38.9072", "longitude": "-77.0369"},
        "Paris": {"latitude": "48.8566", "longitude": "2.3522"},
        "Beijing": {"latitude": "39.9042", "longitude": "116.4074"}
    }

    # Fetch weather data
    weather_data = {}
    for city, coords in locations.items():
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['latitude']}&longitude={coords['longitude']}&current_weather=true&temperature_unit=fahrenheit"
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            # Extract the current temperature from the response
            weather_data[city] = data.get("current_weather", {}).get("temperature")
        except requests.RequestException:
            weather_data[city] = None  # Handle failure gracefully

    # Pass temperatures to the template
    return render_template(
        'explore.html',
        chicago_temp=weather_data.get("Chicago"),
        sf_temp=weather_data.get("San Francisco"),
        ny_temp=weather_data.get("New York"),
        dc_temp=weather_data.get("Washington, D.C."),
        paris_temp=weather_data.get("Paris"),
        beijing_temp=weather_data.get("Beijing")
    )

@main.route('/chat', methods=['POST'])
def chat():
    temp = request.form.get('temp')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    location = request.form.get('location')

    # Validate the received data
    if not all([temp, latitude, longitude, location]):
        return jsonify({'error': 'Missing required data.'}), 400
    
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }
    
    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    )

    genai.configure(api_key="AIzaSyAUjVArswFob0VQuXFNf3MRz3a7v2lBXUU")
    response = model.generate_content(f"Generate clothing suggestions based on the temperature: {temp} degrees farenheit. Only give one sentence response with what to wear in simple terms for an outfit.")
    suggestion = response.text if response.text else "No suggestion available."

    if current_user.is_authenticated:
        new_history = History(
            user_id=current_user.id,
            latitude=latitude,
            longitude=longitude,
            location=location,
            timestamp=datetime.utcnow(),
            response=suggestion
        )
        db.session.add(new_history)
        db.session.commit()

    return jsonify({'suggestion': suggestion})

@main.route('/autocomplete')
def autocomplete():
    q = request.args.get('q', '').lower()
    suggestions = []
    if len(q) >= 2:
        for town in towns:
            name = town.get('name')
            if not name:
                continue  # Skip if 'name' is missing
            state = town.get('address', {}).get('state', '')
            if q in name.lower():
                location = town.get('location', [None, None])
                if location and len(location) >= 2:
                    latitude = location[1]
                    longitude = location[0]
                    suggestions.append({
                        'name': f"{name}, {state}",
                        'latitude': latitude,
                        'longitude': longitude
                    })
            if len(suggestions) >= 20:
                break
    return jsonify(suggestions)