# -*- coding: utf-8 -*-
import unittest
from mobily.utilities import MobilyApiRequest
from mobily.utilities import MobilyApiJsonRequestHandler
from mobily.utilities import MobilyApiAuth
from mobily.utilities import MobilyApiResponse
from mobily.utilities import MobilyApiError


class TestMobilyApiRequestHandlersQueryBuilding(unittest.TestCase):

    def test_json_building(self):
        expected_json = '{"Data": {"Method": "balance", "Auth": {"mobile": "test", "password": "test"}}}'
        request = MobilyApiJsonRequestHandler(MobilyApiAuth('test', 'test'))
        request.set_api_method('balance')
        self.assertEqual(expected_json, request.get_request_data())


class TestMobilyApiRequestHandlersRequestParsing(unittest.TestCase):
    # request stub
    class MobilyApiRequestStub(MobilyApiRequest):
        def __init__(self, fake_response):
            MobilyApiRequest.__init__(self)
            self.fake_response = fake_response

        def send(self, request_data='', content_type=''):
            return self.fake_response

    def test_json_parsing_success_response(self):
        fake_response = '''{
        "status":1,
        "ResponseStatus":"success",
        "Data":{
        "result":"1",
        "MessageAr":"يمكنك الإرسال الآن",
        "MessageEn":"You can send SMS now"
        },
        "Error":null
        }
        '''
        expected_response = MobilyApiResponse(1, 'success')
        expected_response.add_data('result', '1')
        expected_response.add_data('MessageAr', 'يمكنك الإرسال الآن')
        expected_response.add_data('MessageEn', 'You can send SMS now')
        handler = MobilyApiJsonRequestHandler(request=self.MobilyApiRequestStub(fake_response))
        self.assertEqual(expected_response, handler.handle())

    def test_json_parsing_throws_on_failure_response(self):
        fake_response = '''{
        "status":1,
        "ResponseStatus":"fail",
        "Data":null,
        "Error":{
        "ErrorCode":0,
        "MessageAr":"بوابة غير معرفة لدينا",
        "MessageEn":"API not exist"
        }
        }'''
        with self.assertRaises(MobilyApiError):
            MobilyApiJsonRequestHandler(request=self.MobilyApiRequestStub(fake_response)).handle()


if __name__ == '__main__':
    unittest.main()
