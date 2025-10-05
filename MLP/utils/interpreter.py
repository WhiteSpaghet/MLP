# app/app.py
from flask import Flask, render_template, request, jsonify
import numpy as np
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from utils.interpreter import compile_model

app = Flask(__name__)

# ------------------------------
# 1️⃣ Crear y compilar modelo Keras
# ------------------------------
architecture = "Dense(128, relu) -> Dense(64, relu) -> Dense(10, softmax)"
input_dim = 28*28
model = compile_model(architecture, input_dim)

# Cargar MNIST y entrenar rápido para demo
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape(-1, 28*28) / 255.0
y_train = to_categorical(y_train, 10)
x_test = x_test.reshape(-1, 28*28) / 255.0
y_test = to_categorical(y_test, 10)

model.fit(x_train, y_train, epochs=3, batch_size=32, validation_data=(x_test, y_test))

# ------------------------------
# 2️⃣ Rutas HTML
# ------------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

# ------------------------------
# 3️⃣ Endpoint predicción canvas/subida
# ------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    """
    Recibe JSON con un array de 784 píxeles (0-255)
    """
    data = request.json
    pixels = np.array(data["pixels"]).reshape(1, 784) / 255.0
    pred = model.predict(pixels)
    predicted_class = int(np.argmax(pred, axis=1)[0])
    return jsonify({"prediction": predicted_class})

# ------------------------------
# 4️⃣ Endpoint para batch (subida de imágenes)
# ------------------------------
@app.route("/predict_batch", methods=["POST"])
def predict_batch():
    """
    Recibe JSON con varias imágenes
    """
    data = request.json
    results = []
    for img in data["images"]:
        pixels = np.array(img).reshape(1, 784) / 255.0
        pred = model.predict(pixels)
        results.append(int(np.argmax(pred, axis=1)[0]))
    return jsonify({"predictions": results})

# ------------------------------
# 5️⃣ Ejecutar Flask
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
