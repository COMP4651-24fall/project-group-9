import requests
from PIL import Image
import io

def test_prediction(image_path, api_url):
    # Open and convert image to bytes
    with open(image_path, 'rb') as image_file:
        files = {'image': image_file}

        # Make POST request
        response = requests.post(api_url, files=files)

        if response.status_code == 200:
            result = response.json()
            print(f"Predicted digit: {result['predicted_digit']}")
            print(f"Confidence: {result['confidence']:.4f}")
        else:
            print(f"Error: {response.json()}")

# Test the API
test_prediction('test_image.jpg', 'http://3.82.203.124:5000/predict')