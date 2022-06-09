import json
import gzip
import localstack_client.session as boto3
import hashlib
import psycopg2
from datetime import datetime
import re

sqs = boto3.client('sqs')


def transform(ip, device_id):
    # Takes in a string ip and device_id, returns the hexdigest of ip and device_id

    print("Transforming Data..." + ip + " " + device_id)

    mask_ip = hashlib.sha256(ip.encode('UTF-8'))
    mask_device_id = hashlib.sha256(device_id.encode('UTF-8'))

    ip_dig = mask_ip.hexdigest()
    dev_dig = mask_device_id.hexdigest()

    return [ip_dig, dev_dig]


def connect_postgres():
    conn = psycopg2.connect(
        database="postgres", user='postgres', password='postgres', host='127.0.0.1', port= '5432'
    )
    conn.autocommit = True

    return conn


def insert_data(db, data):
    # Takes in a postgres object and a dictonary

    cursor = db.cursor()

    time = datetime.now()

    user_id = data.get("user_id")
    device_type = data.get("device_type")
    masked_ip = data.get("ip")
    masked_device_id = data.get("device_id")
    locale = data.get("locale")
    app_version = re.search("[0-9]*.", str(data.get("app_version")))
    float_app_version = float(app_version.group(0))
    date = time.strftime("%Y-%m-%d")

    print("Inserting data to Database...")

    cursor.execute(f"""INSERT INTO USER_LOGINS(user_id, device_type, masked_ip, masked_device_id, locale,
    	app_version, create_date) VALUES('{user_id}', '{device_type}', '{masked_ip}', '{masked_device_id}', 
    	'{locale}', '{int(float_app_version)}', '{date}')""")


def delete_message(queue_url, receipt_handle):
    # Takes in a string queue_url and receipt_handle

    print("Deleting message from queue...\n")
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )


def read_messages():
    # This function will read messages from SQS, transform that data and insert to the database.
    #	Once done will delete the message

    QUEUE_NAME = "login-queue"

    # Create SQS client
    queue_url = sqs.create_queue(QueueName=QUEUE_NAME)["QueueUrl"]

    loop = True

    while loop:

        # Receive message from SQS queue
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=[
                'SentTimestamp'
                ],
            MaxNumberOfMessages = 1,
            MessageAttributeNames = [
                'All'
                ],
            VisibilityTimeout = 0,
            WaitTimeSeconds = 0
        )

        try:
            if response['Messages'][0] == "":
                loop = False
        except:
            print("Done...no more data")
            break

        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']

        body = json.loads(message.get("Body"))

        hash_values = transform(body.get("ip"), body.get("device_id"))

        insert = {"ip": hash_values[0], "device_id": hash_values[1]}

        body.update(insert)

        insert_data(connect_postgres(), body)

        delete_message(queue_url, receipt_handle)


read_messages()
