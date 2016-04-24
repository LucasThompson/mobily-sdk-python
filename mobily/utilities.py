"""
Copyright (c) 2016 Mobily.ws
Code by Lucas Thompson

Utility functions to support the Mobily API.
"""
import sys
import httplib
import urllib
import xml.etree.ElementTree as ET
import json


class MobilyUnicodeConverter(object):
    def __init__(self, message):
        self.message = u(message)

    def convert(self):
        return ''.join(['{:04x}'.format(ord(byte)).upper() for byte in self.message])


def u(s):
    if sys.version_info < (3,) and type(s) is not unicode:
        return unicode(s, 'utf-8')
    else:
        return s


class MobilyAuth(object):
    def __init__(self, mobile_number, password):
        self.mobile_number = mobile_number
        self.password = password


class MobilyApiResponse(object):
    def __init__(self, status, response_status):
        self.status = status
        self.response_status = response_status.lower()
        self.data = {}

    def add_data(self, key, value):
        self.data.update({u(key): u(value)})

    def get(self, key):
        return self.data[key] if key in self.data else None

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class MobilyApiError(Exception):
    """Exception raised when an a RequestHandler indicates the request failed.

    Attributes:
        code         -- the error code returned from the API
        msg_arabic   -- explanation of the error in Arabic
        msg_english  -- explanation of the error in English
    """

    def __init__(self, code, msg_arabic, msg_english):
        super(MobilyApiError, self).__init__(msg_english, )
        self.code = code
        self.msg_arabic = msg_arabic
        self.msg_english = msg_english


class MobilyApiRequest(object):
    def __init__(self, api_host='www.mobily.ws', api_end_point='/api/'):
        self.api_host = api_host
        self.api_end_point = api_end_point

    def send(self, request_data, content_type):
        headers = {'Content-type': 'application/{0}; charset=utf-8'.format(content_type)}
        conn = httplib.HTTPConnection(self.api_host)
        conn.request('POST', self.api_end_point, request_data, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data


class MobilyApiHttpRequestHandler(object):
    def __init__(self, auth=None, request=MobilyApiRequest(api_end_point='/api/')):
        self.request = request
        self.auth = auth
        self.content_type = 'x-www-form-urlencoded'
        self.params = {}
        self.error_predicate = None
        self.error = None
        self.add_auth(auth)

    def add_auth(self, auth):
        if isinstance(auth, MobilyAuth):
            self.add_parameter('mobile', auth.mobile_number)
            self.add_parameter('password', auth.password)

    def set_api_method(self, method_name):
        self.request.api_end_point = '/api/{0}.php'.format(method_name)

    def add_parameter(self, key, value):
        if value is not None:
            self.params.update({key: value})

    def get_request_data(self):
        return urllib.urlencode(self.params)

    def handle(self):
        return self._parse_response(self.request.send(self.get_request_data(), self.content_type))

    def _parse_response(self, data):
        if callable(self.error_predicate) and self.error_predicate(data):
            raise self.error
        return data


class MobilyApiJsonRequestHandler(MobilyApiHttpRequestHandler):
    def __init__(self, auth=None, request=MobilyApiRequest(api_end_point='/api/json/')):
        super(MobilyApiJsonRequestHandler, self).__init__(request=request)
        self.content_type = 'json'
        self.auth = auth
        self.json_dict = {'Data': {}}

    def add_auth(self, auth):
        if isinstance(auth, MobilyAuth):
            self.json_dict['Data'].update({'Auth': {'mobile': auth.mobile_number, 'password': auth.password}})

    def set_api_method(self, method_name):
        self.json_dict['Data'].update({'Method': method_name})

    def get_request_data(self):
        self.add_auth(self.auth)
        if len(self.params) > 0:
            self.json_dict['Data'].update({'Params': self.params})
        return json.dumps(self.json_dict)

    def _parse_response(self, data):
        json_dict = json.loads(data, encoding='utf-8')
        is_error = json_dict['Error'] is not None
        if is_error:
            error = json_dict['Error']
            raise MobilyApiError(error['ErrorCode'], error['MessageAr'], error['MessageEn'])
        response = MobilyApiResponse(json_dict['status'], json_dict['ResponseStatus'])
        for key, value in json_dict['Data'].iteritems():
            response.add_data(key, value)
        return response


class MobilyApiXmlRequestHandler(MobilyApiHttpRequestHandler):
    def __init__(self, auth=None, request=MobilyApiRequest(api_end_point='/api/xml/')):
        super(MobilyApiXmlRequestHandler, self).__init__(request=request)
        self.content_type = 'xml'
        self.params = ET.Element('MobilySMS')
        self.add_auth(auth)

    def add_auth(self, auth):
        if isinstance(auth, MobilyAuth):
            ET.SubElement(self.params, 'Auth', attrib={'mobile': auth.mobile_number, 'password': auth.password})

    def set_api_method(self, method_name):
        self.add_parameter('Method', method_name)

    def add_parameter(self, key, value):
        if value is not None:
            ET.SubElement(self.params, key).text = value

    def get_request_data(self):
        return ET.tostring(self.params, 'utf-8')

    def _parse_response(self, data):
        tree = ET.fromstring(data)
        response = MobilyApiResponse(tree.find('Status').text, tree.find('ResponseStatus').text)
        error_element = self._element_to_dict(tree.find('Error'))
        is_error = len(list(error_element)) > 0
        data_or_error = 'Error' if is_error else 'Data'
        response_data = self._element_to_dict(tree.find(data_or_error))
        if is_error:
            raise MobilyApiError(response_data['ErrorCode'], response_data['MessageAr'], response_data['MessageEn'])
        for key, value in response_data.iteritems():
            response.add_data(key, value)
        return response

    @staticmethod
    def _element_to_dict(element):
        data = {}
        for child in element:
            if len(list(child)) > 0:
                data.update({child.tag: MobilyApiXmlRequestHandler._element_to_dict(child)})
            else:
                data.update({child.tag: child.text})
        return data
