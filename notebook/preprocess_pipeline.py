import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.base import BaseEstimator, TransformerMixin

# Pastikan resource NLTK tersedia
nltk.download('punkt')

# Inisialisasi komponen Sastrawi
stopword_factory = StopWordRemoverFactory()
stopwords_sastrawi = set(stopword_factory.get_stop_words())
stemmer = StemmerFactory().create_stemmer()

# Custom Transformer untuk pipeline
class TextPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.apply(self._preprocess)

    def _preprocess(self, text):
        text = text.lower()
        tokens = word_tokenize(text)
        tokens = [t for t in tokens if t.isalpha() and t not in stopwords_sastrawi]
        tokens = [stemmer.stem(t) for t in tokens]
        return ' '.join(tokens)

# Fungsi untuk load & bersihkan dataset
def load_and_preprocess_dataset(path):
    df = pd.read_csv(path)

    # Hapus kolom 'Link' jika ada
    if 'Link' in df.columns:
        df.drop(columns=['Link'], inplace=True)

    # Ganti NaN jadi string kosong
    df.fillna('', inplace=True)

    # Inisialisasi pipeline
    preprocessor = TextPreprocessor()

    # Terapkan ke kolom teks
    df['Judul_clean'] = preprocessor.transform(df['Judul'])
    df['Keyword_clean'] = preprocessor.transform(df['Keyword'])
    df['Abstrak_clean'] = preprocessor.transform(df['Abstrak'])

    return df
