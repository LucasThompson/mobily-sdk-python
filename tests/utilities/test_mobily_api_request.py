# -*- coding: utf-8 -*-
import unittest
from mobily.utilities import MobilyApiRequest
from mobily.utilities import MobilyApiResponse
from mobily.utilities import MobilyAuth


class TestMobilyApiRequest(unittest.TestCase):
    def test_xml_building(self):
        expected_xml = '<MobilySMS>'
        expected_xml += '<Auth mobile="66902258638" password="ThaiSim2016" />'
        expected_xml += '<Method>balance</Method>'
        expected_xml += '</MobilySMS>'
        request = MobilyApiRequest(MobilyAuth('66902258638', 'ThaiSim2016'))
        request.add_parameter('Method', 'balance')
        self.assertEqual(expected_xml, request.get_request_data())

    def test_balance_request(self):
        request = MobilyApiRequest(MobilyAuth('66902258638', 'ThaiSim2016'))
        request.add_parameter('Method', 'balance')
        expected_response = MobilyApiResponse('1', 'success')
        expected_response.add_data('balance', {'current': '1', 'total': '3'})
        response = request.send()
        print response.__dict__
        print expected_response.__dict__
        self.assertEqual(expected_response, response)


if __name__ == '__main__':
    unittest.main()
