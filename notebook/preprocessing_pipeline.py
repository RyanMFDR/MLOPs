
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import BertTokenizer, BertModel
import torch

def load_data(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip().str.lower()
    return df

def preprocess_text(df):
    df["panjang_judul"] = df["cleaned_title"].apply(lambda x: len(str(x).split()))
    return df

def get_tfidf_features(df):
    tfidf_vectorizer = TfidfVectorizer(max_features=100)
    return tfidf_vectorizer.fit_transform(df["cleaned_title"])

def get_bert_embedding(text):
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=50)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)

if __name__ == "__main__":
    df = load_data("D:/MLOPs/data/JPTIIK_cleaned.csv")
    df = preprocess_text(df)
    print(df.head())
