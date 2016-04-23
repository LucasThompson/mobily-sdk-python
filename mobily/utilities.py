"""
Copyright (c) 2016 Mobily.ws
Code by Lucas Thompson

Utility functions to support the Mobily API.
"""
import sys
import httplib
import xml.etree.ElementTree as ET


class MobilyUnicodeConverter:
    def __init__(self, message):
        self.message = message
        self._ensure_unicode()

    def convert(self):
        return ''.join(['{:04x}'.format(ord(byte)).upper() for byte in self.message])

    def _ensure_unicode(self):
        if sys.version_info < (3,) and type(self.message) is not unicode:
            self.message = unicode(self.message, 'utf-8')


class MobilyAuth:
    def __init__(self, mobile_number, password):
        self.mobile_number = mobile_number
        self.password = password


class MobilyApiRequest:
    def __init__(self, auth, api_host='www.mobily.ws', api_end_point='/api/xml/'):
        self.api_host = api_host
        self.api_end_point = api_end_point
        self.auth = auth
        self.params = ET.Element('MobilySMS')
        ET.SubElement(self.params, 'Auth', attrib={'mobile': auth.mobile_number, 'password': auth.password})

    def add_parameter(self, key, value):
        ET.SubElement(self.params, key).text = value

    def get_request_data(self):
        return ET.tostring(self.params, 'utf-8')

    def send(self):
        return self._post_request_with_xml_data()

    def _post_request_with_xml_data(self):
        headers = {'Content-type': 'application/xml; charset=utf-8'}
        conn = httplib.HTTPConnection(self.api_host)
        conn.request('POST', self.api_end_point, self.get_request_data(), headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return self._parse_xml_response(data)

    @staticmethod
    def _parse_xml_response(data):
        tree = ET.fromstring(data)
        response = MobilyApiResponse(tree.find('Status').text, tree.find('ResponseStatus').text)
        error_element = MobilyApiRequest._element_to_dict(tree.find('Error'))
        is_error = len(list(error_element)) > 0
        data_or_error = 'Error' if is_error else 'Data'
        response_data = MobilyApiRequest._element_to_dict(tree.find(data_or_error))
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
                data.update({child.tag: MobilyApiRequest._element_to_dict(child)})
            else:
                data.update({child.tag: child.text})
        return data


class MobilyApiError(Exception):
    """Exception raised when an MobilyApiRequest indicates the request failed.

    Attributes:
        code         -- the error code returned from the API
        msg_arabic   -- explanation of the error in Arabic
        msg_english  -- explanation of the error in English
    """

    def __init__(self, code, msg_arabic, msg_english):
        self.code = code
        self.msg_arabic = msg_arabic
        self.msg_english = msg_english


class MobilyApiResponse:
    def __init__(self, status, response_status):
        self.status = status
        self.response_status = response_status.lower()
        self.data = {}

    def add_data(self, key, value):
        self.data.update({key: value})

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
