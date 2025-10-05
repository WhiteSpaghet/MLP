# utils/export_utils.py
import csv
import io

def export_predictions_to_csv(predictions: list) -> bytes:
    """
    Recibe una lista de diccionarios con predicciones y devuelve los bytes de un CSV.
    """
    if not predictions:
        return b''

    # Crear buffer en memoria
    output = io.StringIO()
    
    # Obtener cabeceras del primer diccionario
    fieldnames = list(predictions[0].keys())
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    
    writer.writeheader()
    for pred in predictions:
        writer.writerow(pred)

    return output.getvalue().encode('utf-8')
