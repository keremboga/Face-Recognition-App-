from flask import Flask, request, jsonify
from google.cloud import storage, firestore
import cv2
import numpy as np
from insightface.app import FaceAnalysis
from sklearn.metrics.pairwise import cosine_similarity

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import logging
import google.cloud.logging

# Logging configuration
logging.basicConfig(level=logging.DEBUG)
logging_client = google.cloud.logging.Client()
logging_client.setup_logging()

cred = credentials.Certificate("/app/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Firestore istemcisini başlatılır
db = firestore.Client()

app = Flask(__name__)
client = storage.Client()
bucket_name = 'case_images_cw'
bucket = client.bucket(bucket_name)

face_analyzer = FaceAnalysis()
face_analyzer.prepare(ctx_id=0, det_size=(640, 640))

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    image_path = data['image']
    person_id = data['id']

    # Initialize the verified variable
    verified = False

    logging.debug(f"Received image path: {image_path} for person_id: {person_id}")

    # Google Cloud Storage Bucket'ından görseller alınır.
    blob = bucket.blob(image_path)
    image_data = blob.download_as_bytes()
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Yüz analizi
    faces = face_analyzer.get(img)
    logging.debug(f"Detected faces in new image: {len(faces)}")

    if len(faces) == 1:
        new_face_embedding = faces[0].embedding
        logging.debug(f"New face embedding: {new_face_embedding}")

        # Aynı ID'ye sahip diğer veriler getirilir ve karşılaştırılır
        query = db.collection("identities").where("id", "==", person_id).where("verified", "==", True).get()

        if len(query) > 0:
            for doc in query:
                reference_image_path = doc.to_dict()['image']
                logging.debug(f"Comparing with reference image path: {reference_image_path}")
                
                blob2 = bucket.blob(reference_image_path)
                image_data2 = blob2.download_as_bytes()
                nparr2 = np.frombuffer(image_data2, np.uint8)
                img2 = cv2.imdecode(nparr2, cv2.IMREAD_COLOR)
                faces2 = face_analyzer.get(img2)
                logging.debug(f"Detected faces in reference image: {len(faces2)}")

                if len(faces2) == 1:
                    reference_face_embedding = faces2[0].embedding
                    logging.debug(f"Reference face embedding: {reference_face_embedding}")

                    # Yüzler aynı mı diye kontrol et
                    similarity = cosine_similarity([new_face_embedding], [reference_face_embedding])
                    logging.debug(f"Calculated similarity: {similarity[0][0]}")

                    if similarity[0][0] > 0.5:  # Benzerlik eşiği
                        verified = True
                        break

    logging.debug(f"Verification result: {verified}")
    return jsonify({'verified': verified})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080 , debug=True)
