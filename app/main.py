from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
import requests
from dotenv import load_dotenv
import random
import google.generativeai as genai
import os

load_dotenv()

def page_not_found(e):
    return render_template('404.html', e=e), 404

main = Blueprint('main', __name__)

@main.route('/index')
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
    # Remove hardcoded API key
    
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

    return jsonify({'suggestion': suggestion})