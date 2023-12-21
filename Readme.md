# REST API PYTHON
## 1. Persiapkan DB
Dalam app ini saya pakai XAMPP/MySQ yang bisa di setting apada file .env.

## 2. Buat Database dan Table
Untuk database bebas bisa dengan nama apa saja. Tapi disarankan dengan nama 'universias'. Untuk membuat table silahkan menjalankan query berikut. 

    CREATE TABLE IF NOT EXISTS dosen (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(50) NOT NULL,
    univ VARCHAR(50) NOT NULL,
    jurusan VARCHAR(50) NOT NULL
    );

## 3. Install Package
Sebelum menjalankan aplikasi diharuskan  menginstall package terlebih dahulu. Bisa menggunakan command berikut :

    pip install -r requirements.txt

## 4. Jalankan aplikasi
Untuk menjalankan aplikasi menggunakan command berikut :

    py app.py

atau

    pyhton app.py

atau

    python3 app.py

## 5. Routes
Untuk routes yang digunakan diantaranya :

1. [GET] http://localhost:8080/dosen
2. [POST] http://localhost:8080/dosen
3. [GET] http://localhost:8080/dosen/<int:id>
4. [PUT] http://localhost:8080/dosen/<int:id>
5. [PATCH] http://localhost:8080/dosen/<int:id>
6. [DELETE] http://localhost:8080/dosen/<int:id>