import express from 'express';
import multer from 'multer';
import cors from 'cors';
import dotenv from 'dotenv';
import AWS from 'aws-sdk';
import path from 'path';

const __dirname = path.dirname(new URL(import.meta.url).pathname);
dotenv.config({ path: path.resolve(__dirname, '../.env') });

const app = express();

app.use(cors());

const upload = multer();

if (!process.env.AWS_ACCESS_KEY_ID || 
    !process.env.AWS_SECRET_ACCESS_KEY || 
    !process.env.AWS_BUCKET_NAME || 
    !process.env.AWS_ACCESS_TOKEN) {
  throw new Error('Missing required AWS environment variables');
}

console.log('AWS Access Key ID:', process.env.AWS_ACCESS_KEY_ID);
console.log('AWS Secret Access Key:', process.env.AWS_SECRET_ACCESS_KEY);
console.log('AWS Bucket Name:', process.env.AWS_BUCKET_NAME);

const s3 = new AWS.S3({
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  sessionToken: process.env.AWS_ACCESS_TOKEN, // Only needed for temporary credentials
  region: 'us-east-1'
});

let predictions = {};

app.post('/upload', upload.single('file'), async (req, res) => {
  try {
    const file = req.file;

    if (!file) {
      return res.status(400).send({ message: 'No file uploaded' });
    }

    const allowedTypes = ['image/jpeg', 'image/png'];
    if (!allowedTypes.includes(file.mimetype)) {
      return res.status(400).send({ message: 'Invalid file type' });
    }

    if (file.size > 5 * 1024 * 1024) {
      return res.status(400).send({ message: 'File size exceeds limit' });
    }

    // Configure S3 upload parameters
    const params = {
      Bucket: process.env.AWS_BUCKET_NAME,
      Key: file.originalname, // Original file name
      Body: file.buffer, // File content
      ContentType: file.mimetype, // File MIME type
    };

    // Upload to S3
    await s3.putObject(params).promise();

    predictions[file.originalname] = { status: 'processing' };

    res.status(200).send({ message: 'File uploaded successfully', fileName: file.originalname });

  } catch (error) {
    console.error('Unexpected error:', error);
    res.status(500).send({ message: 'Internal Server Error' });
  }
});

app.post('/display-classification', express.json(), (req, res) => {
  const { key: key, class: classification, confidence } = req.body;

  if (!classification || !confidence) {
    return res.status(400).send({ message: 'Invalid data received' });
  }

  console.log(`Received classification: ${classification}, confidence: ${confidence}`);

  predictions[key] = {
    status: 'complete',
    result: { classification, confidence },
  };

  res.status(200).send({ message: 'Classification result received', classification, confidence });
});

app.get('/get-prediction/:uploadId', (req, res) => {
  const { uploadId } = req.params;

  if (predictions[uploadId]) {
    if (predictions[uploadId].status === 'complete') {
      return res.status(200).send({
        prediction: predictions[uploadId].result.classification, // Return prediction result
        confidence: predictions[uploadId].result.confidence,
      });
    } else {
      return res.status(200).send({ prediction: null }); // Prediction is still being processed
    }
  }

  res.status(404).send({ message: 'Prediction not found' });
});


app.listen(3000, () => {
  console.log('Server is running on http://localhost:3000');
});
