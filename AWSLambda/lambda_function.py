import json
import boto3
import io
import requests

FLASK_SERVER_URL = 'http://54.147.120.100:5000/predict'
EXPRESS_SERVER_URL = 'http://44.198.183.17:3000/display-classification'

s3Client = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    print(f"Bucket: {bucket}, Key: {key}")

    try:
        response = s3Client.get_object(Bucket=bucket, Key=key)

        # Check HTTP status code
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Image retrieved successfully!")
        else:
            print("Failed to retrieve the image.")
            return {
                'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
                'body': 'Error retrieving the object.'
            }

        # Get image content
        image_data = response['Body'].read()
        print(f"Retrieved {len(image_data)} bytes")

        files = {'image': ('image.jpg', image_data, 'image/jpeg')}
        flask_response = requests.post(FLASK_SERVER_URL, files=files)

        if flask_response.status_code == 200:
            # Get the result from Flask
            result = flask_response.json()
            print(f"Flask Response: {result}")

            # Send the result to the Express server
            classification_data = {
                'key': key,
                'class': result.get('predicted_digit'),
                'confidence': result.get('confidence')
            }
            express_response = requests.post(EXPRESS_SERVER_URL, json=classification_data)

            if express_response.status_code == 200:
                print("Successfully sent classification to Express server.")
            else:
                print(f"Error sending classification to Express server: {express_response.status_code}")
            
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }
        else:
            # Error response
            print(f"Flask Error: {flask_response.status_code}, {flask_response.text}")
            return {
                'statusCode': flask_response.status_code,
                'body': flask_response.text
            }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
