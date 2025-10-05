# utils/training_utils.py
import os
import tensorflow as tf
import numpy as np

def load_base_model(model_path: str):
    """
    Carga el modelo base MNIST entrenado, si existe.
    
    Args:
        model_path: ruta del modelo (.h5 o SavedModel)
    
    Returns:
        modelo Keras o None si no existe
    """
    if os.path.exists(model_path):
        return tf.keras.models.load_model(model_path)
    return None

def incremental_train(model, x_new: np.ndarray, y_new: np.ndarray, epochs=1, batch_size=32):
    """
    Entrenamiento incremental: ajusta un modelo existente con nuevos datos.
    
    Args:
        model: modelo Keras existente
        x_new: datos de entrada normalizados y aplanados
        y_new: etiquetas one-hot
        epochs: número de épocas
        batch_size: tamaño de batch
    
    Returns:
        history de Keras (objeto con métricas)
    """
    history = model.fit(x_new, y_new, epochs=epochs, batch_size=batch_size, verbose=1)
    return history

def save_model(model, save_path: str):
    """
    Guarda el modelo Keras en la ruta especificada.
    
    Args:
        model: modelo Keras
        save_path: ruta para guardar el modelo
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    model.save(save_path)
