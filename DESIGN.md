# ClimaCloset Design Document

## Overview
ClimaCloset is built using the Flask web framework. The project integrates a dynamic weather API and AI API to offer personalized outfit recommendations.

## Architecture
The project follows a Model-View-Controller (MVC) architecture:
- **Models**: Handle data structure and interactions (e.g., user profiles).
- **Views**: Render HTML templates dynamically based on user interactions.
- **Controllers**: Logic for API calls and user requests.

## Key Features
1. **Weather Integration**:
   - Uses an external API to fetch real-time weather data.
   - Provides tailored recommendations based on weather conditions.

2. **User Authentication**:
   - Secure login and signup mechanisms using Flask-Security.
   - User profiles are stored securely in the database.

## Design Decisions
1. **Framework Selection**:
   - Flask was chosen for its simplicity, lightweight structure, and robust ecosystem. It was also taught during lectures for CS50.

2. **Database**:
   - SQLite was used for development due to its ease of use. For production, the app can be configured to use PostgreSQL for better scalability.

3. **Frontend**:
   - Jinja2 templating engine provides dynamic content rendering.
   - Static files (CSS, JS) are managed under the `static/` directory.
   - Added header words to create easy access to different 

4. **Deployment**:
   - Designed to deploy on Heroku. The `Procfile` and environment variables ensure smooth deployment.

## Challenges and Solutions
1. **API Rate Limits**:
   - Implemented caching to minimize excessive calls to the weather API.
2. **Responsive Design**:
   - Leveraged Bootstrap for consistent and responsive UI.

## Future Enhancements
- Integrating machine learning for visual outfit recommendations.
- Adding support for multiple languages.
