# AWS Infrastructure Setup & Deployment Guide

ResumeIQ supports seamless deployment to AWS serverless infrastructure using AWS SAM (Serverless Application Model).

## AWS Resources Provisioned
- **AWS Lambda**: Executes shared Python ATS core engine inside serverless functions.
- **Amazon API Gateway**: Routes HTTPS REST API requests to Lambda.
- **Amazon S3**: Private S3 bucket for storing uploaded resumes and generated PDF outputs securely.
- **Amazon DynamoDB**: Key-value table storing deterministic analysis records.

## Deployment Steps

1. Install AWS CLI & AWS SAM CLI:
   ```bash
   sam --version
   ```

2. Configure AWS Credentials:
   ```bash
   aws configure
   ```

3. Build SAM Package:
   ```bash
   cd infrastructure
   sam build
   ```

4. Deploy Serverless Stack:
   ```bash
   sam deploy --guided
   ```

5. Set Environment Variables in `.env` (for Cloud Mode):
   ```env
   STORAGE_MODE=aws
   DATABASE_MODE=dynamodb
   AWS_REGION=us-east-1
   AWS_S3_BUCKET=<your-sam-bucket-name>
   AWS_DYNAMODB_TABLE=resumeiq-analyses
   ```
