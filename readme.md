# Face Recognition System

## Deskripsi Proyek

Face recognition adalah teknologi penglihatan komputer untuk mengidentifikasi dan memverifikasi seseorang dari gambar digital atau frame video. Sistem ini bisa dipakai untuk berbagai keperluan, seperti keamanan, pengawasan, kontrol akses, dan lainnya.

Proyek ini membangun sistem pengenalan wajah dengan model deep learning, memanfaatkan **MTCNN** untuk deteksi wajah dan **Facenet** untuk ekstraksi fitur wajah.

---

## Struktur Folder

```
app/
├── api/
│   └── endpoints.py          # Kode untuk API endpoints (registrasi, pengenalan wajah, penghapusan data)
├── database/
│   └── db.py                # Kode untuk mengelola koneksi dan operasi database
├── models/
│   ├── face.py              # Kode untuk deteksi dan ekstraksi fitur wajah
│   ├── facenet_pretrained.onnx # Model pre-trained untuk ekstraksi fitur wajah (ONNX format)
│   └── schema.py            # Skema untuk validasi data
├── notebook/
│   ├── exportToOnnx.ipynb   # Notebook untuk mengekspor model ke format ONNX
│   ├── finetune.ipynb       # Notebook untuk melakukan finetuning model pre-trained
├── Dockerfile               # File untuk membangun Docker image
├── requirements.txt         # Daftar dependensi Python yang diperlukan
├── docker-compose.yml       # File konfigurasi untuk Docker Compose
├── facerecognition.postman_collection.json    # Postman collection untuk menguji API
└── readme.md                # Dokumentasi penggunaan aplikasi
```
---

## Model Pre-trained yang Digunakan

- **MTCNN (Multi-task Cascaded Convolutional Networks)**  
  Digunakan untuk deteksi wajah, menemukan dan mengidentifikasi lokasi wajah dalam gambar.

- **Facenet (ONNX)**  
  Digunakan untuk ekstraksi fitur wajah, menghasilkan representasi unik wajah untuk keperluan perbandingan dan pencocokan.

---

## Cara Menjalankan API menggunakan Docker

### Langkah-Langkah menggunakan image docker dari docker hub

1. **Pastikan Docker Desktop Terinstal**  

   Pastikan Docker Desktop terinstal di laptop/komputer

2. **Buat network untuk menghubungkan image app dan postgre**

   Buat jaringan Docker untuk menghubungkan container aplikasi dan PostgreSQL:
   ```bash
   docker network create my-network
   ```

3. **Pull dan Jalankan Container PostgreSQL** 

   Pull image PostgreSQL, lalu jalankan container
   ```bash
   docker pull postgres:14-alpine
   ```
   ```bash
   docker run --name db --network my-network -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=root -e POSTGRES_DB=face_db -p 5432:5432 -d postgres:14-alpine
   ```

4. **Pull dan Jalankan Container Aplikasi**

   Pull image aplikasi dari Docker Hub, lalu jalankan container
   ```bash
   docker pull afreborn/face-recognition-app:latest 
   ```
   ```bash
   docker run --name face-recognition --network my-network -e DATABASE_URL=postgresql://postgres:root@db:5432/face_db -e DB_HOST=db -e DB_PORT=5432 -e DB_USER=postgres -e DB_PASSWORD=root -e DB_NAME=face_db -p 8000:8000 -d afreborn/face-recognition-app:latest 
   ```

5. **periksa kontainer yang berjalan**

   ```bash
   docker ps 
   ```

### Langkah-Langkah jika menggunakan docker-compose

1. **Pastikan Docker Desktop Terinstal**  

   Pastikan Docker Desktop terinstal di laptop/komputer

2. **Kloning Repositori GitHub**  

   Clone repositori GitHub ini untuk mendapatkan file konfigurasi (`docker-compose.yml`) dan dokumentasi:
   ```bash
   git clone https://github.com/AFreborn22/face-recognition.git
   ```

3. **Masuk ke Direktori Proyek**  

   Masuk ke direktori proyek:
   ```bash
   cd face-recognition
   ```

