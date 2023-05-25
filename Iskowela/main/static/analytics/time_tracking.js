
window.addEventListener('beforeunload', function(event) {
    // Send an AJAX request to update the time tracking information
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/update-time-spent/');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send();
});
