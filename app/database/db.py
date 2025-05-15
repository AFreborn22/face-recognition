from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import numpy as np

# Konfigurasi database
DATABASE_URL = "postgresql://postgres:root@localhost:5432/face_db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Face(Base):
    __tablename__ = "faces"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    embedding = Column(LargeBinary) 

# tabel
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def add_face(name: str, embedding: np.ndarray):
    """Menambahkan wajah ke database"""
    session = Session()
    embedding_bytes = embedding.tobytes()
    print(f"Panjang embedding sebelum di simpan: {len(embedding_bytes)}")
    face = Face(name=name, embedding=embedding_bytes)
    session.add(face)
    session.commit()
    face_id = face.id
    session.close()
    return face_id

def get_all_faces():
    """Dapatkan daftar semua wajah"""
    session = Session()
    faces = session.query(Face).all()
    result = [{"id": f.id, "name": f.name} for f in faces]
    session.close()
    return result

def delete_face(face_id: int):
    """Menghapus wajah berdasarkan ID"""
    session = Session()
    face = session.query(Face).filter(Face.id == face_id).first()
    if face:
        session.delete(face)
        session.commit()
        session.close()
        return True
    session.close()
    return False

def get_embedding(face_id: int):
    """Mendapatkan embedding wajah berdasarkan ID"""
    session = Session()
    face = session.query(Face).filter(Face.id == face_id).first()
    if face:
        embedding = np.frombuffer(face.embedding, dtype=np.float32)  
        session.close()
        return embedding
    session.close()
    return None