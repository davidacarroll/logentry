import json
import boto3
import requests
import datetime
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import urllib3
from urllib.parse import urlencode

def get_timestamp():
    utc_now = datetime.now()

    # Put time into Eastern Time Zone
    est_tz = pytz.timezone('US/Eastern')
    now = utc_now.astimezone(est_tz)

    # Format timestamp to the way you like it YYYY:MM:DD:HH:MM
    timestamp = str(now.year) + ":"
    if(now.month < 10):
        timestamp += "0"
    timestamp += str(now.month) + ":"
    if (now.day < 10):
        timestamp += "0"
    timestamp += str(now.day) + ":"
    if (now.hour < 10):
        timestamp += "0"
    timestamp += str(now.hour) + ":"
    if (now.minute < 10):
        timestamp += "0"
    timestamp += str(now.minute) + ":"
    if (now.second < 10):
        timestamp += "0"
    timestamp += str(now.second)
    return(timestamp)

def lambda_handler(event, context):
    timestamp = get_timestamp()
    #ddb = boto3.resource('dynamodb')
    #table = ddb.Table('logbook')
    #print(table.scan())

    message = json.loads(event['Records'][0]['Sns']['Message'])
    timestampMessage = event['Records'][0]['Sns']['Timestamp']
    base_url = "https://xysjr7sxo1.execute-api.us-east-1.amazonaws.com/Prod"
    r = requests.post(f"{base_url}/log-entries",
                      data={'logbookTimestamp': timestamp,
                            'From': message['originationNumber'],
                            'Subject': "Text Message from" + message['originationNumber'],
                            'Message': message['messageBody']})
    print("Made it to SMSTextToLogbook Lambda Handler!")
    print("event['Records'][0]['Sns']['Message']['messageBody']",
          event['Records'][0]['Sns']['Message'])
    print("Message", message)
    print("Message Body", message['messageBody'])
#    print("Timestamp", event['logbookTimestamp'])
    return{
        'statusCode': 200,
        'body': json.dumps("SMSTextToLogbook Posted to DDB logbook table")
    }