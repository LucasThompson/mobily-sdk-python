# -*- coding: utf-8 -*-
import unittest
from mobily.utilities import MobilyApiXmlRequestHandler
from mobily.utilities import MobilyApiHttpRequestHandler
from mobily.utilities import MobilyApiJsonRequestHandler
from mobily.utilities import MobilyAuth


class TestMobilyApiRequestHandlers(unittest.TestCase):
    def setUp(self):
        self.valid_auth = MobilyAuth('66902258638', 'ThaiSim2016')

    def test_xml_building(self):
        expected_xml = '<MobilySMS>'
        expected_xml += '<Auth mobile="66902258638" password="ThaiSim2016" />'
        expected_xml += '<Method>balance</Method>'
        expected_xml += '</MobilySMS>'
        request = MobilyApiXmlRequestHandler(self.valid_auth)
        request.set_api_method('balance')
        self.assertEqual(expected_xml, request.get_request_data())

    def test_url_building(self):
        expected_url = 'mobile={0}&password={1}'.format(self.valid_auth.mobile_number, self.valid_auth.password)
        request = MobilyApiHttpRequestHandler(self.valid_auth)
        self.assertEqual(expected_url, request.get_request_data())

    def test_json_building(self):
        expected_json = '{{"Data": {{"Method": "balance", "Auth": {{"mobile": "{0}", "password": "{1}"}}}}}}'.format(
            self.valid_auth.mobile_number, self.valid_auth.password)
        request = MobilyApiJsonRequestHandler(self.valid_auth)
        request.set_api_method('balance')
        self.assertEqual(expected_json, request.get_request_data())


if __name__ == '__main__':
    unittest.main()
