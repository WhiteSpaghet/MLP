# Proyecto Deep-Learning
import sys
import os
import uuid
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify, render_template, send_file, session, redirect, url_for
import io
import json
from datetime import datetime
import numpy as np
from tensorflow import keras
from utils.preprocessing import preprocess_image
from utils.qr_utils import generate_qr_from_data, generate_qr_from_url
from utils.export_utils import export_predictions_to_csv

app = Flask(__name__)
app.secret_key = "super_secret_key"
app.config['UPLOAD_FOLDER'] = os.path.join('app', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- Cargar modelo si existe ---
MODEL_PATH = os.path.join('models', 'mnist_compiled_model.keras')
model = None
if os.path.exists(MODEL_PATH):
    model = keras.models.load_model(MODEL_PATH, compile=False, safe_mode=False)
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
else:
    print(f"⚠️ Warning: modelo no encontrado en {MODEL_PATH}. Rutas de predicción inactivas.")

# --- Log de predicciones ---
PRED_LOG = os.path.join('app', 'predictions.json')
if not os.path.exists(PRED_LOG):
    with open(PRED_LOG, 'w', encoding='utf-8') as f:
        json.dump([], f)

# --- Usuarios ficticios para demo ---
USERS = {}  # {'username': 'password'}

def save_prediction_local(record: dict):
    """Guarda la predicción localmente en predictions.json"""
    with open(PRED_LOG, 'r+', encoding='utf-8') as fh:
        try:
            data = json.load(fh)
        except json.JSONDecodeError:
            data = []
        data.insert(0, record)  # newest first
        fh.seek(0)
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.truncate()

def get_current_user():
    """Devuelve el nombre de usuario si está logueado, si no un ID anónimo"""
    if session.get('user'):
        return session['user']
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())
    return session["user_id"]

# ---------------- Rutas principales ----------------
@app.route('/')
def index():
    return render_template('index.html')

# ---------------- Login / Register / Logout ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if USERS.get(username) == password:
            session['user'] = username
            return redirect(url_for('index'))
        return render_template('login.html', error="Usuario o contraseña incorrectos")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS:
            return render_template('register.html', error="Usuario ya existe")
        USERS[username] = password
        session['user'] = username
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    if not session.get('user'):
        return redirect(url_for('login'))
    return render_template('profile.html', user=session['user'])

@app.route('/my_predictions')
def my_predictions():
    user_id = get_current_user()
    with open(PRED_LOG, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    user_data = [d for d in data if d.get('user') == user_id]
    return render_template('my_predictions.html', history=user_data)

# ---------------- Rutas de predicción ----------------
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Modelo no cargado'}), 500

    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({'error': 'No image provided'}), 400

    user_id = get_current_user()
    try:
        arr = preprocess_image(data['image'], target_size=(28,28), flatten=True)
        pred = model.predict(arr.reshape(1, -1))
        label = int(np.argmax(pred))
        confidence = float(np.max(pred))

        record = {
            'time': datetime.utcnow().isoformat(),
            'user': user_id,
            'filename': None,
            'pred': label,
            'confidence': confidence,
        }
        save_prediction_local(record)
        return jsonify({'pred': label, 'confidence': confidence})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict_batch', methods=['POST'])
def predict_batch():
    if model is None:
        return jsonify({'error': 'Modelo no cargado'}), 500

    results = []
    files = request.files.getlist('files')
    if not files:
        return jsonify({'error': 'No files provided'}), 400

    user_id = get_current_user()

    for f in files:
        try:
            arr = preprocess_image(f.read(), target_size=(28,28), flatten=True)
            pred = model.predict(arr.reshape(1, -1))
            label = int(np.argmax(pred))
            confidence = float(np.max(pred))
            record = {
                'time': datetime.utcnow().isoformat(),
                'user': user_id,
                'filename': f.filename or None,
                'pred': label,
                'confidence': confidence,
            }
            save_prediction_local(record)
            results.append(record)
        except Exception as e:
            results.append({'filename': getattr(f, 'filename', None), 'error': str(e)})

    return jsonify(results)

# ---------------- Historial de predicciones ----------------
@app.route('/history', methods=['GET'])
def history():
    user_id = get_current_user()
    limit = int(request.args.get('limit', 50))
    with open(PRED_LOG, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    data = [d for d in data if d.get('user') == user_id]
    return jsonify(data[:limit])

# ---------------- Exportación CSV ----------------
@app.route('/export', methods=['GET'])
def export():
    user_id = get_current_user()
    with open(PRED_LOG, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    data = [d for d in data if d.get('user') == user_id]
    csv_bytes = export_predictions_to_csv(data)
    return send_file(
        io.BytesIO(csv_bytes),
        mimetype='text/csv',
        as_attachment=True,
        download_name='predictions_export.csv'
    )

# ---------------- Página de estadísticas ----------------
@app.route('/stats')
def stats():
    user_id = get_current_user()
    with open(PRED_LOG, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    data = [d for d in data if d.get('user') == user_id]
    return render_template("stats.html", history=data)

# ---------------- QR de estadísticas actualizado ----------------
@app.route('/generate_qr', methods=['GET'])
def generate_qr_route():
    """Genera un QR apuntando a la página QR-view del usuario"""
    user_id = get_current_user()
    url = url_for('qr_view', user_id=user_id, _external=True)
    img_bytes = generate_qr_from_url(url)  # generamos QR solo con URL
    return send_file(io.BytesIO(img_bytes), mimetype='image/png')

# ---------------- Página QR View ----------------
@app.route('/qr_view/<user_id>')
def qr_view(user_id):
    """Muestra la página HTML bonita de predicciones para un usuario"""
    with open(PRED_LOG, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    user_history = [d for d in data if d.get('user') == user_id]
    return render_template('qr_view.html', history=user_history)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
