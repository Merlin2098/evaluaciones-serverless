# Serverless Evaluation Pipeline (Typeform + AWS)

![AWS](https://img.shields.io/badge/AWS-Serverless-orange)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![SAM](https://img.shields.io/badge/AWS%20SAM-Infrastructure%20as%20Code-green)
![License](https://img.shields.io/badge/license-Educational-lightgrey)

Sistema **serverless** para procesar evaluaciones enviadas desde
**Typeform**, generar automáticamente un **reporte PDF**, almacenarlo en
**Amazon S3** y enviarlo por **correo electrónico usando Amazon SES**.

Toda la infraestructura se define como **Infrastructure as Code** usando
**AWS SAM / CloudFormation**.

------------------------------------------------------------------------

# Features

-   Arquitectura serverless
-   Procesamiento automático de evaluaciones
-   Generación automática de PDF
-   Almacenamiento en Amazon S3
-   Envío automático de correos con Amazon SES
-   Infraestructura definida como código (IaC)

------------------------------------------------------------------------

# Technologies

-   AWS Lambda
-   Amazon API Gateway
-   Amazon S3
-   Amazon SES
-   AWS SAM
-   Python 3.11
-   ReportLab

------------------------------------------------------------------------

# Why this project exists

Este proyecto demuestra cómo construir un **pipeline serverless para
procesar datos provenientes de webhooks**.

Objetivos:

-   Automatizar evaluaciones enviadas desde formularios
-   Generar reportes PDF automáticamente
-   Almacenar resultados estructurados
-   Enviar reportes automáticamente por correo

Este patrón se utiliza comúnmente en integraciones con:

-   Typeform
-   Stripe
-   Slack
-   GitHub Webhooks
-   Shopify

------------------------------------------------------------------------

# Architecture

El sistema utiliza una arquitectura serverless simple y escalable.

![Architecture Diagram](./architecture.png)

Flujo:

Typeform Webhook\
↓\
API Gateway (POST /evaluacion)\
↓\
AWS Lambda (Python)\
↓\
Generación de PDF (ReportLab)\
↓\
Amazon S3 (almacenamiento de resultados)\
↓\
Amazon SES (envío automático de correo)

Servicios AWS utilizados:

-   AWS Lambda
-   Amazon API Gateway
-   Amazon S3
-   Amazon SES
-   Amazon CloudWatch Logs
-   Lambda Layers
-   AWS SAM / CloudFormation

------------------------------------------------------------------------

# Project Structure

    evaluaciones-serverless/
    │
    ├── lambda/
    │   └── app.py
    │
    ├── layer/
    │   └── dependencies.zip
    │
    ├── template.yaml
    │
    ├── architecture.png
    │
    └── README.md

  Folder             Description
  ------------------ ----------------------------------------------------
  lambda             código de la función Lambda
  layer              dependencias Python empaquetadas como Lambda Layer
  template.yaml      definición de infraestructura serverless
  architecture.png   diagrama de arquitectura
  README.md          documentación del proyecto

------------------------------------------------------------------------

# Requirements

Antes de desplegar el sistema necesitas:

-   Cuenta AWS
-   AWS CLI configurado
-   AWS SAM CLI instalado
-   Python 3.11
-   Bucket S3 existente
-   SES configurado (email o dominio verificado)

Instalar SAM CLI:

    pip install aws-sam-cli

Verificar instalación:

    sam --version

------------------------------------------------------------------------

# Environment Variables

La función Lambda utiliza variables de entorno para evitar **hardcoding
de infraestructura**.

  Variable         Description
  ---------------- ---------------------------------------
  BUCKET_NAME      bucket S3 donde se guardan resultados
  CLIENTE_EMAIL    destinatario del reporte
  FROM_EMAIL       remitente del correo
  SES_REGION       región de SES
  SES_CONFIG_SET   configuration set de SES

Ejemplo:

    BUCKET_NAME=evaluaciones-demo-bucket
    CLIENTE_EMAIL=example@email.com
    FROM_EMAIL=example@email.com
    SES_REGION=us-east-1
    SES_CONFIG_SET=email-debug

------------------------------------------------------------------------

# Quick Start

## 1️⃣ Clonar repositorio

    git clone https://github.com/Merlin2098/evaluaciones-serverless
    cd evaluaciones-serverless

## 2️⃣ Construir el proyecto

    sam build

Esto prepara:

-   código Lambda
-   layer
-   template CloudFormation

## 3️⃣ Desplegar infraestructura

    sam deploy --guided

Durante el deploy AWS solicitará:

-   nombre del stack
-   región
-   bucket para artefactos
-   confirmación de permisos IAM

SAM creará automáticamente:

-   Lambda
-   API Gateway
-   permisos
-   integración webhook

------------------------------------------------------------------------

# Configure Typeform Webhook

Después del deploy obtendrás un endpoint similar a:

    https://xxxx.execute-api.us-east-1.amazonaws.com/Prod/evaluacion

Configura ese endpoint como **webhook en Typeform**.

Cada envío del formulario activará la Lambda.

------------------------------------------------------------------------

# Output Generated

Cada evaluación produce:

1.  JSON con respuestas procesadas\
2.  PDF con reporte de evaluación

Archivos almacenados en:

    s3://BUCKET_NAME/respuestas/
    s3://BUCKET_NAME/pdfs/

Ejemplo de estructura:

    respuestas/
       procesado-20250101T100000Z.json

    pdfs/
       evaluacion-20250101T100000Z.pdf

Además el sistema envía automáticamente un **correo con el reporte PDF
adjunto**.

------------------------------------------------------------------------

# Observability

Las ejecuciones de la Lambda generan logs automáticamente en:

    CloudWatch Logs
    /aws/lambda/<function-name>

Esto permite:

-   monitorear ejecuciones
-   detectar errores
-   analizar comportamiento del sistema

------------------------------------------------------------------------

# Security Considerations

Este proyecto sigue buenas prácticas básicas de seguridad:

-   uso de variables de entorno para evitar hardcoding
-   IAM roles para controlar acceso a servicios
-   logs centralizados en CloudWatch

En producción se recomienda:

-   restringir permisos IAM
-   habilitar autenticación en API Gateway
-   usar AWS Secrets Manager para credenciales sensibles

------------------------------------------------------------------------

# Infrastructure as Code

La infraestructura se define usando **AWS SAM**, basado en
**CloudFormation**.

Esto permite:

-   reproducibilidad del sistema
-   despliegue automatizado
-   versionado de infraestructura

Archivo principal:

    template.yaml

------------------------------------------------------------------------

# Local Testing (Optional)

Puedes probar la Lambda localmente usando Docker:

    sam local invoke -e event.json

------------------------------------------------------------------------

# Cost Considerations

Este proyecto está diseñado para funcionar dentro del **AWS Free Tier**
para entornos de prueba.

Costos principales:

-   Lambda invocations
-   almacenamiento en S3
-   envío de correos en SES

Para cargas pequeñas el costo es prácticamente cero.

------------------------------------------------------------------------

# Future Improvements

Posibles mejoras:

-   usar SQS para desacoplar procesamiento
-   agregar DynamoDB para historial de evaluaciones
-   crear dashboard analítico con Athena o QuickSight
-   usar EventBridge para orquestación
-   implementar autenticación en API Gateway

------------------------------------------------------------------------

# License

Proyecto de ejemplo con fines educativos.
