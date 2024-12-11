document.addEventListener('DOMContentLoaded', function () {
    // ...existing code...

    const locationInput = document.getElementById('location-input');
    const suggestionsBox = document.getElementById('suggestions');

    let timeout = null;

    locationInput.addEventListener('input', function () {
        const query = this.value;
        clearTimeout(timeout);
        suggestionsBox.innerHTML = '';  // Clear suggestions immediately

        if (query.length >= 3) {
            timeout = setTimeout(() => {
                fetch(`/autocomplete?q=${encodeURIComponent(query)}`)
                    .then(response => response.json())
                    .then(data => {
                        suggestionsBox.innerHTML = '';
                        data.forEach(item => {
                            const suggestionItem = document.createElement('a');
                            suggestionItem.href = '#';
                            suggestionItem.classList.add('list-group-item', 'list-group-item-action');
                            suggestionItem.textContent = item.name;
                            suggestionItem.dataset.latitude = item.latitude;
                            suggestionItem.dataset.longitude = item.longitude;
                            suggestionItem.addEventListener('click', function (e) {
                                e.preventDefault();
                                locationInput.value = this.textContent;
                                suggestionsBox.innerHTML = '';
                                const latitude = this.dataset.latitude;
                                const longitude = this.dataset.longitude;
                                // Update the weather information
                                updateWeather(latitude, longitude);
                            });
                            suggestionsBox.appendChild(suggestionItem);
                        });
                    });
            }, 300);
        } else {
            suggestionsBox.innerHTML = '';
        }
    });

    function updateWeather(latitude, longitude) {
        fetch(`/?latitude=${latitude}&longitude=${longitude}`)
            .then(response => response.text())
            .then(html => {
                // Parse the returned HTML to update the weather info and image
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newWeatherInfo = doc.querySelector('#weather-info').innerHTML;
                const newWeatherImage = doc.querySelector('#weather-image').src;
                document.getElementById('weather-info').innerHTML = newWeatherInfo;
                document.getElementById('weather-image').src = newWeatherImage;
                document.getElementById('temp').value = doc.querySelector('#temp').value;
            });
    }

    // ...existing code...
});

function sendGetRequest() {
    const selectedLocation = this.value;
    const [latitude, longitude] = selectedLocation.split(',');
    const encodedLatitude = encodeURIComponent(latitude);
    const encodedLongitude = encodeURIComponent(longitude);
    window.location.href = `?latitude=${encodedLatitude}&longitude=${encodedLongitude}`;
}
