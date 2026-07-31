import json
import base64
from app import app

def handler(event, context):
    """
    AWS Lambda proxy handler for Amazon API Gateway REST events.
    Translates API Gateway v1/v2 payload into WSGI environment for Flask app.
    """
    # Using serverless-wsgi or basic event translator
    path = event.get("path", "/")
    http_method = event.get("httpMethod", "GET")
    headers = event.get("headers") or {}
    query_params = event.get("queryStringParameters") or {}
    
    # Body decoding
    body = event.get("body", "")
    if event.get("isBase64Encoded", False):
        body = base64.b64decode(body)

    # Use Flask test_client for in-process request processing
    with app.test_client() as client:
        response = client.open(
            path=path,
            method=http_method,
            headers=headers,
            query_string=query_params,
            data=body
        )

        response_headers = {k: v for k, v in response.headers.items()}

        return {
            "statusCode": response.status_code,
            "headers": response_headers,
            "body": response.get_data(as_text=True)
        }
