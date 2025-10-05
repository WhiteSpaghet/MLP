# utils/analysis.py
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np
import io

def compute_confusion(y_true, y_pred, labels=None):
    """
    Calcula la matriz de confusión.
    """
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    return cm

def plot_confusion_matrix(cm, labels=None):
    """
    Genera un heatmap de la matriz de confusión.
    """
    plt.figure(figsize=(8,6))
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=labels, yticklabels=labels, cmap='Blues')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

def print_classification_report(y_true, y_pred, labels=None):
    """
    Retorna el reporte de clasificación tipo precision, recall y f1-score.
    """
    report = classification_report(y_true, y_pred, labels=labels, output_dict=True)
    return report

def plot_training_history(history):
    """
    history: objeto retornado por model.fit()
    Retorna figura matplotlib de accuracy y loss
    """
    plt.figure(figsize=(10,4))

    # Accuracy
    plt.subplot(1,2,1)
    plt.plot(history.history['accuracy'], label='train_acc')
    plt.plot(history.history.get('val_accuracy', []), label='val_acc')
    plt.title('Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()

    # Loss
    plt.subplot(1,2,2)
    plt.plot(history.history['loss'], label='train_loss')
    plt.plot(history.history.get('val_loss', []), label='val_loss')
    plt.title('Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf
