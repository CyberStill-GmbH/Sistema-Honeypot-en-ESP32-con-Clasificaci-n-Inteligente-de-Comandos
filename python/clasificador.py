import os
from typing import Dict
import joblib

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'modelo_persona2.joblib')

_model = None
_vectorizer = None
if os.path.exists(MODEL_PATH):
    try:
        data = joblib.load(MODEL_PATH)
        # data expected: {'model': model, 'vectorizer': vectorizer}
        _model = data.get('model')
        _vectorizer = data.get('vectorizer')
    except Exception:
        _model = None
        _vectorizer = None

def clasificar(cmd: str) -> Dict:
    """Clasifica el comando recibido.
    Retorna dict: {label, score, reason}
    """
    cmd = (cmd or '').strip()
    if not cmd:
        return {'label': 'empty', 'score': 0.0, 'reason': 'comando vacío'}

    text = cmd.lower()

    # Si hay modelo cargado, usarlo
    if _model is not None and _vectorizer is not None:
        try:
            X = _vectorizer.transform([text])
            probs = _model.predict_proba(X)[0]
            idx = probs.argmax()
            label = _model.classes_[idx]
            score = float(probs[idx])
            return {'label': str(label), 'score': score, 'reason': 'modelo cargado'}
        except Exception as e:
            # fallback a reglas si el modelo falla
            pass

    # Fallback basado en reglas (keywords)
    low_risk = ['status', 'ping', 'temp', 'get', 'read', 'info']
    suspicious = ['rm -rf', 'del ', 'format', 'overwrite', 'wget ', 'curl ', 'nc ', 'netcat', 'reverse', 'meterpreter', 'exploit']
    exploit = ['payload', 'msf', 'shell', 'sudo ', 'su ', 'passwd ', 'chpasswd', 'mimikatz']

    score = 0.0
    label = 'normal'
    reason = 'reglas fallback'

    if any(k in text for k in exploit):
        label = 'exploit'
        score = 0.99
        reason = 'contiene palabras clave de exploit/privilegios'
    elif any(k in text for k in suspicious):
        label = 'sospechoso'
        score = 0.75
        reason = 'contiene palabras clave sospechosas'
    elif any(k in text for k in low_risk):
        label = 'normal'
        score = 0.6
        reason = 'palabras clave comunes'
    else:
        label = 'desconocido'
        score = 0.4
        reason = 'no clasificable por reglas'

    return {'label': label, 'score': score, 'reason': reason}
