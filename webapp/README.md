Start an EC2 instance in AWS. We used an EC2 Ubuntu t3.large instance with 30GB of disk storage. Modify the security group inbound rules to allow TCP traffic from any IP.

Connect to the instance through SSH. Install the necessary requirements for the project.

Mainly:

sudo apt update

sudo apt-get install nodejs

sudo apt install npm

// After running the command bellow, giva a name for the project and choose React and Typescript as the development tools

npm create vite@latest

npm install axios

npm install express

npm install multer

npm install cors

npm install dotenv

npm install aws-sdk

After installing all the necessary requirements, remove all the files inside the src/ directory that has been created inside your Vite project and replace them with the ones that you cloned in this directory (you may use scp command in your local machine to achieve this).

Additionally, in the webapp dir, add a .env file. You need to specify the following credentials of your AWS account to be able to send images to S3:

AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_ACCESS_TOKEN=...
AWS_BUCKET_NAME=...

AWS_ACCESS_TOKEN is needed only for temporary credentials (like AWS Lab environment), and in AWS_BUCKET_NAME you need to specify the name of your S3 bucket. Additionally, be careful to indicate your own region in the server.js code (we used us-east-1).

#
Frontend:

To start the frontend, run the following command:

npm run dev

An http link will be displayed that can be opened in a web browser. However, to see the UI in you local machine, you need to replace the IP inside the http link with the public IP address of the EC2 instance in which the Vite project is running on.


#
Backend:

Open a new terminal in your local computer and connect to the same EC2 instance with SSH. cd into the backend/ dir and run the command:

node server.js

#

Now you can use the UI to send images from your local device to the backend!!

