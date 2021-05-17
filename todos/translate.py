import os
import json

from todos import decimalencoder
import boto3

dynamodb = boto3.client('dynamodb')
client_translate = boto3.client('translate')

def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    #invoke translate function 
    translated_result = client_translate.translate_text(Text=result['Item']['text'],
        SourceLanguageCode="auto", TargetLanguageCode=event['pathParameters']['language'])


    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(translated_result['TranslatedText'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
    