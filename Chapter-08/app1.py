from flask import Flask, render_template, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image  # <-- Ensure correct import here
from PIL import Image  # <-- Import PIL.Image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import optimizers
import os
import io

app = Flask(__name__, template_folder='templates')

# Load the trained model
model_path = "CIFAR_model.h5"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file '{model_path}' not found!")

model = load_model(model_path)

# CIFAR-10 Class Names
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    try:
        # Convert the file to a PIL image
        img = Image.open(file.stream)
        img = img.resize((32, 32))  # Resize the image to match the model's input size
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array.astype('float32') / 255  # Normalize the image

        # Prediction
        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction)
        predicted_label = class_names[predicted_class]

        return jsonify({'label': predicted_label})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
