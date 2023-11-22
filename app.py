from flask import Flask, request, jsonify
import face_recognition
import pickle
from supabase import create_client, Client
from io import BytesIO 
import numpy as np
import ast

app = Flask(__name__)

# Load Supabase credentials from environment variables
SUPABASE_URL = "SUPABASE_URL"
SUPABASE_API_KEY = "SUPABASE_API_KEY"

# Initialize Supabase client
supabaseClient: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

# Load the saved face encodings


@app.route('/registers', methods=['POST'])
def register_face():
    data = request.form
    name = data['name']

    # Load the image from the URL
    if 'image' not in request.files:
        return jsonify({'error': 'Image not found in the request'}), 400

    image_file = request.files['image']

    # Load the image from the file
    image = face_recognition.load_image_file(BytesIO(image_file.read()))
    
    # Find face locations and encodings
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)


    # Store face encodings in Supabase
    for face_encoding in face_encodings:
        supabaseClient.table('faces').upsert([{
            'name': name,
            'encoding': face_encoding.tolist()
        }]).execute()

    return jsonify({'message': 'Face registered successfully'})

@app.route('/recognize', methods=['POST'])
def recognize_face():

    response = supabaseClient.table('faces').select('name', 'encoding').execute().data
    print(response)
    supabase_data = response

    known_names = [entry['name'] for entry in supabase_data]
    known_encodings = [np.array(ast.literal_eval(entry['encoding'])).astype(float) for entry in supabase_data]

    if 'image' not in request.files:
        return jsonify({'error': 'Image not found in the request'}), 400

    image_file = request.files['image']

    # Load the image from the file
    image = face_recognition.load_image_file(BytesIO(image_file.read()))

    # Find face locations and encodings
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    # Compare each face in the frame with known faces
    recognized_faces = []

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]

        recognized_faces.append({'name': name})

    return jsonify({'recognized_faces': recognized_faces})

if __name__ == '__main__':
    app.run(port=8000, debug=True)
