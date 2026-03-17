import json
import boto3
import datetime
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText


# ===== VARIABLES DE ENTORNO =====

BUCKET_NAME = os.getenv("BUCKET_NAME")
if not BUCKET_NAME:
    raise ValueError("La variable de entorno BUCKET_NAME no está definida")

SES_REGION = os.getenv("SES_REGION", "us-east-1")


# ===== CLIENTES AWS =====

s3 = boto3.client("s3")
ses = boto3.client("ses", region_name=SES_REGION)


def generar_pdf(resultado):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()

    # Página 1
    elements.append(Paragraph("Evaluación de Competencias", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Nombre: {resultado['nombre']}", styles["Normal"]))
    elements.append(Paragraph(f"Email: {resultado['email']}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    data = [["Competencia", "Puntaje"]]

    for comp, val in resultado["competencias"].items():
        data.append([comp.replace("_", " ").title(), str(val)])

    data.append(["Promedio", f"{resultado['promedio']:.2f}"])

    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
    ]))

    elements.append(table)
    elements.append(PageBreak())

    # Página 2
    elements.append(Paragraph("Resultado Final", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Clasificación: {resultado['clasificacion']}", styles["Heading2"]))
    elements.append(Spacer(1, 12))

    if resultado["clasificacion"] == "ALTO":
        interpretacion = "El postulante demuestra competencias sólidas y consistentes."
    elif resultado["clasificacion"] == "MEDIO":
        interpretacion = "El postulante muestra competencias aceptables con margen de mejora."
    else:
        interpretacion = "Se recomienda reforzar competencias clave."

    elements.append(Paragraph(interpretacion, styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)

    return buffer


def enviar_resultado_empresa(resultado, pdf_buffer):
    destinatario = os.environ["CLIENTE_EMAIL"]
    remitente = os.environ["FROM_EMAIL"]

    subject = f"Nuevo resultado de evaluación – {resultado['nombre']}"

    cuerpo = f"""
Estimados,

Se ha completado una nueva evaluación de competencias.

Candidato: {resultado['nombre']}
Promedio: {resultado['promedio']:.2f}
Clasificación: {resultado['clasificacion']}

Se adjunta el reporte detallado en PDF.

Sistema de Evaluación Automatizado
"""

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = remitente
    msg["To"] = destinatario

    msg.attach(MIMEText(cuerpo, "plain"))

    adjunto = MIMEApplication(pdf_buffer.getvalue())
    adjunto.add_header(
        "Content-Disposition",
        "attachment",
        filename=f"Evaluacion_{resultado['nombre'].replace(' ', '_')}.pdf",
    )

    msg.attach(adjunto)

    params = {
        "Source": remitente,
        "Destinations": [destinatario],
        "RawMessage": {"Data": msg.as_string()},
    }

    config_set = os.getenv("SES_CONFIG_SET")
    if config_set:
        params["ConfigurationSetName"] = config_set

    ses.send_raw_email(**params)


def lambda_handler(event, context):
    try:
        if "body" in event and event["body"]:
            body = json.loads(event["body"])
        else:
            body = event

        form_response = body.get("form_response", {})
        answers = form_response.get("answers", [])

    except Exception as e:
        print("ERROR parsing event:", str(e))
        raise
    nombre = None
    email = None
    competencias = {}

    for answer in answers:
        ref = answer["field"]["ref"]

        if ref == "nombre":
            nombre = answer.get("text")
        elif ref == "email":
            email = answer.get("email")
        else:
            competencias[ref] = answer.get("number")

    valores = list(competencias.values())
    promedio = sum(valores) / len(valores) if valores else 0

    if promedio >= 4:
        clasificacion = "ALTO"
    elif promedio >= 3:
        clasificacion = "MEDIO"
    else:
        clasificacion = "BAJO"

    timestamp = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')

    resultado = {
        "nombre": nombre,
        "email": email,
        "competencias": competencias,
        "promedio": promedio,
        "clasificacion": clasificacion,
        "timestamp": timestamp
    }

    json_key = f"respuestas/procesado-{timestamp}.json"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=json_key,
        Body=json.dumps(resultado),
        ContentType="application/json"
    )

    pdf_buffer = generar_pdf(resultado)

    pdf_key = f"pdfs/evaluacion-{timestamp}.pdf"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=pdf_key,
        Body=pdf_buffer.getvalue(),
        ContentType="application/pdf"
    )

    enviar_resultado_empresa(resultado, pdf_buffer)

    print(f"Evaluación procesada y enviada para candidato: {nombre}")

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Evaluación procesada y enviada correctamente"})
    }
