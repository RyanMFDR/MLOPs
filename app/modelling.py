import os
import pandas as pd
import mlflow
import wandb
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
    tokenized_docs = [doc.split() for doc in docs]
    topics = topic_model.get_topics()
    topic_words = []

    for topic_id in topics:
        if topic_id == -1:
            continue
        words_in_topic = [word for word, score in topics[topic_id]]
        topic_words.append(words_in_topic)
    
    dictionary = Dictionary(tokenized_docs)
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
    model_path = os.path.join(output_dir, "bertopic_model")
    topic_model.save(model_path)
    df_with_topics.to_csv(os.path.join(output_dir, "topic_results.csv"), index=False)
    print("Artefak berhasil disimpan.")
    return model_path  # Untuk digunakan di wandb

def start_metrics_server(port: int = 8000):
    threading.Thread(target=lambda: start_http_server(port), daemon=True).start()
    print(f"Prometheus metrics server berjalan di http://localhost:{port}")

if __name__ == "__main__":
    # MLflow setup
    mlflow.set_experiment("BERTopic Experiment")
    with mlflow.start_run():
        # wandb setup
        wandb.init(
            project="bertopic-experiment",
            config={
                "embedding_model": "paraphrase-multilingual-MiniLM-L12-v2",
                "min_topic_size": 5
            }
        )
        config = wandb.config

        # Konfigurasi
        DATA_PATH = "./data/dataset_clean.csv"
        COLUMNS_TO_PROCESS = ['Title', 'Abstrak']
        EMBEDDING_MODEL = config.embedding_model
        MIN_TOPIC_SIZE = config.min_topic_size
        MODEL_OUTPUT_DIR = "models"

        # Logging parameter
        mlflow.log_param("embedding_model", EMBEDDING_MODEL)
        mlflow.log_param("min_topic_size", MIN_TOPIC_SIZE)

        wandb.config.update({
            "dataset_path": DATA_PATH,
            "output_dir": MODEL_OUTPUT_DIR
        })

        start_metrics_server()
        coherence_gauge = Gauge('topic_model_coherence_score_cv', 'C_V Coherence Score dari BERTopic Model')

        df = load_and_prepare_data(DATA_PATH, COLUMNS_TO_PROCESS)

        if df is not None:
            docs = df['text_gabungan'].tolist()
            model, topics = train_bertopic_model(docs, EMBEDDING_MODEL, MIN_TOPIC_SIZE)

            coherence = calculate_coherence_score(model, docs)
            mlflow.log_metric("coherence_score", coherence)
            wandb.log({"coherence_score": coherence})
            coherence_gauge.set(coherence)

            df['Topic'] = topics
            model_path = save_artifacts(model, df, MODEL_OUTPUT_DIR)

            # Log model ke wandb
            artifact = wandb.Artifact("bertopic_model", type="model")
            artifact.add_filed(model_path)
            wandb.log_artifact(artifact)

            print("\n--- Ringkasan Topik yang Ditemukan ---")
            print(model.get_topic_info())
            print("\nSelesai.")

        wandb.finish()
