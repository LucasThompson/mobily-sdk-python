class MobilyUnicodeEncoder:
    def __init__(self, message):
        self.message = message

    def encode(self):
        return ''.join(['{:04x}'.format(ord(byte)).upper() for byte in self.message])
