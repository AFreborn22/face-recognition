from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.models.face import detect_and_extract_features
from app.database.db import add_face, get_all_faces, delete_face, get_embedding
from app.schema import FaceResponse
from PIL import Image
import io
from scipy.spatial.distance import cosine

router = APIRouter()

@router.get("/api/face", response_model=list[FaceResponse])
def get_faces():
    """Mengambil semua wajah yang terdaftar dari database"""
    faces = get_all_faces()
    if not faces:
        raise HTTPException(status_code=404, detail="Tidak ada wajah yang ditemukan dalam database.")
    return faces

@router.post("/api/face/register")
async def register_face(name: str = Form(...), file: UploadFile = File(...)):
    """Mendaftarkan wajah baru ke database."""
    if not name or not file:
        raise HTTPException(status_code=400, detail="Field 'nama' maupun 'file' diperlukan.")
    
    try:
        image = Image.open(io.BytesIO(await file.read())).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="File gambar tidak valid.")
    
    try:
        embedding = detect_and_extract_features(image)
        if embedding.shape[0] != 512:
            raise ValueError(f"Unexpected embedding dimension: {embedding.shape}. Expected (512,).")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Save to database
    face_id = add_face(name, embedding)
    return {"id": face_id, "name": name}

@router.post("/api/face/recognize")
async def recognize_face(file: UploadFile = File(...)):
    """Mengenali wajah dengan membandingkannya dengan wajah yang terdaftar dalam database."""
    # Read and validate the image
    try:
        image = Image.open(io.BytesIO(await file.read())).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="File gambar tidak valid.")
    
    # Extract embedding
    try:
        embedding = detect_and_extract_features(image)
        if embedding.shape[0] != 512:
            raise ValueError(f"Unexpected embedding dimension: {embedding.shape}. Expected (512,).")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Retrieve all faces from the database
    faces_db = get_all_faces()
    if not faces_db:
        raise HTTPException(status_code=404, detail="Tidak ada wajah yang terdaftar dalam database")
    
    # Compare embeddings
    for face in faces_db:
        db_embedding = get_embedding(face["id"])
        if db_embedding.shape[0] != 512:
            raise HTTPException(status_code=500, detail=f"Dimensi embedding yang tidak valid dalam database: {db_embedding.shape}.")
        
        similarity = 1 - cosine(embedding, db_embedding)
        if similarity > 0.9:  
            return {"id": face["id"], "name": face["name"]}
    
    raise HTTPException(status_code=404, detail="Tidak ditemukan kecocokan")

@router.delete("/api/face/{id}")
def delete_face_endpoint(id: int):
    """Menghapus wajah dari basis data berdasarkan ID."""
    if delete_face(id):
        return {"message": "Wajah berhasil dihapus"}
    raise HTTPException(status_code=404, detail="Wajah tidak ditemukan")