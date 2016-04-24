from mobily.utilities import MobilyApiXmlRequestHandler


class MobilySMS:
    def __init__(self, auth):
        self.auth = auth
        self.numbers = []
        self.sender = ''
        self.msg = ''
        self.date_send = 0
        self.time_send = 0
        self.delete_key = None
        self.msg_id = None
        self.application_type = 24

    def add_number(self, number):
        self.numbers.append(number)

    def get_numbers_as_csv(self):
        return ','.join(self.numbers)

    @staticmethod
    def can_send():
        # send status api method wrapper
        request = MobilyApiXmlRequestHandler()
        request.set_api_method('sendStatus')  # did i want HTTP?

    def delete(self):
        if self.delete_key is None:
            return

    def send(self):
        # send sms method wrapper
        pass


class MobilyFormattedSMS(MobilySMS):
    def __init__(self, auth):
        MobilySMS.__init__(self, auth)
