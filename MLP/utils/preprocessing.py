# utils/preprocessing.py
import numpy as np
from PIL import Image
import base64
import io

# Compatibilidad con diferentes versiones de Pillow
try:
    resample_method = Image.Resampling.LANCZOS  # Pillow 10+
except AttributeError:
    resample_method = Image.LANCZOS  # Pillow <10

def preprocess_image(image_input, target_size=(28,28), flatten=True):
    """
    Convierte una imagen (bytes o base64) a un array normalizado listo para Keras.
    """
    # Si es base64 tipo 'data:image/png;base64,...'
    if isinstance(image_input, str) and image_input.startswith('data:image'):
        header, base64_data = image_input.split(',', 1)
        image_input = base64.b64decode(base64_data)
    
    img = Image.open(io.BytesIO(image_input)).convert('L')
    img = img.resize(target_size, resample_method)
    img_array = np.array(img, dtype=np.float32) / 255.0

    if flatten:
        img_array = img_array.flatten()
    return img_array

def preprocess_canvas_data(canvas_data, target_size=(28,28), flatten=True):
    """
    Convierte datos de canvas (p. ej. array de píxeles) a formato listo para Keras.
    canvas_data: array 2D o 1D con valores 0-255
    """
    arr = np.array(canvas_data, dtype=np.float32)
    if arr.max() > 1:
        arr /= 255.0  # normalizar
    img = Image.fromarray((arr*255).astype(np.uint8)).convert('L')
    img = img.resize(target_size, resample_method)
    img_array = np.array(img, dtype=np.float32)/255.0
    if flatten:
        img_array = img_array.flatten()
    return img_array
