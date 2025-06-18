from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

preprocess_transformer = TextPreprocessor(text_columns=['Title', 'Abstrak'])

full_pipeline = Pipeline([
    ('custom_preprocessing', preprocess_transformer),
    ('vectorization', TfidfVectorizer(max_features=1000))
])

tfidf_matrix = full_pipeline.fit_transform(df)

print("Proses berhasil. Bentuk matriks TF-IDF:", tfidf_matrix.shape)