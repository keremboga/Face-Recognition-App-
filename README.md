Face Verification System
This project implements a face verification system using Firebase Firestore, Google Cloud Storage, and a Python Flask backend with the InsightFace library for face analysis. The system consists of Firebase Cloud Functions that trigger on Firestore events, and a Python backend that performs face verification by comparing facial embeddings.

Overview
The face verification system works as follows:

-A new document is added to the Firestore collection identities.
-A Firebase Cloud Function triggers on the creation of the document.
-The Cloud Function checks if there are other documents with the same id in Firestore:
-If no other document with the same id exists, the document is marked as verified.
-If other documents with the same id exist, the function sends a request to the Python backend for face verification.
-The Python backend retrieves the images from Google Cloud Storage, performs face analysis using the InsightFace library, and compares the facial embeddings.
-The verification result is sent back to Firestore, and the document is updated accordingly.

Prerequisites
-Docker
-Firebase CLI
-Google Cloud SDK
-A Firebase project
-A Google Cloud project

Project Structure
functions/: Contains Firebase Cloud Functions code.
app.py: The main Python backend application file.
Dockerfile: Docker configuration for the Python backend.
firebase_project/index.js = Nodejs cloud function. 
serviceAccountKey.json: Firebase service account key for accessing Firestore. (I did not push this file into repo because this file includes my private key.)

Setup
-Install Firebase CLI:
npm install -g firebase-tools
-Initialize Firebase in your project directory:
firebase init

Deploy Firebase Cloud Functions:
cd functions
firebase deploy --only functions

-Docker image build and Push into GCR
docker buildx create --use
docker buildx build --platform linux/amd64 -t gcr.io/YOUR_PROJECT_ID/your_image_name --push .

-Deploy image in GCR 
gcloud run deploy your_service_name \
  --image gcr.io/YOUR_PROJECT_ID/your_image_name  \
  --platform managed \
  --region YOUR_REGION \
  --allow-unauthenticated



