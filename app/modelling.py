import os
import pandas as pd
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from gensim.corpora import Dictionary
from gensim.models.coherencemodel import CoherenceModel
import threading
from prometheus_client import start_http_server, Gauge

def load_and_prepare_data(file_path: str, text_columns: list) -> pd.DataFrame:
    if not os.path.exists(file_path):
        print(f"Error: File tidak ditemukan di {file_path}")
        return None
    
    print(f"Memuat data dari {file_path}...")
    df = pd.read_csv(file_path)
    
    # Gabungkan kolom teks yang ditentukan (misal: ['Title', 'Abstrak'])
    df['text_gabungan'] = df[text_columns].fillna('').agg(' '.join, axis=1)
    
    print("Data berhasil dimuat dan kolom 'text_gabungan' telah dibuat.")
    return df

def train_bertopic_model(docs: list, embedding_model_name: str, min_topic_size: int) -> BERTopic:
    print(f"Melatih model BERTopic dengan embedding '{embedding_model_name}'...")
    embedding_model = SentenceTransformer(embedding_model_name)
    
    topic_model = BERTopic(
        embedding_model=embedding_model,
        language="multilingual",
        min_topic_size=min_topic_size,
        verbose=True
    )
    
    topics, _ = topic_model.fit_transform(docs)
    print("Pelatihan model BERTopic selesai.")
    return topic_model, topics

def calculate_coherence_score(topic_model: BERTopic, docs: list) -> float:
    print("Menghitung Coherence Score...")
    # Tokenisasi dokumen (di-split berdasarkan spasi karena sudah di-preprocess)
    tokenized_docs = [doc.split() for doc in docs]
    
    # Dapatkan dictionary dari semua topik yang dihasilkan oleh model
    topics = topic_model.get_topics()
    
    # PERBAIKAN DI SINI:
    # Kita akan membangun list of lists yang berisi kata-kata per topik.
    topic_words = []
    # Iterasi melalui setiap topik yang ada di dalam model
    for topic_id in topics:
        # Lewati topik outlier (-1) karena tidak relevan untuk koherensi
        if topic_id == -1:
            continue
        
        # Ambil HANYA kata-katanya saja dari pasangan (kata, skor)
        words_in_topic = [word for word, score in topics[topic_id]]
        topic_words.append(words_in_topic)
    
    # Buat dictionary dan corpus Gensim
    dictionary = Dictionary(tokenized_docs)
    
    # Hitung Coherence
    coherence_model = CoherenceModel(
        topics=topic_words,
        texts=tokenized_docs,
        dictionary=dictionary,
        coherence='c_v'
    )
    
    coherence_score = coherence_model.get_coherence()
    print(f"Coherence Score (c_v): {coherence_score:.4f}")
    return coherence_score

def save_artifacts(topic_model: BERTopic, df_with_topics: pd.DataFrame, output_dir: str):
    print(f"Menyimpan artefak ke folder '{output_dir}'...")
    os.makedirs(output_dir, exist_ok=True)
    
    # Gunakan method .save() dari BERTopic
    topic_model.save(os.path.join(output_dir, "bertopic_model"))
    
    # Simpan DataFrame dengan hasil topik
    df_with_topics.to_csv(os.path.join(output_dir, "topic_results.csv"), index=False)
    
    print("Artefak berhasil disimpan.")

def start_metrics_server(port: int = 8000):
    threading.Thread(target=lambda: start_http_server(port), daemon=True).start()
    print(f"Prometheus metrics server berjalan di http://localhost:{port}")

if __name__ == "__main__":
    # --- Konfigurasi ---
    DATA_PATH = "data/dataset_clean.csv" # Path ke data bersih Anda
    COLUMNS_TO_PROCESS = ['Title', 'Abstrak'] # Kolom yang akan digabung
    EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
    MIN_TOPIC_SIZE = 5
    MODEL_OUTPUT_DIR = "models"
    
    # --- 1. Memulai Server Monitoring ---
    start_metrics_server()
    coherence_gauge = Gauge('topic_model_coherence_score_cv', 'C_V Coherence Score dari BERTopic Model')

    # --- 2. Memuat dan Mempersiapkan Data ---
    df = load_and_prepare_data(DATA_PATH, COLUMNS_TO_PROCESS)
    
    if df is not None:
        # --- 3. Melatih Model ---
        docs = df['text_gabungan'].tolist()
        model, topics = train_bertopic_model(docs, EMBEDDING_MODEL, MIN_TOPIC_SIZE)
        
        # --- 4. Mengevaluasi Model ---
        coherence = calculate_coherence_score(model, docs)
        coherence_gauge.set(coherence) # Update metrik Prometheus
        
        # --- 5. Menyimpan Hasil ---
        df['Topic'] = topics
        save_artifacts(model, df, MODEL_OUTPUT_DIR)
        
        # --- 6. Menampilkan Hasil ---
        print("\n--- Ringkasan Topik yang Ditemukan ---")
        print(model.get_topic_info())
        print("\nSelesai.")