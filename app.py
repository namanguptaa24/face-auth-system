from flask import Flask, request, jsonify
import os
import json
import uuid


from database import init_db, save_user, get_user_by_email
from face_service import validate_single_face, generate_embedding, compare_embeddings

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()


@app.route("/")
def home():
    return "Face Authentication Backend Running"


@app.route("/register", methods=["POST"])
def register():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        image = request.files.get("image")

        if not name or not email or not image:
            return jsonify({"success": False, "message": "Name, email and image are required"}), 400

        existing_user = get_user_by_email(email)
        if existing_user:
            return jsonify({"success": False, "message": "Email already registered"}), 400

        # image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        # image.save(image_path)
        unique_filename = str(uuid.uuid4()) + "_" + image.filename
        image_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        image.save(image_path)
 
        valid, msg = validate_single_face(image_path)
        if not valid:
            if os.path.exists(image_path):
                os.remove(image_path)
            return jsonify({"success": False, "message": "No valid face detected in uploaded image"}), 400
        
        embedding = generate_embedding(image_path)
        if embedding is None:
            return jsonify({"success": False, "message": "Embedding generation failed"}), 500

        save_user(name, email, image_path, embedding)

        return jsonify({
            "success": True,
            "message": "User registered successfully"
        })

    # except Exception as e:
    #     return jsonify({"success": False, "message": str(e)}), 500
    except Exception:
        return jsonify({"success": False, "message": "Registration failed due to invalid face input"}), 500

@app.route("/authenticate", methods=["POST"])
def authenticate():
    try:
        email = request.form.get("email")
        image = request.files.get("image")

        if not email or not image:
            return jsonify({"success": False, "message": "Email and image are required"}), 400

        user = get_user_by_email(email)
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        stored_embedding = json.loads(user[4])

        #image_path = os.path.join(UPLOAD_FOLDER, "auth_" + image.filename)
        #image.save(image_path)
        unique_filename = "auth_" + str(uuid.uuid4()) + "_" + image.filename
        image_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        image.save(image_path)

        # valid, msg = validate_single_face(image_path)
        # if not valid:
        #     return jsonify({"success": False, "message": msg}), 400
        # valid, msg = validate_single_face(image_path)
        # if not valid:
        #     return jsonify({"success": False, "message": "No valid face detected in uploaded image"}), 400

        valid, msg = validate_single_face(image_path)
        if not valid:
            if os.path.exists(image_path):
              os.remove(image_path)
            return jsonify({"success": False, "message": "No valid face detected in uploaded image"}), 400
        
        new_embedding = generate_embedding(image_path)
        if new_embedding is None:
            return jsonify({"success": False, "message": "Embedding generation failed"}), 500

        matched, distance = compare_embeddings(stored_embedding, new_embedding)

        if matched:
            return jsonify({
                "success": True,
                "message": "Identity verified",
                "distance": float(distance)
            })
        else:
            return jsonify({
                "success": False,
                "message": "Face does not match",
                "distance": float(distance)
            })

    # except Exception as e:
    #     return jsonify({"success": False, "message": str(e)}), 500
    except Exception:
        return jsonify({"success": False, "message": "Authentication failed due to invalid face input"}), 500

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=False)