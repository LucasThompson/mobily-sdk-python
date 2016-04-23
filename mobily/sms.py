from mobily.utilities import MobilyApiRequest


class MobilySMS:
    def __init__(self, auth):
        self.auth = auth

    @staticmethod
    def can_send():
        # send status api method wrapper
        request = MobilyApiRequest()
        request.add_parameter('Method', 'sendStatus')

    def send(self):
        # send sms method wrapper
        pass

    def send_formatted(self):
        # send sms formatted method wrapper
        pass

    def delete(self):
        # delete sms method wrapper
        pass
