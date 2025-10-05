import qrcode
import io

def generate_qr_from_data(data: list, max_rows: int = 20) -> bytes:
    """
    Genera un QR que contiene un HTML con las últimas predicciones.
    Devuelve los bytes de la imagen PNG.
    
    Parámetros:
        data (list): Lista de diccionarios con las predicciones.
        max_rows (int): Número máximo de filas a incluir en el HTML.
    """
    # Limitar filas para que el QR no sea demasiado grande
    data = data[:max_rows]

    # Crear filas HTML
    rows_html = ""
    for rec in data:
        time = rec.get('time', '-')
        filename = rec.get('filename') or "Canvas"
        pred = rec.get('pred', '-')
        conf = f"{(rec.get('confidence', 0)*100):.2f}%"
        rows_html += f"<tr><td>{time}</td><td>{filename}</td><td>{pred}</td><td>{conf}</td></tr>"

    html_content = f"""
    <html>
    <head><meta charset="UTF-8"><title>Mis Predicciones</title></head>
    <body>
    <h3>Últimas Predicciones</h3>
    <table border="1" cellpadding="3" cellspacing="0">
    <tr><th>Hora</th><th>Archivo/Canvas</th><th>Predicción</th><th>Confianza</th></tr>
    {rows_html}
    </table>
    </body>
    </html>
    """

    # Generar QR
    qr = qrcode.QRCode(
        version=None,  # autoajustable según la cantidad de datos
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=8,
        border=2,
    )
    qr.add_data(html_content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Convertir a bytes PNG
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf.getvalue()


def generate_qr_from_url(url: str) -> bytes:
    """
    Genera un QR a partir de una URL y devuelve los bytes PNG.

    Parámetros:
        url (str): URL que se codificará en el QR.
    """
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=8,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf.getvalue()
