from flask import Flask, request, jsonify
import tensorflow_hub as hub
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import numpy as np
import io
from PIL import Image
import json
app = Flask(__name__)
with open('output.txt') as f: 
    data = f.read()
labels = json.loads(data)  
model = load_model('temp.keras', custom_objects={"KerasLayer": hub.KerasLayer})

@app.route('/predict', methods=['POST'])
def predict():
    file = request.data
    if file:
        im_data = io.BytesIO(file)
        im = Image.open(im_data)
        img_array = image.img_to_array(im)
        img_array_expanded_dims = np.expand_dims(img_array, axis=0)
        img_224 = tf.image.resize_with_pad(img_array_expanded_dims, 224, 224)
        predictions = model.predict(img_224)
        top_5_indices = np.argsort(predictions[0])[::-1][:5]
        top_5_labels = [list(labels.keys())[index] for index in top_5_indices]
        top_5_probabilities = [predictions[0][index] for index in top_5_indices]
        top_5_dict = {label: np.round(probability, 4) for label, probability in zip(top_5_labels, top_5_probabilities)}
        #print(top_5_dict)
        return jsonify({'prediction': str(top_5_dict)}), 200
     
    return jsonify({'error': 'Error processing file'}), 500

if __name__ == '__main__':
    app.run(port=3267, debug=True)