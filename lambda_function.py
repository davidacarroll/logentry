import json
import boto3
import requests
import datetime
import urllib3
from urllib.parse import urlencode

def get_timestamp():
    now = datetime.datetime.now()
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

    ############# THE WORKING WAY
    base_url = "https://xysjr7sxo1.execute-api.us-east-1.amazonaws.com/Prod"
    r = requests.post(f"{base_url}/log-entries", data={'logbookTimestamp': timestamp, 'Name': "Freddy"})
    print("Made it to SMSTextToLogbook Lambda Handler!")
    return{
        'statusCode': 200,
        'body': json.dumps("SMSTextToLogbook Posted to DDB logbook table")
    }
    """

    ############# THE NOT WORKING WAY
    http = urllib3.PoolManager()
    fields = {'logbookTimestamp': timestamp, 'Name': "Fred"}
    encoded_fields = json.dumps(fields)
    other_encoded_fields = urlencode(fields)
    link = "https://xysjr7sxo1.execute-api.us-east-1.amazonaws.com/Prod/log-entries"
    link2 = link + other_encoded_fields
    r = http.request('POST',
                     link,
                     body=encoded_fields,
                     headers={'Content-Type': 'application/json'}
                     )
    print("Results are:", r.data)
    """