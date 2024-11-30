from flask import Flask, request, jsonify
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from PIL import Image
import io
import numpy as np

app = Flask(__name__)

# Constants
IMAGE_SHAPE = (224, 224, 3)  
CLASS_NAMES = [
    'air hockey', 'ampute football', 'archery', 'arm wrestling', 'axe throwing',
    'balance beam', 'barell racing', 'baseball', 'basketball', 'baton twirling',
    'bike polo', 'billiards', 'bmx', 'bobsled', 'bowling',
    'boxing', 'bull riding', 'bungee jumping', 'canoe slamon', 'cheerleading',
    'chuckwagon racing', 'cricket', 'croquet', 'curling', 'disc golf',
    'fencing', 'field hockey', 'figure skating men', 'figure skating pairs', 'figure skating women',
    'fly fishing', 'football', 'formula 1 racing', 'frisbee', 'gaga',
    'giant slalom', 'golf', 'hammer throw', 'hang gliding', 'harness racing',
    'high jump', 'hockey', 'horse jumping', 'horse racing', 'horseshoe pitching',
    'hurdles', 'hydroplane racing', 'ice climbing', 'ice yachting', 'jai alai',
    'javelin', 'jousting', 'judo', 'lacrosse', 'log rolling',
    'luge', 'motorcycle racing', 'mushing', 'nascar racing', 'olympic wrestling',
    'parallel bar', 'pole climbing', 'pole dancing', 'pole vault', 'polo',
    'pommel horse', 'rings', 'rock climbing', 'roller derby', 'rollerblade racing',
    'rowing', 'rugby', 'sailboat racing', 'shot put', 'shuffleboard',
    'sidecar racing', 'ski jumping', 'sky surfing', 'skydiving', 'snow boarding',
    'snowmobile racing', 'speed skating', 'steer wrestling', 'sumo wrestling', 'surfing',
    'swimming', 'table tennis', 'tennis', 'track bicycle', 'trapeze',
    'tug of war', 'ultimate', 'uneven bars', 'volleyball', 'water cycling',
    'water polo', 'weightlifting', 'wheelchair basketball', 'wheelchair racing', 'wingsuit flying'
]

CLASS_SIZE = len(CLASS_NAMES) 

def create_model():
    base_model = DenseNet121(
        weights='imagenet',
        include_top=False,
        input_shape=IMAGE_SHAPE
    )
    
    base_model.trainable = True

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.3)(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.2)(x)
    predictions = Dense(CLASS_SIZE, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    return model

# load the model and weights
model = create_model()
model.load_weights('sport_classification.weights.h5')

def preprocess_image(image_bytes):
    # convert bytes to PIL Image
    image = Image.open(io.BytesIO(image_bytes))
    
    image = image.convert('RGB')
    
    # Resize image
    image = image.resize((224, 224))
    
    # Convert to numpy array
    image_array = np.array(image)
    
    # Expand dimensions
    image_array = np.expand_dims(image_array, axis=0)
    
    return image_array

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files or 'actual_class' not in request.form:
        return jsonify({'error': 'Image and actual class required'}), 400
    
    try:
        
        image_file = request.files['image'] #receive from user
        actual_class = request.form['actual_class'] #receive from user

        image_bytes = image_file.read()
        processed_image = preprocess_image(image_bytes)
        
        # get prediction
        predictions = model.predict(processed_image)
        predicted_class = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class])
        
        return jsonify({
            'predicted_class': CLASS_NAMES[predicted_class],
            'actual_class': CLASS_NAMES.index(actual_class),
            'confidence': confidence
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500