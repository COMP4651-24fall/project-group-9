from flask import Flask, request, jsonify
import torch
import torch.nn as nn
from PIL import Image
import io
import torchvision.transforms as transforms
import numpy as np

app = Flask(__name__)

# Define the same CNN architecture
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3)
        self.fc1 = nn.Linear(64 * 24 * 24, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = torch.flatten(x, 1)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load the model
model = SimpleCNN()
model.load_state_dict(torch.load('mnist_cnn.pth', 
                                 weights_only=True,
                                 map_location=device))
model.eval()
model.to(device)

# Define the same transforms used during training
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),  # Convert to grayscale
    transforms.Resize((28, 28)),  # MNIST size
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

def preprocess_image(image_bytes):
    # Convert bytes to PIL Image
    image = Image.open(io.BytesIO(image_bytes))
    
    # Apply transforms
    image_tensor = transform(image)
    
    # Add batch dimension
    image_tensor = image_tensor.unsqueeze(0)
    
    return image_tensor

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    try:
        image_file = request.files['image']
        image_bytes = image_file.read()
        image_tensor = preprocess_image(image_bytes)
        
        # Move tensor to device
        image_tensor = image_tensor.to(device)
        
        # Get prediction
        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_class].item()
        
        return jsonify({
            'predicted_digit': predicted_class,
            'confidence': float(confidence)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)