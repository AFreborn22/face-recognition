import onnxruntime as ort
import numpy as np
from PIL import Image
from facenet_pytorch import MTCNN
import torch

mtcnn = MTCNN(keep_all=False)
facenet_session = ort.InferenceSession("app/models/facenet_pretrained.onnx")

def preprocess_image(image: Image.Image, size=(160, 160)):
    image = image.convert("RGB")
    image = image.resize(size)
    img_array = np.array(image).astype(np.float32) / 255.0
    img_array = np.transpose(img_array, (2, 0, 1))
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def detect_faces(image: Image.Image):
    try:
        face, prob = mtcnn(image, return_prob=True)
        if face is None or prob < 0.9:
            raise ValueError("No face detected or confidence too low")
        return face
    except Exception as e:
        raise RuntimeError(f"Error during face detection: {e}")

def extract_features(face: torch.Tensor):
    if len(face.shape) == 3:  
        face = face.unsqueeze(0)  
    face_np = face.cpu().numpy()
    inputs = {facenet_session.get_inputs()[0].name: face_np}
    embedding = facenet_session.run(None, inputs)[0]
    return embedding.flatten()

def detect_and_extract_features(image: Image.Image):
    face = detect_faces(image)
    embedding = extract_features(face)
    return embedding