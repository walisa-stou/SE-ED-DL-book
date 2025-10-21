document.getElementById('uploadBtn').addEventListener('click', function() {
    document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        // Show image preview
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('imagePreview').innerHTML = `<img src="${e.target.result}" width="200" />`;
        };
        reader.readAsDataURL(file);

        // Prepare the form data for the file upload
        const formData = new FormData();
        formData.append('file', file);

        // Send the file to the Flask backend for prediction
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.label) {
                document.getElementById('predictionResult').textContent = `Predicted Label: ${data.label}`;
            } else {
                document.getElementById('predictionResult').textContent = `Error: ${data.error}`;
            }
        })
        .catch(error => {
            document.getElementById('predictionResult').textContent = `Error: ${error}`;
        });
    }
});
