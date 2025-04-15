import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import csv

def run_scraping(csv_file_path="../data/dataset.csv", log_dir="log"):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import os

    # --- Konfigurasi awal ---
    PATH = r"C:\Users\RyanMFDR\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    MAX_RETRY = 2
    WAIT = 5

    os.makedirs(log_dir, exist_ok=True)
    os.makedirs("data", exist_ok=True)

    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    driver = uc.Chrome(driver_executable_path=PATH, options=options, use_subprocess=True)
    driver.get("https://j-ptiik.ub.ac.id/index.php/j-ptiik/issue/archive")
    time.sleep(3)

    # Scroll Lazy Loading
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Ambil semua link
    titles = driver.find_elements(By.CLASS_NAME, "title")
    hrefs = [(title.text.strip(), title.get_attribute('href')) for title in titles if title.text.strip() != ""]

    print(f"\n✅ Total link ditemukan: {len(hrefs)}\n")

    # LOGGING
    success_log = open(f"{log_dir}/log_sukses.txt", "w", encoding="utf-8")
    failed_log = open(f"{log_dir}/log_gagal.txt", "w", encoding="utf-8")

    # Simpan ke CSV
    with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Judul", "Penulis", "Tanggal", "Keyword", "Abstrak", "Link"])

        for label, link in hrefs:
            attempt = 0
            while attempt < MAX_RETRY:
                try:
                    driver.get(link)
                    print(f"✅ Berhasil mengunjungi: {label}")
                    success_log.write(f"{label} - {link}\n")
                    time.sleep(WAIT)

                    # Artikel
                    articles = driver.find_elements(By.XPATH, "//a[starts-with(@id, 'article-')]")
                    article_links = [(a.text.strip(), a.get_attribute("href")) for a in articles if a.text.strip() != ""]

                    print(f"📝 {label} - Jumlah artikel ditemukan: {len(article_links)}")
                    for title, art_link in article_links:
                        print(f"    • {title} -> {art_link}")

                        driver.get(art_link)
                        time.sleep(2)

                        try:
                            # Judul
                            judul = driver.find_element(By.CLASS_NAME, "page_title").text.strip()

                            # Penulis
                            authors_ul = driver.find_element(By.CLASS_NAME, "authors")
                            authors_li = authors_ul.find_elements(By.TAG_NAME, "li")
                            penulis = []
                            for li in authors_li:
                                try:
                                    nama = li.find_element(By.CLASS_NAME, "name").text.strip()
                                except:
                                    nama = "Nama tidak ditemukan"
                                try:
                                    affil = li.find_element(By.CLASS_NAME, "affiliation").text.strip()
                                except:
                                    affil = "-"
                                penulis.append(f"{nama} ({affil})")
                            penulis_str = ", ".join(penulis)

                            # Tanggal publikasi
                            tanggal = driver.find_element(By.XPATH, "/html/body/main/div[1]/article/div/div[2]/div[2]/section/div/span").text.strip()

                            # Abstrak
                            try:
                                abstrak_section = driver.find_element(By.CLASS_NAME, "abstract")
                                abstrak_paragraphs = abstrak_section.find_elements(By.TAG_NAME, "p")
                                abstrak = abstrak_paragraphs[0].text.strip() if abstrak_paragraphs else "Tidak ditemukan"
                            except:
                                abstrak = "Tidak ditemukan"

                            # Keyword
                            try:
                                keyword_section = driver.find_element(By.CLASS_NAME, "keywords")
                                keyword = keyword_section.find_element(By.CLASS_NAME, "value").text.strip()
                            except:
                                keyword = "Tidak tersedia"

                            # Simpan ke CSV
                            writer.writerow([judul, penulis_str, tanggal, keyword, abstrak, art_link])
                            print(f"✅ CSV Updated")

                        except Exception as e:
                            print("❌ Error mengambil data artikel:", e)

                    break  # keluar dari retry loop

                except Exception as e:
                    attempt += 1
                    print(f"❌ Gagal ({attempt}/{MAX_RETRY}) mengunjungi {label}: {e}")
                    if attempt == MAX_RETRY:
                        failed_log.write(f"{label} - {link} - ERROR: {e}\n")
                    time.sleep(3)

    success_log.close()
    failed_log.close()
    driver.quit()
    print("🎉 Scraping selesai!")

# Untuk uji manual (opsional)
if __name__ == "__main__":
    run_scraping()
