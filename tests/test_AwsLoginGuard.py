from re import S
import unittest
import AwsLoginGuard as guard


class TestAwsLoginGuard(unittest.TestCase):
    def test_check_user_agent_regular(self):
        # given
        ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:62.0) Gecko/20100101 Firefox/62.0"

        # when
        result = guard.check_user_agent(user_agent=ua)

        # then
        self.assertEqual(False, result)

    def test_check_user_agent_pentester(self):
        pentoo = "Mozilla/5.0 (X11; Pentoo; rv:64.0) Gecko/20100101 Firefox/64.0"
        kali = "Mozilla/5.0 (X11; Kali; rv:64.0) Gecko/20100101 Firefox/64.0"
        parrot = "Mozilla/5.0 (X11; ParrotOS; rv:64.0) Gecko/20100101 Firefox/64.0"

        self.assertTrue(guard.check_user_agent(user_agent=pentoo))
        self.assertTrue(guard.check_user_agent(user_agent=kali))
        self.assertTrue(guard.check_user_agent(user_agent=parrot))

    def test_is_user_in_whitelist(self):
        self.assertTrue(guard.is_user_in_whitelist('AIDACKCEVSQ6C2EXAMPLE'))
        self.assertFalse(guard.is_user_in_whitelist('AIDACVEXAMPLE'))

    def test_create_body_payload(self):
        # given
        arn = "arn:aws:iam::111122223333:user/anaya"
        kali = "Mozilla/5.0 (X11; Kali; rv:64.0) Gecko/20100101 Firefox/64.0"
        expectation = {'Username': 'arn:aws:iam::111122223333:user/anaya',
                       'UserAgent': 'Mozilla/5.0 (X11; Kali; rv:64.0) Gecko/20100101 Firefox/64.0',
                       'Pentester': True}

        # when
        result = guard.create_body_payload(arn=arn, user_agent=kali)

        # then
        self.assertEqual(result, expectation)
