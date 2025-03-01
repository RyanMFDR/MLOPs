# MLOPs


## 🛠️ Tools yang Digunakan
- **[Web Scraper Chrome Extension](https://chrome.google.com/webstore/detail/web-scraper)** untuk scraping data.
- **NLTK / spaCy** untuk preprocessing teks.
- **Pandas** untuk manipulasi data.

## 🚀 Cara Melakukan Scraping
1. **Install Web Scraper Chrome Extension**  
   - Download ekstensi dari [Web Scraper](https://chrome.google.com/webstore/detail/web-scraper).
   - Tambahkan ke Chrome.

2. **Konfigurasi Scraper**  
   - Buka website sumber data penelitian.
   - Gunakan fitur **Selector** pada ekstensi untuk memilih elemen judul penelitian.
   - Jalankan scraping dan ekspor hasil dalam format CSV/JSON.

3. **Simpan Data Hasil Scraping**  
   - Simpan file di folder `data/`, misalnya:
     ```
     data/research_titles_raw.csv
     ```

## 🛠️ Preprocessing Data
1. **Pastikan sudah install dependensi**  
   ```bash
   pip install -r requirements.txt
