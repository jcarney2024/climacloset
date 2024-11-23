from email.mime import image
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from . import db
import requests
from dotenv import load_dotenv
import os
import random
import google.generativeai as genai

load_dotenv()

def page_not_found(e):
    return render_template('404.html', e=e), 404

main = Blueprint('main', __name__)

@main.route('/')
def index():
    latitude = request.args.get('latitude', '41.3081')
    longitude = request.args.get('longitude', '-72.9282')
    selected_location = f"{latitude},{longitude}" if latitude and longitude else None

    api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&temperature_unit=fahrenheit"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        weather_data = response.json()
        temp = weather_data['current_weather']['temperature']
    except requests.RequestException as e:
        temp = None
        
    # List of image paths
    images = [
    "../static/rain.svg",
    "../static/sun_cloud.svg",
    "../static/windy.svg",
    ]

    # Choose a random image from the list
    random_index = random.randint(0, len(images) - 1)
    random_image = images[random_index]

    return render_template('index.html', temp=temp, selected_location=selected_location, image=random_image)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/explore')
def explore():
    return render_template('explore.html')

@main.route('/chat', methods=['POST'])
def chat():
    temp = request.form.get('temp')
    genai.configure(api_key=os.environ["API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Generate clothing suggestions based on the temperature: {temp}. Only give one sentence response with what to wear in simple terms.")
    
    suggestion = response.text if response.text else "No suggestion available."
    
    return jsonify({'suggestion': suggestion})