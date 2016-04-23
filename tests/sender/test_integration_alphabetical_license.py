import unittest
from mobily.utilities import MobilyApiError
from mobily.utilities import MobilyAuth
from mobily.sender import MobilySender


class TestIntegrationSenderAlphabeticalLicense(unittest.TestCase):
    def setUp(self):
        self.valid_auth = MobilyAuth('66902258638', 'ThaiSim2016')

    def test_throws_exception_with_invalid_auth(self):
        with self.assertRaises(MobilyApiError):
            sender = MobilySender(MobilyAuth('INVALID_MOBILE', ''))
            sender.request_alphabetical_license('Test')

    def test_throws_exception_with_long_name(self):
        with self.assertRaises(MobilyApiError):
            sender = MobilySender(self.valid_auth)
            sender.request_alphabetical_license('MoreThanElevenCharacters')


if __name__ == '__main__':
    unittest.main()
