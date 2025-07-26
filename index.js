const API_URL = 'http://127.0.0.1:8000'

document.addEventListener('DOMContentLoaded', function() {
    fetch(`${API_URL}/userdetails`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('userdetails').innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
        })
        .catch(error => {
            document.getElementById('userdetails').textContent = 'Error: ' + error;
        });
});