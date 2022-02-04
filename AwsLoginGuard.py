import boto3
from botocore.exceptions import ClientError

USER_WHITELIST = ["aws-ome-user1"]
PENTESTING_OS_USER_AGENTS = ["kali", "parrot", "pentoo", "botocore"]


def lambda_handler(event, context):
    identity = event['userIdentity']
    user_agent = event['userAgent']
    arn = identity['arn']

    if not user_in_whitelist(principal_id=identity['principalId']):
        send_mail(event=create_body_payload(arn, user_agent))

    return {'statusCode': 200}


def check_user_agent(user_agent):
    return any(agent in user_agent.lower() for agent in PENTESTING_OS_USER_AGENTS)


def user_in_whitelist(principal_id):
    return any(id in principal_id for id in USER_WHITELIST)


def create_body_payload(arn, user_agent):
    return {'Username': str(arn),
            'UserAgent': str(user_agent),
            'Pentester': check_user_agent(user_agent)
            }


def send_mail(event):
    print(event)
    SENDER = "sender@mail.com"
    RECIPIENT = "recipient@mail.com"
    AWS_REGION = "eu-central-1"
    CHARSET = "UTF-8"
    SUBJECT = "ATTENTION: Some unplanned access was recognized"

    BODY_TEXT = (
        "This email was sent with Amazon SES using the AWS SDK for Python (Boto)")

    BODY_HTML = """<html>
    <head></head>
    <body>
        <p> Details about the (possible) intruder</p>
        <p>Username: {0} </p>
        <p>UserAgent: {1} </p>
        <p>Pentester: {2} </p>
    </body>
    </html>
    """.format(event['Username'], event['UserAgent'], event['Pentester'])

    client = boto3.client('ses', region_name=AWS_REGION)

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