4. **Inisialisasi Git LFS untuk Mengunduh File Model**  

   Inisialisasi Git LFS untuk mengunduh file model (`facenet_pretrained.onnx`):
   ```bash
   git lfs install
   git lfs pull
   ```
   - File `facenet_pretrained.onnx` di folder `app/models/` diperlukan untuk menjalankan aplikasi secara lokal. File ini dikelola menggunakan Git LFS karena ukurannya besar (>50 MB).

5. **Jalankan Aplikasi Menggunakan Docker Compose**  

   Jalankan aplikasi menggunakan Docker Compose:
   ```bash
   docker-compose up --build -d
   ```
   - Perintah ini akan menjalankan layanan `app` (aplikasi Face Recognition) dan `db` (database PostgreSQL) dalam jaringan yang sama, memastikan koneksi database berfungsi.
   - Opsi `--build` memastikan image dibangun ulang jika ada perubahan, dan `-d` menjalankan container di latar belakang.
   - Docker Compose akan secara otomatis menarik image `postgres:14` dari Docker Hub jika belum ada (memerlukan koneksi internet).

---

## Cara Menggunakan API

### **[GET] /api/face**  
Mengambil daftar semua wajah yang terdaftar dalam database.

```bash
curl http://localhost:8000/api/face
```

### **[POST] /api/face/register**  
Mendaftarkan wajah baru ke dalam database.

#### **Body (Form Data)**:
- `name`: Nama orang yang akan didaftarkan.  
- `file`: Gambar wajah yang akan didaftarkan.

#### **Contoh Menggunakan curl**:
```bash
curl -X POST -F "name=Akmal Fauzan" -F "file=@/path/to/your/image.jpg" http://localhost:8000/api/face/register
```

### **[POST] /api/face/recognize**  
Mencocokkan wajah yang diunggah dengan wajah yang terdaftar dalam database.

#### **Body (Form Data)**: 
- `file`: Gambar wajah yang akan dikenali.

#### **Contoh Menggunakan curl**:
```bash
curl -X POST -F "file=@/path/to/your/image.jpg" http://localhost:8000/api/face/recognize
```

### **[DELETE] /api/face/{id}**  
Menghapus wajah dari database berdasarkan ID.

#### **Contoh Menggunakan curl**:
```bash
curl -X DELETE http://localhost:8000/api/face/1
```

---

## Cara Menggunakan API jika memakai Postman

### 1. Impor Koleksi Postman
Impor file `facerecognition.postman_collection.json` untuk menguji API. Buka Postman, klik "Import", lalu pilih file JSON tersebut.

### 2. Menyiapkan Postman untuk Menggunakan API

#### **Endpoint [POST] /api/face/register**
- **URL**: `http://localhost:8000/api/face/register`
- **Method**: POST
- **Headers**:
  - `Content-Type: multipart/form-data`
- **Body**:
  - Pilih `form-data`.
  - Tambahkan dua field:
    - `Key: name` (value: nama orang yang akan didaftarkan, misalnya "Akmal Fauzan").
    - `Key: file` (value: pilih file gambar wajah dari komputer).

#### **Endpoint [POST] /api/face/recognize**
- **URL**: `http://localhost:8000/api/face/recognize`
- **Method**: POST
- **Headers**:
  - `Content-Type: multipart/form-data`
- **Body**:
  - Pilih `form-data`.
  - Tambahkan satu field:
    - `Key: file` (value: pilih file gambar wajah yang akan dikenali).

#### **Endpoint [GET] /api/face**
- **URL**: `http://localhost:8000/api/face`
- **Method**: GET  
Tidak perlu header atau body, cukup kirimkan permintaan GET untuk melihat daftar wajah yang terdaftar.

#### **Endpoint [DELETE] /api/face/{id}**
- **URL**: `http://localhost:8000/api/face/{id}`
- **Method**: DELETE  
Ganti `{id}` dengan ID wajah yang ingin dihapus (ID dapat dilihat setelah registrasi wajah menggunakan endpoint `/api/face/register`).

---
