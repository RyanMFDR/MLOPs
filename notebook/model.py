from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
from gensim.models.coherencemodel import CoherenceModel
import pandas as pd
import joblib
import os

class TopicModelingService:
    def __init__(self, model_name="bertopic_model"):
        self.model_name = model_name
        self.model = None
    
    def load_data(self, csv_path="E:/College/MLOPs/data/dataset_clean.csv"):
        """Load dataset yang sudah dibersihkan."""
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Dataset not found at {csv_path}")
        self.df = pd.read_csv(csv_path)
        self.documents = self.df['Abstrak_clean'].dropna().tolist()
        print(f"Loaded {len(self.documents)} documents for training.")

    def train(self):
        """Train BERTopic model dengan dataset."""
        vectorizer_model = CountVectorizer(ngram_range=(1, 2))
        self.model = BERTopic(vectorizer_model=vectorizer_model, language="indonesian")
        self.topics, _ = self.model.fit_transform(self.documents)
        print(f"Model trained with {len(set(self.topics))} topics.")

    def evaluate_coherence(self):
        """Hitung coherence score dari model yang sudah dilatih."""
        from gensim.corpora import Dictionary
        tokenized_docs = [doc.split() for doc in self.documents]
        topics_words = [self.model.get_topic(topic) for topic in set(self.topics)]
        topics_list = [[word for word, _ in topic] for topic in topics_words if topic]

        dictionary = Dictionary(tokenized_docs)
        corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]

        coherence_model = CoherenceModel(
            topics=topics_list,
            texts=tokenized_docs,
            dictionary=dictionary,
            coherence='c_v'
        )
        coherence_score = coherence_model.get_coherence()
        print(f"Coherence Score: {coherence_score:.4f}")
        return coherence_score

    def save_model(self, path="E:/College/MLOPs/models/bertopic_model.bin"):
        """Simpan model yang telah dilatih."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.model.save(path)
        print(f"Model saved to {path}")

# Example usage
if __name__ == "__main__":
    service = TopicModelingService()
    service.load_data()
    service.train()
    service.evaluate_coherence()
    service.save_model()
