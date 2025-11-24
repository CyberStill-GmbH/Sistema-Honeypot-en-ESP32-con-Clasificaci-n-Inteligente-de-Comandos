"""Script de ejemplo para entrenar un modelo de texto y guardarlo en models/modelo_persona2.joblib
Este script crea un dataset sintético como plantilla; reemplaza con tus datos reales.
"""
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import joblib

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

# dataset sintético de ejemplo
X = [
    'get temp', 'get status', 'read sensor',
    'rm -rf /', 'wget http://malware', 'nc -e /bin/sh',
    'sudo passwd root', 'payload exec', 'meterpreter reverse',
]
y = ['normal', 'normal', 'normal', 'sospechoso', 'sospechoso', 'sospechoso', 'exploit', 'exploit', 'exploit']

vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=2000)
model = LogisticRegression(max_iter=1000)
X_vec = vectorizer.fit_transform(X)
model.fit(X_vec, y)

joblib.dump({'model': model, 'vectorizer': vectorizer}, os.path.join(MODEL_DIR, 'modelo_persona2.joblib'))
print('Modelo guardado en models/modelo_persona2.joblib')
