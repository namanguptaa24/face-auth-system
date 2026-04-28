from deepface import DeepFace
import numpy as np
import cv2


def validate_single_face(image_path):
    try:
        img = cv2.imread(image_path)

        if img is None:
            return False, "Invalid image file"

        analysis = DeepFace.extract_faces(
            img_path=image_path,
            detector_backend='opencv',
            enforce_detection=True
        )

        if len(analysis) == 0:
            return False, "No valid face detected in uploaded image"

        if len(analysis) > 1:
            return False, "Multiple faces detected. Please upload a single face image."

        return True, "Valid single face"

    except Exception:
        return False, "No valid face detected in uploaded image"


def generate_embedding(image_path):
    try:
        embedding = DeepFace.represent(
            img_path=image_path,
            model_name='Facenet',
            detector_backend='opencv',
            enforce_detection=True
        )

        return embedding[0]["embedding"]

    except Exception:
        return None


def compare_embeddings(embedding1, embedding2, threshold=10):
    emb1 = np.array(embedding1)
    emb2 = np.array(embedding2)

    distance = np.linalg.norm(emb1 - emb2)

    if distance < threshold:
        return True, distance
    else:
        return False, distance