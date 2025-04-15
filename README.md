# MLOPs Kelompok 'Ber-3'

### 🧍Anggota

- Ryan Muhammad Firdaus (225150207111076)
- Arion Syemael Siahaan (225150207111060)
- Ashbahul Danna Yunas (225150201111022)

Selamat datang Pak Rizal di Kelompok kami🙌
Pada projek ini, Kami berfokus dalam Analisis Tren Topik dalam Jurnal PTIIK 2023-2025 menggunakan BERTopic

🔗 **https://docs.google.com/document/d/1RCNP4xn6RzWeGiKqxZQ76S2KLyuNqenUCKmMNqGPgsI/edit?tab=t.0**

### 📊 Sumber Data

🔗 **https://j-ptiik.ub.ac.id/index.php/j-ptiik/issue/archive**

---

### 📅 Future Improvements & Update

| Tanggal    | Update Proyek                                        | Status         |
| ---------- | ---------------------------------------------------- | -------------- |
| 2025-04-15 | **5. Implementasi Topic Modelling**                  | 🟨 On Progress |
| 2025-04-15 | **4. Services**                                      | 🟨 On Progress |
| 2025-04-15 | **3.2 Update Eksplorasi Data & Feature Engineering** | ✅ Selesai     |
| 2025-04-15 | **3.1 Update Scrapper**                              | ✅ Selesai     |
| 2025-03-23 | **3. Eksplorasi Data**                               | ✅ Selesai     |
| 2025-03-01 | **2. Preprocessing**                                 | ✅ Selesai     |
| 2025-03-01 | **Initial commit : Scrapping**                       | ✅ Selesai     |

### 🗃️ Struktur Direktori

<pre>MLOPs/ 
├── data/
      ├── dataset.csv 
├── notebooks/
      ├── scraping.ipynb
      ├── preprocess.ipynb
├── README.md
├── requirements.txt 
└── .gitignore # File yang di-ignore </pre>

### 🛠️ Tools yang Digunakan

- **Selenium**

  => mengotomatisasi browser dan mengambil data dari web secara dinamis.

- **Undetected Chromedriver**

  =>Versi modifikasi dari ChromeDriver yang mampu menghindari deteksi anti-bot.

---

### 🌐 Proses Scraping Data

1. **Inisialisasi Browser**

   Menggunakan _undetected-chromedriver_ untuk menjalankan browser secara headless dan menghindari pemblokiran dari website target.

2. **Akses Halaman Arsip Jurnal**

   URL target: https://j-ptiik.ub.ac.id/index.php/j-ptiik/issue/archive
   Scraper mengakses daftar edisi jurnal yang tersedia.

3. **Scroll Otomatis**

   Auto-scroll hingga mencapai bagian paling bawah halaman untuk mengatasi lazy loading.

4. **Mengumpulkan Link Jurnal**

   Mengambil seluruh elemen berisi judul dan link edisi menggunakan class .title.

5. **Kunjungi Setiap Edisi**

   Dari masing-masing link edisi, scraper mengekstrak semua artikel yang tersedia.

6. **Ambil Data Artikel**

   Informasi yang diambil dari masing-masing artikel:

   - Judul
   - Nama dan afiliasi penulis
   - Tanggal publikasi
   - Abstrak
   - Keyword (kata kunci)
   - Link artikel

7. **Simpan ke File CSV**
   Data disimpan langsung ke file dataset.csv

---

### 💻 Preprocessing Data

Setelah data dikumpulkan melalui proses scraping, langkah selanjutnya adalah membersihkan dan mempersiapkan data agar siap untuk analisis menggunakan BERTopic.

#### 1. **Pembersihan Teks**

- Pada tahap ini, data teks seperti abstrak artikel dibersihkan dari elemen-elemen yang tidak relevan, seperti tanda baca, angka, dan karakter khusus.
- Semua teks juga diubah menjadi huruf kecil untuk memastikan konsistensi dan menghindari duplikasi kata yang sebenarnya sama tetapi ditulis dengan kapitalisasi yang berbeda.

#### 2. **Tokenisasi**

- **Tokenisasi** adalah proses memecah teks menjadi unit-unit terkecil yang disebut token. Dalam konteks ini, token biasanya berupa kata-kata yang membentuk kalimat. Proses ini sangat penting karena memungkinkan model untuk memahami dan menganalisis kata-kata secara terpisah.

#### 3. **Penghapusan Stopwords**

- **Stopwords** adalah kata-kata umum yang sering muncul dalam bahasa sehari-hari, namun tidak memiliki makna penting dalam konteks analisis teks, seperti "dan", "atau", "yang", dan sebagainya.
- Menghapus stopwords membantu mengurangi noise dalam data dan memfokuskan analisis pada kata-kata yang lebih relevan.

#### 4. **Lematisasi (Opsional)**

- **Lematisasi** adalah proses mengubah kata menjadi bentuk dasarnya (lemma), sehingga variasi bentuk kata seperti "makan", "memakan", "makanlah" dapat diubah menjadi kata dasar yang sama, yaitu "makan".
- Lematisasi sangat membantu dalam menyederhanakan data dan mengurangi jumlah kata yang harus dianalisis.

#### 5. **Penyimpanan Data yang Sudah Diproses**

- Setelah seluruh langkah preprocessing selesai, data yang sudah dibersihkan dan diproses disimpan ke dalam format yang siap digunakan, seperti **CSV**, agar mudah diakses dan digunakan dalam analisis lebih lanjut.
