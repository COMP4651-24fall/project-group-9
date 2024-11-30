In here you may find the code for the AWS Lambda function. 

You need to additionally create a trigger for the function with your S3 bucket as the source, that listens to PUT operations.

It is important to replace the following variables with the public IP addresses of the EC2 instances you created for the webapp and AI model respectivelly:

FLASK_SERVER_URL = 'http://<your_AImodel_EC2_public_IP>:5000/predict'

EXPRESS_SERVER_URL = 'http://<your_webapp_EC2_public_IP>:3000/display-classification'
