# Serverless Evaluation Pipeline (Typeform + AWS)

![AWS](https://img.shields.io/badge/AWS-Serverless-orange)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![SAM](https://img.shields.io/badge/AWS%20SAM-Infrastructure%20as%20Code-green)
![License](https://img.shields.io/badge/license-Educational-lightgrey)

Serverless workflow for processing evaluations submitted via **Typeform webhooks**.

The system automatically generates a **PDF report**, stores the results in
**Amazon S3**, and sends the report via **Amazon SES**.

All infrastructure is defined as **Infrastructure as Code using AWS SAM
(CloudFormation)**.

---

# Features

- Serverless event-driven architecture
- Webhook-based evaluation processing
- Automatic PDF report generation
- Artifact storage in Amazon S3
- Automated email delivery using Amazon SES
- Infrastructure defined as code using AWS SAM

---

# Technologies

- Amazon API Gateway
- AWS Lambda
- Amazon S3
- Amazon SES
- Amazon CloudWatch Logs
- AWS SAM (CloudFormation)
- Python 3.11
- ReportLab

---

# Why this project exists

This project demonstrates how to build a **serverless pipeline for
processing data from webhooks**.

Goals:

- Automate evaluations submitted from forms
- Automatically generate PDF reports
- Store structured results
- Send reports automatically by email

This pattern is commonly used in integrations with:

- Typeform
- Stripe
- Slack
- GitHub Webhooks
- Shopify

---


# Example Use Case

Imagine a company collecting structured evaluations through an online form.

Each time a user submits the form:

1. The form platform sends a webhook event.
2. The system processes the responses automatically.
3. A PDF evaluation report is generated.
4. The report is stored in Amazon S3.
5. The report is emailed to the recipient.

This eliminates manual processing and allows evaluations to be generated
and delivered automatically.

The same architecture pattern can be used for other webhook-driven workflows,
such as payment notifications, order processing, or automated report generation.

---

# Architecture

The system uses a simple and scalable serverless architecture.

![Architecture Diagram](./architecture.png)

Flow:

Typeform Webhook
→ API Gateway (POST /evaluation)
→ AWS Lambda (Python)
→ PDF Generation (ReportLab)
→ Amazon S3 (result storage)
→ Amazon SES (email delivery)

AWS services used:

- AWS Lambda
- Amazon API Gateway
- Amazon S3
- Amazon SES
- Amazon CloudWatch Logs
- Lambda Layers
- AWS SAM / CloudFormation

---

# Project Structure

evaluations-serverless/
│
├── lambda/
│   └── app.py
│
├── layer/
│   └── dependencies.zip
│
├── template.yaml
├── architecture.png
└── README.md

---

# Requirements

Before deploying the system, you need:

- An AWS account
- AWS CLI configured
- AWS SAM CLI installed
- Python 3.11
- An existing S3 bucket
- SES configured (verified email or domain)

Install SAM CLI:

    pip install aws-sam-cli

Verify installation:

    sam --version

---

# Environment Variables

The Lambda function uses environment variables to avoid **hardcoding
infrastructure values**.

| Variable       | Description                        |
| -------------- | ---------------------------------- |
| BUCKET_NAME    | S3 bucket where results are stored |
| CLIENTE_EMAIL  | Report recipient                   |
| FROM_EMAIL     | Sender email                       |
| SES_REGION     | SES region                         |
| SES_CONFIG_SET | SES configuration set              |

Example:

    BUCKET_NAME=evaluaciones-demo-bucket
    CLIENTE_EMAIL=example@email.com
    FROM_EMAIL=example@email.com
    SES_REGION=us-east-1
    SES_CONFIG_SET=email-debug

---

# Quick Start

## 1. Clone the repository

    git clone https://github.com/Merlin2098/evaluaciones-serverless
    cd evaluaciones-serverless

## 2. Build the project

    sam build

This prepares:

- Lambda code
- Layer
- CloudFormation template

## 3. Deploy the infrastructure

    sam deploy --guided

During deployment AWS will ask for:

- Stack name
- Region
- Bucket for artifacts
- IAM permission confirmation

SAM will automatically create:

- Lambda
- API Gateway
- Permissions
- Webhook integration

---

# Configure the Typeform Webhook

After deployment you will get an endpoint similar to:

    https://xxxx.execute-api.us-east-1.amazonaws.com/Prod/evaluation

Configure that endpoint as a **webhook in Typeform**.

Each form submission will trigger the Lambda.

---

# Generated Output

Each evaluation produces:

1. JSON with processed responses\
2. PDF with the evaluation report

Files are stored in:

    s3://BUCKET_NAME/responses/
    s3://BUCKET_NAME/pdfs/

Example structure:

    responses/
       processed-20250101T100000Z.json

    pdfs/
       evaluation-20250101T100000Z.pdf

In addition, the system automatically sends an **email with the PDF
report attached**.

---

# Observability

Lambda executions generate logs automatically in **Amazon CloudWatch Logs**:

/aws/lambda/`<function-name>`

This makes it possible to:

- Monitor executions
- Detect errors
- Analyze system behavior

---

# Security Considerations

This project follows basic security best practices:

- Environment variables to avoid hardcoded values
- IAM roles to restrict service access
- Centralized logging in CloudWatch

In production, it is recommended to:

- Restrict IAM permissions
- Enable authentication in API Gateway
- Use AWS Secrets Manager for sensitive credentials

---

# Infrastructure as Code

The infrastructure is defined using **AWS SAM**, based on
**CloudFormation**.

This enables:

- System reproducibility
- Automated deployment
- Infrastructure versioning

Main file:

    template.yaml

---

# Local Testing (Optional)

You can test the Lambda locally using Docker:

    sam local invoke -e event.json

---

# Cost Considerations

This project is designed to run within the **AWS Free Tier** for test
environments.

Main costs:

- Lambda invocations
- S3 storage
- SES email sending

For small workloads, the cost is practically zero.

---

# What I Learned

Building this project helped me understand:

- Designing event-driven serverless workflows
- Integrating external services via webhooks
- Using AWS SAM for infrastructure as code
- Managing Lambda dependencies using layers
- Storing generated artifacts in Amazon S3
- Sending automated notifications using Amazon SES
- Observing system behavior through CloudWatch logs

---

# Future Improvements

Possible improvements:

- **Introduce Amazon SQS and split the Lambda into ingestion and processing stages**

  Currently, a single Lambda function handles the full workflow: receiving
  the webhook payload, generating the PDF report, storing results in S3,
  and sending the email via SES.

  A future improvement would introduce **Amazon SQS** to decouple ingestion
  from processing. The architecture would evolve into two Lambda functions:

  - **Ingestion Lambda**: receives the webhook via API Gateway and pushes the
    event to an SQS queue.
  - **Processing Lambda**: triggered by SQS to generate the PDF report,
    store results in S3, and send the email via SES.

  This pattern improves reliability, allows retries, and enables the system
  to better handle bursts of webhook traffic.
- Add DynamoDB for evaluation history
- Create an analytics dashboard with Athena or QuickSight
- Use EventBridge for orchestration
- Implement authentication in API Gateway

# License

Sample project for educational purposes.
