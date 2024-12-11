document.addEventListener('DOMContentLoaded', function () {
    const locationInput = document.getElementById('location-input');
    const suggestionsBox = document.getElementById('suggestions');
    const latitudeInput = document.getElementById('latitude');
    const longitudeInput = document.getElementById('longitude');
    const locationHiddenInput = document.getElementById('location');
    const tempInput = document.getElementById('temp');

    let timeout = null;

    locationInput.addEventListener('input', function () {
        const query = this.value;
        clearTimeout(timeout);
        suggestionsBox.innerHTML = '';  // Clear suggestions immediately

        if (query.length >= 2) {
            timeout = setTimeout(() => {
                fetch(`/autocomplete?q=${encodeURIComponent(query)}`)
                    .then(response => response.json())
                    .then(data => {
                        suggestionsBox.innerHTML = '';
                        data.forEach(location => {
                            const suggestionItem = document.createElement('div');
                            suggestionItem.classList.add('list-group-item', 'list-group-item-action');
                            suggestionItem.textContent = location.name;
                            suggestionItem.dataset.latitude = location.latitude;
                            suggestionItem.dataset.longitude = location.longitude;
                            suggestionItem.dataset.locationName = location.name;
                            suggestionItem.addEventListener('click', function () {
                                locationInput.value = this.dataset.locationName;
                                latitudeInput.value = this.dataset.latitude;
                                longitudeInput.value = this.dataset.longitude;
                                locationHiddenInput.value = this.dataset.locationName;
                                suggestionsBox.innerHTML = '';

                                // Update the weather information
                                updateWeather(this.dataset.latitude, this.dataset.longitude, this.dataset.locationName);
                            });
                            suggestionsBox.appendChild(suggestionItem);
                        });
                    });
            }, 300);
        } else {
            suggestionsBox.innerHTML = '';
        }
    });

    function updateWeather(latitude, longitude, locationName) {
        fetch(`/?latitude=${latitude}&longitude=${longitude}&location=${encodeURIComponent(locationName)}`)
            .then(response => response.text())
            .then(html => {
                // Parse the returned HTML to update the weather info and image
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newWeatherInfo = doc.querySelector('#weather-info').innerHTML;
                const newWeatherImage = doc.querySelector('#weather-image').src;
                const newTemp = doc.querySelector('#temp').value;

                document.getElementById('weather-info').innerHTML = newWeatherInfo;
                document.getElementById('weather-image').src = newWeatherImage;
                tempInput.value = newTemp;

                // Update hidden inputs
                latitudeInput.value = latitude;
                longitudeInput.value = longitude;
                locationHiddenInput.value = locationName;
            });
    }
});

function sendGetRequest() {
    const selectedLocation = this.value;
    const [latitude, longitude] = selectedLocation.split(',');
    const encodedLatitude = encodeURIComponent(latitude);
    const encodedLongitude = encodeURIComponent(longitude);
    window.location.href = `?latitude=${encodedLatitude}&longitude=${encodedLongitude}`;
}
