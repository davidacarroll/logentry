import json
import boto3
import requests
import datetime
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import urllib3
from urllib.parse import urlencode
import email
import mimetypes
from email.policy import default
from argparse import ArgumentParser
import re

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
    debug_on = False

    # Grab the timestamp for writing to DDB
    timestamp = get_timestamp()

    # From the handler event which contains a pointer to the s3 bucket, get the contents
    #  of the message and perpare it to be stored in DDB
    message = json.loads(event['Records'][0]['Sns']['Message'])
    if(debug_on):
        print("MESSAGE:", message)
    base_url = "https://xysjr7sxo1.execute-api.us-east-1.amazonaws.com/Prod"
    s3 = boto3.client('s3')

    # Store the contens of the email in a temporary file
    with open("/tmp/temp_s3_data.txt", 'wb') as data:
        try:
            s3.download_file('logbook-bucket-dac1', message['receipt']['action']['objectKey'], "/tmp/temp_s3_data.txt")
        except Exception as e:
            print("EXCEPTION IS", e)

    # Read the email contents into a parser object
    myparser = email.parser.Parser(policy=email.policy.default)
    fp = open("/tmp/temp_s3_data.txt", "r")
    msg = myparser.parse(fp)

    if (debug_on):
        for part in msg.walk():
            print("PART GET CONTENT TYPE", part.get_content_type())

    # Get the Subject line and store it for later storage into DDB
    if 'Subject' in msg:
        if (debug_on):
            print("SUBJECT IS:", msg['Subject'])
        subject_line_data = msg['Subject']

    if 'Content-Transfer-Encoding' in msg:
        if (debug_on):
            print("CONTENT-TRANSFER-ENCODING IS:", msg['Content-Transfer-Encoding'])

    # Find the body of the message (if this is an email, not for a text) and prep
    #  it for the DDB
    message_line_data = msg.get_payload()
    incr = 0
    for item in message_line_data:
        incr += 1

        test_string = item.get_content()
        if (debug_on):
            print("MESSAGE LINE", incr, "TEXT:", message_line_data)
            print("TEST STRING", incr, "TEXT:", test_string)
        if (incr == 1):
            output_string = test_string

    # Now that you have all the fields needed, write it to DDB
    r = requests.post(f"{base_url}/log-entries",
                      data={'logbookTimestamp': timestamp,
                            'From': message['mail']['source'],
                            'Subject': subject_line_data,
                            'Message': output_string
                            })
    return{
        'statusCode': 200,
        'body': json.dumps("EmailToLogbook Posted to DDB logbook table")
    }