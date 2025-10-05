# utils/firebase_utils.py
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Inicializar Firebase si no está ya inicializado
if not firebase_admin._apps:
    cred_path = os.path.join('firebase', 'serviceAccountKey.json')
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def save_prediction_to_firebase(user_id: str, record: dict):
    """
    Guarda una predicción en Firestore bajo el usuario especificado.
    """
    user_ref = db.collection('users').document(user_id)
    predictions_ref = user_ref.collection('predictions')
    predictions_ref.add(record)

def get_user_predictions(user_id: str, limit: int = 50):
    """
    Obtiene las últimas `limit` predicciones de un usuario.
    """
    user_ref = db.collection('users').document(user_id)
    predictions_ref = (
        user_ref.collection('predictions')
        .order_by('time', direction=firestore.Query.DESCENDING)
        .limit(limit)
    )
    results = [doc.to_dict() for doc in predictions_ref.stream()]
    return results
