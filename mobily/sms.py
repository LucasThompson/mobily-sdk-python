from mobily.utilities import MobilyApiJsonRequestHandler
from mobily.utilities import MobilyApiError
from mobily.utilities import MobilyApiUnicodeConverter


class MobilySMS(object):
    def __init__(self, auth, numbers, sender, msg, date_send=0, time_send=0, delete_key=None, msg_id=None,
                 domain_name=None, application_type=24):
        self.auth = auth
        self.numbers = numbers
        self.sender = sender
        self.msg = msg
        self.date_send = date_send
        self.time_send = time_send
        self.delete_key = delete_key
        self.msg_id = msg_id
        self.domain_name = domain_name
        self.application_type = application_type
        self.request_handler = MobilyApiJsonRequestHandler(self.auth)

    def add_number(self, number):
        self.numbers.append(number)

    def get_numbers_as_csv(self):
        return ','.join(self.numbers)

    @staticmethod
    def can_send():
        # send status api method wrapper, doesn't need authentication
        request_handler = MobilyApiJsonRequestHandler()
        request_handler.set_api_method('sendStatus')
        try:
            response = request_handler.handle()
        except MobilyApiError:
            return False
        else:
            return response.get('result') == '1'

    def send(self):
        # send sms api method wrapper
        self._prepare_to_send()
        return self.request_handler.handle()

    def delete(self):
        # send sms api method wrapper
        if self.delete_key is None:
            return
        request_handler = MobilyApiJsonRequestHandler(self.auth)
        request_handler.set_api_method('deleteMsg')
        request_handler.add_parameter('deleteKey', self.delete_key)
        return request_handler.handle()

    def _prepare_to_send(self):
        self.request_handler.set_api_method('msgSend')
        self.request_handler.add_parameter('sender', self.sender)
        self.request_handler.add_parameter('msg', MobilyApiUnicodeConverter.convert(self.msg))
        self.request_handler.add_parameter('numbers', self.get_numbers_as_csv())
        self.request_handler.add_parameter('dateSend', self.date_send)
        self.request_handler.add_parameter('timeSend', self.time_send)
        self.request_handler.add_parameter('deleteKey', self.delete_key)
        self.request_handler.add_parameter('msgId', self.msg_id)
        self.request_handler.add_parameter('applicationType', self.application_type)
        self.request_handler.add_parameter('domainName', self.domain_name)


class MobilyFormattedSMS(MobilySMS):
    def __init__(self, auth, numbers, sender, msg, date_send=0, time_send=0, delete_key=None, msg_id=None,
                 domain_name=None, application_type=24):
        super(MobilyFormattedSMS, self).__init__(auth, numbers, sender, msg, date_send, time_send, delete_key, msg_id,
                                                 domain_name, application_type)
        self.variable_dict = {}

    def generate_msg_key(self):
        is_value_set_count_consistent = 1 == len(set([len(val) for val in self.variable_dict.values()]))
        value_set_count_equals_mobile_number_count = len(self.variable_dict) == len(self.numbers)
        is_valid_key = is_value_set_count_consistent and value_set_count_equals_mobile_number_count
        if is_valid_key:
            ordered_number_variables = [self.variable_dict[num] for num in self.numbers]
            return '***'.join(
                map(',@,'.join, map(lambda sym_val: map(',*,'.join, sym_val), ordered_number_variables)))
        else:
            raise ValueError('Cannot generate msgKey, symbol count is inconsistent')

    def add_variable_for_number(self, mobile_number, symbol, value):
        if mobile_number not in self.numbers:
            return
        if mobile_number in self.variable_dict:
            self.variable_dict[mobile_number].append((symbol, value))
        else:
            self.variable_dict.update({mobile_number: [(symbol, value)]})

    def _prepare_to_send(self):
        super(MobilyFormattedSMS, self)._prepare_to_send()
        self.request_handler.add_parameter('msgKey', MobilyApiUnicodeConverter.convert(self.generate_msg_key()))
