import json
import boto3
from botocore.exceptions import ClientError

USER_WHITELIST = ["AIDACKCEVSQ6C2EXAMPLE"]
PENTESTING_OS_USER_AGENTS = ["kali", "parrot", "pentoo", "botocore"]


def lambda_handler(event, context):
    # pylint: disable=unused-argument
    user_identity = event['userIdentity']
    user_agent = event['userAgent']
    arn = user_identity['arn']

    if not is_user_in_whitelist(principal_id=user_identity['principalId']):
        send_mail(payload=create_body_payload(arn, user_agent))

    return {'statusCode': 200}


def check_user_agent(user_agent):
    return any(agent in user_agent.lower() for agent in PENTESTING_OS_USER_AGENTS)


def is_user_in_whitelist(principal_id):
    return any(id in principal_id for id in USER_WHITELIST)


def create_body_payload(arn, user_agent):
    return {'Username': str(arn),
            'UserAgent': str(user_agent),
            'Pentester': check_user_agent(user_agent)
            }


def send_mail(payload, client=None):
    sender = "sender@mail.com"
    recipient = "recipient@mail.com"
    aws_region = "eu-central-1"
    charset = "UTF-8"
    suject = "ATTENTION: Some unplanned access was recognized"

    body_text = (
        "This email was sent with Amazon SES using the AWS SDK for Python (Boto)")

    body_html = f'''<html>
    <head></head>
    <body>
        <p>Details about the (possible) intruder</p>
        <p>Username: {0} </p>
        <p>UserAgent: {1} </p>
        <p>Pentester: {2} </p>
    </body>
    </html>
    '''.format(payload['Username'], payload['UserAgent'], payload['Pentester'])

    if not client:
        client = boto3.client('ses', region_name=aws_region)

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': charset,
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': charset,
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': charset,
                    'Data': suject,
                },
            },
            Source=sender,
        )
    except ClientError as err:
        print(err.response['Error']['Message'])
        return {'statusCode': 500}
    else:
        return {'statusCode': 200,
                'body': json.dumps(f"Email sent! Response: {0}".format(response))
                }
