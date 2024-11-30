import requests
import boto3
import json
from datetime import datetime

#replace with your own information if you need to test
# Sensitive info all deleted on here (related to AWS)
BUCKET_NAME = 'hkustclassificationresultbucket'  


def test_prediction(image_path, actual_class, api_url):
    with open(image_path, 'rb') as image_file:
        # create files and data dictionaries
        files = {'image': image_file}
        data = {'actual_class': actual_class}

        # make POST request with both image and actual class
        response = requests.post(api_url, files=files, data=data)

        if response.status_code == 200:
            result = response.json()
            print(f"Predicted class: {result['predicted_class']}")
            print(f"Actual class: {result['actual_class']}")
            print(f"Confidence: {result['confidence']:.4f}")

            # initialize S3 client
            # replace all id/key/token for testing
            s3_client = boto3.client('s3', 
                aws_access_key_id=aws_access_key_id,  
                aws_secret_access_key=aws_secret_access_key,  
                aws_session_token=aws_session_token, #remove it if you are not academic account
                region_name = 'us-east-1'                
                                    )
            
            prediction_record = {
                'predicted_class': result['predicted_class'],
                'actual_class': result['actual_class'] #assuming user know exactly the label name
            }

            # generate unique key (using timestamp as unique identifier)
            unique_key = f"prediction_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
            # upload to S3 as flat structure
            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=unique_key,
                Body=json.dumps(prediction_record),
                ContentType='application/json'
            )
        else:
            print(f"Error: {response.json()}")

        

# for testing the API

# test_prediction(
#     image_path='test_image.jpg',
#     actual_class='basketball', # Replace with actual sport class
#     api_url='http://3.82.203.124:5000/predict'
# )