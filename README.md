# Face Authentication Backend System

This project is a backend-based face registration and authentication system developed as part of an AI/ML Intern technical assignment.

The system allows a user to:
1. Register using name, email, and a face image.
2. Authenticate later using the same email and a different face image.
3. Verify identity by comparing stored and newly generated facial embeddings.

A pretrained open-source GitHub face recognition library, **DeepFace**, is used to perform face detection and face embedding extraction.

---

## Tech Stack Used

- Programming Language: Python  
- Backend Framework: Flask  
- Face Recognition Library: DeepFace (Facenet model)  
- Database: SQLite  
- Image Processing: OpenCV  
- API Testing: Postman  

---

## Why This Architecture?

### Flask
Flask was chosen because the assignment requires only lightweight REST APIs and no frontend. It keeps the implementation simple and modular.

### DeepFace
DeepFace is a free open-source GitHub facial recognition framework that provides pretrained face detection and embedding generation without requiring model training.

### SQLite
SQLite is used for persistent lightweight storage. It survives server restarts and allows efficient lookup using unique email IDs.

---

## Project Structure

face-auth-system/  
│── app.py  
│── database.py  
│── face_service.py  
│── requirements.txt  
│── README.md  
│── user_data.db  
│── uploads/  
│── sample_images/  

---

## Setup Instructions

### 1. Clone the repository

git clone <your_repository_link>  
cd face-auth-system  

---

### 2. Install dependencies

pip install -r requirements.txt  

---

### 3. Run the server

python app.py  

Server runs on:  
http://127.0.0.1:5000  

---

## API Endpoints

### POST /register

Registers a new user.

Form Data:
- name
- email
- image (JPEG/PNG)

Response:
{
  "success": true,
  "message": "User registered successfully"
}

---

### POST /authenticate

Authenticates a user.

Form Data:
- email
- image (JPEG/PNG)

Success Response:
{
  "success": true,
  "message": "Identity verified",
  "distance": 9.63
}

Failure Response:
{
  "success": false,
  "message": "Face does not match",
  "distance": 12.67
}

---

## Face Recognition Pipeline

### Registration Flow
1. User uploads face image.
2. System validates that exactly one face is present.
3. DeepFace generates facial embedding using Facenet model.
4. Data stored in SQLite database.

### Authentication Flow
1. User uploads new face image.
2. Stored embedding fetched using email.
3. New embedding generated.
4. Euclidean distance calculated.
5. If distance < 10 → verified  
6. Else → rejected  

---

## Threshold Selection

Threshold used: 10  

Observed values:
- Same person → ~9.63  
- Different person → ~12.67  

This threshold was selected based on testing with realistic variations.

---

## Storage Design

Database: SQLite (`user_data.db`)

Each record stores:
- id
- name
- email (unique)
- image path
- face embedding (stored as JSON string)

This ensures persistence across server restarts.

---

## Edge Cases Handled

- Duplicate email registration  
- Unknown email authentication  
- Non-face image rejection  
- Invalid image handling  
- Different user mismatch  

---

## Notes on Accuracy

Face recognition is not perfect. Minor false positives/negatives can occur under extreme conditions.

This system works reliably under:
- moderate lighting changes  
- small expression changes  
- different backgrounds  

For production improvement:
- better preprocessing  
- stricter thresholds  
- multiple model ensemble  
- quality filtering  

---

## Additional Notes

- UUID-based filenames are used to prevent file overwrite.
- Only valid face images are processed and stored.
- Backend APIs are designed to be tested via Postman as required.
