from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
import google.generativeai as genai
from flask import request, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

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

@main.route('/chat')
def chat():
    def get_weather():
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')

        if not latitude or not longitude:
            return jsonify({'error': 'Missing latitude or longitude'}), 400

        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&temperature_unit=fahrenheit"

        try:
            response = request.get(api_url)
            response.raise_for_status()
            weather_data = response.json()
            return jsonify(weather_data['current_weather'])
        except request.RequestException as e:
            return jsonify({'error': 'Failed to fetch weather data'}), 500

    genai.configure(api_key="AIzaSyDa7FYJhcamSRfO1udd9-p5BDe0rwdhqGQ")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Explain how AI works")
    return response.text