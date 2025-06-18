import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.base import BaseEstimator, TransformerMixin

# Inisialisasi komponen Sastrawi (bisa diletakkan di luar agar tidak diinisialisasi ulang terus-menerus)
nltk.download('punkt', quiet=True)
stopword_factory = StopWordRemoverFactory()
stopwords_sastrawi = set(stopword_factory.get_stop_words())
stemmer = StemmerFactory().create_stemmer()

class TextPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self, text_columns):
        if not isinstance(text_columns, list):
            raise ValueError("'text_columns' harus dalam bentuk list, contoh: ['Title', 'Abstrak']")
        self.text_columns = text_columns

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        # Pastikan X adalah DataFrame
        if not isinstance(X, pd.DataFrame):
            raise TypeError("Input untuk transformer ini harus berupa pandas DataFrame.")

        # Salin untuk menghindari mengubah DataFrame asli
        X_copy = X.copy()
        
        # Gabungkan kolom teks yang ditentukan menjadi satu kolom
        combined_text = X_copy[self.text_columns].fillna('').agg(' '.join, axis=1)
        
        # Terapkan fungsi _preprocess ke kolom gabungan tersebut
        return combined_text.apply(self._preprocess)

    def _preprocess(self, text):
        text = text.lower()
        tokens = word_tokenize(text)
        # Filter token: harus alphabet dan bukan stopword
        tokens = [t for t in tokens if t.isalpha() and t not in stopwords_sastrawi]
        # Lakukan stemming
        tokens = [stemmer.stem(t) for t in tokens]
        return ' '.join(tokens)