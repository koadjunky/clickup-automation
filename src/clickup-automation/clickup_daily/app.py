import os
import json
from main import main
from dotenv import load_dotenv
from discord_interactions import verify_key

# import requests


load_dotenv()
DISCORD_PUBLIC_KEY = os.environ.get('DISCORD_PUBLIC_KEY')


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    main()

    return {
        "statusCode": 200,
        "body": "Completed"
    }



def integrations(event, context):
    signature = event["headers"]["X-Signature-Ed25519"]
    timestamp = event["headers"]["X-Signature-Timestamp"]
    if verify_key(event.body, signature, timestamp, DISCORD_PUBLIC_KEY):
        return {
            "statusCode": 200,
            "body": "Success"
        }
    else:
        return {
            "statusCode": 401,
            "body": "Auth error"
        }
