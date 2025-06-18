import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Download resource yang diperlukan
nltk.download('punkt')

# Load dataset
df = pd.read_csv("../data/dataset.csv")

# Hapus kolom 'Link' jika ada
if 'Link' in df.columns:
    df.drop(columns=['Link'], inplace=True)

# Isi NaN dengan string kosong
df.fillna('', inplace=True)

# Inisialisasi stopword dan stemmer dari Sastrawi
factory_stopwords = StopWordRemoverFactory()
stopwords_sastrawi = set(factory_stopwords.get_stop_words())

stemmer = StemmerFactory().create_stemmer()

# Fungsi preprocessing gabungan: lower, tokenize, hapus stopword, stemming
def preprocess(text):
    text = text.lower()
    tokens = word_tokenize(text)
    filtered_tokens = [word for word in tokens if word.isalpha() and word not in stopwords_sastrawi]
    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]
    return ' '.join(stemmed_tokens)

# Terapkan ke kolom teks
df['Judul'] = df['Judul'].apply(preprocess)
df['Keyword'] = df['Keyword'].apply(preprocess)
df['Abstrak'] = df['Abstrak'].apply(preprocess)

# Simpan ke file baru
df.to_csv("../data/dataset_clean.csv", index=False)

print("Preprocessing selesai! File disimpan sebagai dataset_clean.csv")