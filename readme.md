# Face Recognition System

Sistem pengenalan wajah berbasis deep learning dengan REST API, dibangun untuk tes PT Widya Inovasi Indonesia.

## Tech Stack
- **Python 3.9**: Bahasa pemrograman.
- **FastAPI**: Framework untuk REST API.
- **PostgreSQL**: Database untuk menyimpan embedding wajah.
- **facenet-pytorch**: Model pra-latih MTCNN (deteksi wajah) dan FaceNet (ekstraksi fitur).
- **Docker**: Untuk deployment.

## Prasyarat
- Python 3.9+
- Docker (opsional)
- PostgreSQL (jika tidak menggunakan Docker)

## Instalasi
1. Clone repositori:
   ```bash
   git clone <your-repo-url>
   cd face-recognition-system