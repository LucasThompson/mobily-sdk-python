import unittest
from mobily.utilities import MobilyApiError
from mobily.utilities import MobilyApiAuth
from mobily.sender import MobilySender


class TestIntegrationSenderAlphabeticalLicense(unittest.TestCase):
    def setUp(self):
        self.valid_auth = MobilyApiAuth('66902258638', 'ThaiSim2016')

    def test_throws_exception_with_invalid_auth(self):
        with self.assertRaises(MobilyApiError):
            sender = MobilySender(MobilyApiAuth('INVALID_MOBILE', ''))
            sender.request_alphabetical_license('Test')

    def test_throws_exception_with_long_name(self):
        with self.assertRaises(MobilyApiError):
            sender = MobilySender(self.valid_auth)
            sender.request_alphabetical_license('MoreThanElevenCharacters')


if __name__ == '__main__':
    unittest.main()
