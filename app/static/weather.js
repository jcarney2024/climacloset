function sendGetRequest() {
    const selectedLocation = this.value;
    const [latitude, longitude] = selectedLocation.split(',');
    const encodedLatitude = encodeURIComponent(latitude);
    const encodedLongitude = encodeURIComponent(longitude);
    window.location.href = `?latitude=${encodedLatitude}&longitude=${encodedLongitude}`;
}
