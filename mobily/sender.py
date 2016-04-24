from mobily.utilities import MobilyApiXmlRequestHandler


class MobilySender:
    def __init__(self, auth):
        self.auth = auth

    def request_mobile_number_license(self):
        pass

    def activate_mobile_number_license(self):
        pass

    def is_mobile_number_license_active(self):
        pass

    def request_alphabetical_license(self, sender):
        request = MobilyApiXmlRequestHandler(self.auth)
        request.set_api_method('addAlphaSender')
        request.add_parameter('Sender', sender)
        request.handle()

    def is_alphabetical_license_active(self):
        pass

    def get_active_senders(self):
        pass

    def get_pending_senders(self):
        pass

    def get_inactive_senders(self):
        pass
