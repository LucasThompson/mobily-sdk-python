import unittest
from mobily.sms import MobilySMS


class IntegrationTestSmsMethods(unittest.TestCase):
    def test_send_status_is_boolean(self):
        # doesn't matter if the response from the server is positive or not
        # we just want to know that the method interprets the response or errors properly
        self.assertIn(MobilySMS.can_send(), [True, False])


if __name__ == '__main__':
    unittest.main()
