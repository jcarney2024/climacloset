# ClimaCloset

ClimaCloset is a web application that is designed to give you weather-specific outfit recommendations. By integrating weather forecasts, ClimaCloset allows you to dress appropriately for any occasion.

## Features
- Dynamic weather-based clothing suggestions.
- Easy-to-navigate user interface.
- Secure user authentication and specific profile management.

## Prerequisites
- Python 3.9+ installed on your system.
- A GitHub account for using Codespaces (if applicable).
- Flask framework and required dependencies (see `requirements.txt`).

## Development Setup

### Option 1: Using GitHub Codespaces
1. **Create a Codespace**:
   - On the repository page, click the **Code** button.
   - Select **Codespaces** and click **Create codespace on main**.

   **--OR--**
   Use this badge to create a codespace directly:
   [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/jcarney2024/climacloset)

2. **Initialization**:
   - Wait for the development container to set up using `.devcontainer/devcontainer.json`.

3. **Run the Flask app**:
   type flask run --debug --host=0.0.0.0 into the terminal 

4. **Access the app**:
   - Forward port **5000** when prompted.
   - Open the forwarded port in your browser.

### Option 2: Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/jcarney2024/climacloset.git
   cd climacloset
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # (Windows: venv\\Scripts\\activate)
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example` and configure your settings.

5. Run the app:
   ```bash
   flask run
   ```

## Usage
1. Open the app in your browser.

## Without a Log in
1. Use text box to input a location
2. Read temperature of location
3. Click outfit suggestion button
4. View recommendations based on the current weather.
5. Check out Explore Page from clicking "Explore" on the top header
6. Check out About Page from clicking "About" on the top header

## With a Log in
3. Sign up or log in.
4. Edit profile picture if you want to
5. Edit name if you want to
6.  Use text box to input a location
7. Read temperature of location
8. Click outfit suggestion button
9. View recommendations based on the current weather.
10. Check out Explore Page from clicking "Explore" on the top header
11. Check out About Page from clicking "About" on the top header
12. Log out when done

## Deployment
This app is designed to deploy easily on Heroku. Use the `Procfile` for deployment configuration. Ensure all environment variables in `.env` are configured correctly.
