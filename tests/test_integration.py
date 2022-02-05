import json
import os
import unittest
from unittest.mock import patch
import AwsLoginGuard as guard
import boto3
from moto import mock_lambda, mock_ses


class TestMitMiMiMiIntegrationsHintergrund(unittest.TestCase):
    @mock_ses
    def test_send_mail(self):
        # given
        payload = {'Username': 'arn:aws:iam::111122223333:user/anaya',
                   'UserAgent': 'Mozilla/5.0 (X11; Kali; rv:64.0) Gecko/20100101 Firefox/64.0',
                   'Pentester': True}

        client = boto3.client('ses', 'eu-central-1')
        client.verify_email_identity(EmailAddress='sender@mail.com')

        # when
        response = guard.send_mail(payload)

        # then
        self.assertEqual(200, response['statusCode'])
        self.assertTrue("Email sent! Response: {" in response['body'])

    @mock_lambda
    def test_lambda_handler_no_mail_sent(self):
        # given
        f = open(
            "{0}/ressources/login_event.json".format(os.path.dirname(__file__)), "r")
        event = json.loads(f.read())
        f.close()

        # when
        response = guard.lambda_handler(event=event, context=None)

        # then
        self.assertEqual({'statusCode': 200}, response)

    @mock_lambda
    @patch("AwsLoginGuard.send_mail")
    def test_lambda_handler_no_mail_sent(self, mail_mock):
        # given
        f = open(
            "{0}/ressources/login_event_malicious.json".format(os.path.dirname(__file__)), "r")
        event = json.loads(f.read())
        f.close()

        # when
        response = guard.lambda_handler(event=event, context=None)

        # then
        self.assertEqual("[call(payload={'Username': 'arn:aws:iam::111122223333:user/h4x0r', 'UserAgent': 'Mozilla/5.0 (Kali Linux; Intel Mac OS X 10.12; rv:62.0) Gecko/20100101 Firefox/62.0', 'Pentester': True})]",
                         str(mail_mock.call_args_list))
        self.assertTrue(mail_mock.called)
        self.assertEqual({'statusCode': 200}, response)