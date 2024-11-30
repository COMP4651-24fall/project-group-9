1. Demonstration model for User interaction:

mnist_cnn.pth contains a Convolutional Neural Network we trained on the mnist dataset to classify images of digits. 

To run the model part of the project:

Start an EC2 instance in AWS (different than the one used for the webapp). We used an EC2 Ubuntu t3.large instance with 30GB of disk storage. Modify the security group inbound rules to allow TCP traffic from any IP.

Connect to the instance through SSH. Follow the instructions in the instruction_to_setup_ec2.txt file found in this repository to install the necessary requirements.

Please use 

pip install "numpy<2"

in case an error with the version shows when running the code.

Note: the send_request.py isn't used to run the project and it was just used for testing. Additionally, the photo provided in this repo is just a reference of a photo you may use for testing, but any other can be used as well.

2. The actual model which is connected to S3:

IMPORTANT Note: our project also has participated in data analytics based on the Sport Classification Model. Detail is in "COMP4651ProjectModel.ipynb". The model should be the main model of our project instead of the "DigitRecoginiton.ipynb". To make things simple, we use "DigitRecoginiton.ipynb" for the demonstration of the process from user sending request to the part that EC2 respond with predicted result.

Besides, sport_classification.weights.h5 is the weight information of a DenseNet architecture we trained on the sports dataset reference: https://www.kaggle.com/datasets/gpiosenka/sports-classification. The corresponding py file is classification_with_s3.py and send_request_with_s3.py.
for "classification_with_s3.py": It contains the the sport classification model which can put in the EC2 instance.

For "classification_with_s3.py", the difference between it and classification.py is that it will also return the label value corresponding to the user actual class name.

For "send_request_with_s3.py", the difference between it and "send_request.py" is that it also perform write operation to the S3 bucket, so that when we need to collect data to evaluate the result using Hadoop, we can directly retrieve it from the S3 and process the data in distribution manner in Hadoop (detail for the Hadoop implementation, you can check the directory "accuracy-checker). 

To simply the complexity, we decide not use the implementation of classification_with_s3.py and send_request_with_s3.py for lambda function for make things more understandable, but just show the code here. Although such part is not integrated, the operation for getting classification result and send to S3 are all tested and workable.
