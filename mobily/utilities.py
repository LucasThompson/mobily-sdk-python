import sys


class MobilyUnicodeEncoder:
    def __init__(self, message):
        self.message = message
        self._ensure_unicode()

    def encode(self):
        return ''.join(['{:04x}'.format(ord(byte)).upper() for byte in self.message])

    def _ensure_unicode(self):
        if sys.version_info < (3,):
            if type(self.message) is not unicode:
                self.message = unicode(self.message, 'utf-8')
