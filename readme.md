# Face Recognition System

## Deskripsi Proyek

Face recognition adalah teknologi penglihatan komputer untuk mengidentifikasi dan memverifikasi seseorang dari gambar digital atau frame video. Sistem ini bisa dipakai untuk berbagai keperluan, seperti keamanan, pengawasan, kontrol akses, dan lainnya.

Proyek ini membangun sistem pengenalan wajah dengan model deep learning, memanfaatkan **MTCNN** untuk deteksi wajah dan **Facenet** untuk ekstraksi fitur wajah.

---

## Struktur Folder

```
app/
├── api/
│   └── endpoints.py
├── database/
│   └── db.py
├── models/
│   ├── face.py
│   ├── facenet_pretrained.onnx
│   └── schema.py
├── notebook/
│   ├── exportToOnnx.ipynb
│   ├── finetune.ipynb
├── Dockerfile
├── requirements.txt
├── docker-compose.yml
└── readme.md
```

- **app/api/endpoints.py**  
  Berisi kode REST API untuk menangani permintaan seperti registrasi, pengenalan wajah, dan penghapusan data wajah.

- **app/database/db.py**  
  Berisi kode untuk mengelola database, termasuk menyimpan dan mengambil data wajah.

- **app/models/face.py**  
  Berisi skrip untuk deteksi wajah dan ekstraksi fitur wajah menggunakan model pre-trained MTCNN dan Facenet.

- **app/models/facenet_pretrained.onnx**  
  Model pre-trained untuk ekstraksi fitur wajah dalam format ONNX.

- **app/notebook/exportToOnnx.ipynb**  
  Notebook untuk mengekspor model ke format ONNX.

- **app/notebook/finetune.ipynb**  
  Notebook untuk melakukan finetuning pada model pre-trained.

- **Dockerfile**  
  File untuk membuat Docker image.

- **docker-compose.yml**  
  File untuk mengatur konfigurasi Docker Compose.

- **requirements.txt**  
  Daftar dependensi yang diperlukan untuk menjalankan aplikasi.

- **readme.md**  
  Dokumentasi penggunaan aplikasi.

---

## Model Pre-trained yang Digunakan

- **MTCNN (Multi-task Cascaded Convolutional Networks)**  
  Digunakan untuk deteksi wajah, menemukan dan mengidentifikasi lokasi wajah dalam gambar.

- **Facenet (ONNX)**  
  Digunakan untuk ekstraksi fitur wajah, menghasilkan representasi unik wajah untuk keperluan perbandingan dan pencocokan.

---

## Cara Menjalankan Docker Image dari DockerHub

### Menggunakan Docker Pull

Setelah image diunggah ke DockerHub, tarik image dengan perintah berikut. Ganti `<dockerhub_username>/<image_name>` dengan nama pengguna dan nama image di DockerHub.

```bash
docker pull <dockerhub_username>/<image_name>
```

Jalankan container dengan perintah berikut:

```bash
docker run -p 8000:8000 <dockerhub_username>/<image_name>
```

Alternatifnya, jika menggunakan Docker Compose:

```bash
docker-compose up
```

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
- `name`: Nama orang yang ingin dikenali.  
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

## Cara Menggunakan Postman

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