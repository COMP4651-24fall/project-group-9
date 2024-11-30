import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FileUpload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [prediction, setPrediction] = useState<string | null>(null);
  const [confidence, setConfidence] = useState<string | null>(null);
  const [selected, setSelected] = useState<string | null>(null);
  const [uploadId, setUploadId] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const uploadedFile = event.target.files?.[0] || null;
    setFile(uploadedFile);

    if (uploadedFile) {
      setSelected(`Selected: ${uploadedFile.name}`);
      setPreview(URL.createObjectURL(uploadedFile));
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:3000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setSuccess('File uploaded successfully');
      setUploadId(response.data.fileName); // Store the upload ID (or file name)
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  // Polling for the prediction result
  useEffect(() => {
    if (!uploadId) return;

    const intervalId = setInterval(async () => {
      try {
        const result = await axios.get(`http://localhost:3000/get-prediction/${uploadId}`);
        console.log("Result:", result.data);
        if (result.data.prediction) {
          console.log("Prediction:", result.data.prediction);
          setPrediction(result.data.prediction);
          setConfidence(result.data.confidence);
          clearInterval(intervalId); // Stop polling when we get the prediction
        }
      } catch (error) {
        console.error('Error fetching prediction:', error);
      }
    }, 2000); // Poll every 2 seconds

    return () => clearInterval(intervalId); // Clean up the interval on component unmount
  }, [uploadId]);

  return (
    <div className="upload-container">
      <div className="upload-header">
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="file-input"
          id="file-input"
        />
      </div>
      <label htmlFor="file-input" className="file-input-label">
        Choose a File
      </label>
      {selected && <p className="selected-msg">{selected}</p>}
      {preview && (
        <div className="image-preview">
          <img src={preview} alt="Preview" className="preview-img" />
        </div>
      )}
      <button onClick={handleUpload} className="upload-btn">Classify</button>
      {success && <p className="success-msg">{success}</p>}
      {prediction && <p className="prediction-msg">Prediction: {prediction}</p>}
      {confidence && <p className="confidence-msg">Confidence: {confidence}</p>}
    </div>
  );
};

export default FileUpload;
