import json
import datetime
import dateutil
import boto3
import botocore
import base64
import gzip

cw = boto3.client('cloudwatch')


def lambda_handler(event, context):
    cw_data = event['awslogs']['data']
    compressed_payload = base64.b64decode(cw_data)
    uncompressed_payload = gzip.decompress(compressed_payload)
    payload = json.loads(uncompressed_payload)

    log_events = payload['logEvents']

    for log_event in log_events:
        log = json.loads(log_event['message'])
        payload = log['payload']
        print(payload)

        print("Processing some event: {}...".format(
            payload['name_of_something_you_set_in_your_logs']))

        # Publish DB Runtime
        cw.put_metric_data(Namespace='RAILS',
                           MetricData=[{
                               'MetricName': 'name_of_something_you_set_in_your_logs',
                               'Dimensions': [
                                   {
                                       'Name': 'Dimension 1',
                                       'Value': payload['data 1']
                                   },
                                   {
                                       'Name': 'Dimension 2',
                                       'Value': payload['data 2']
                                   }],
                               'Timestamp': datetime.datetime.now(dateutil.tz.tzlocal()),
                               'Value': payload['name_of_something_you_set_in_your_logs],
                               'Unit': 'Milliseconds'
                           }])

        print("name_of_something_you_set_in_your_logs {} sent".format(
            payload['name_of_something_you_set_in_your_logs']))
    return {}
