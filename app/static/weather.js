function sendGetRequest() {
    const selectedLocation = this.value;
    const [latitude, longitude] = selectedLocation.split(',');
    window.location.href = `?latitude=${latitude}&longitude=${longitude}`;
}
