# Face Recognition API with Flask

This repository contains a simple REST API for face recognition using Flask in Python.

## Installation

To install the project dependencies, use the following command:

```bash
pip install -r requirements.txt
```
How to Run

To run the project, execute the following command:

```bash
python app.py
```

The API will be accessible at http://localhost:8000.

Endpoints

1. /registers
Description

Endpoint for face registration.

Method

POST
Parameters

name (text): The name associated with the registered face.
image (multiple images): Multiple face images for registration.
Example

```bash
curl -X POST -F "name=John Doe" -F "image=@image1.jpg" -F "image=@image2.jpg" http://localhost:5000/registers
```
2. /recognize
Description

Endpoint for face recognition.

Method

POST
Parameters

image (single image): The face image to be recognized.
Example

```bash
curl -X POST -F "image=@image_to_recognize.jpg" http://localhost:8000/recognize
```
