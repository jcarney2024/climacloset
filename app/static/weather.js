document.getElementById('location-select').addEventListener('change', function () {
    // Get the selected location value
    const selectedLocation = this.value;
    const [latitude, longitude] = selectedLocation.split(',');

    console.log("Selected location:", selectedLocation);
    console.log("Latitude:", latitude, "Longitude:", longitude);

    // Construct the API URL with dynamic latitude and longitude
    const apiUrl = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current_weather=true&temperature_unit=fahrenheit`;

    // Fetch the weather data from the Open-Meteo API
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            const temperature = data.current_weather.temperature;
            const weatherCode = data.current_weather.weathercode; // Get the weather condition code

            // Display the temperature in the #weather-info div
            document.getElementById('weather-info').innerText = `The current temperature is ${temperature}°F`;

            const images = [
                "../static/rain.svg",
                "../static/sun_cloud.svg",
                "../static/windy.svg",
            ];

            // Choose a random image from the array
            const randomIndex = Math.floor(Math.random() * images.length);
            const randomImage = images[randomIndex];

            // Update the image source with the random image
            document.getElementById('weather-image').src = randomImage;
        })
        .catch(error => {
            // If there is an error, display an error message and use a default image
            document.getElementById('weather-info').innerText = "Unable to fetch weather data.";
            document.getElementById('weather-image').src = "../static/error_image.svg";
        });
});

// Trigger the change event to show the weather for the default location when the page loads
document.getElementById('location-select').dispatchEvent(new Event('change'));
