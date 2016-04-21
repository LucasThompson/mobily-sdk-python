# -*- coding: utf-8 -*-
import unittest
from mobily.utilities import MobilyUnicodeEncoder


class TestMobilyUnicode(unittest.TestCase):
    def test_multiple_bytes(self):
        encoder = MobilyUnicodeEncoder('•')
        self.assertEqual('00E2008000A2', encoder.encode())
        encoder = MobilyUnicodeEncoder('π')
        self.assertEqual('00CF0080', encoder.encode())

    def test_single_byte_with_leading_zeros(self):
        encoder = MobilyUnicodeEncoder('\r')
        self.assertEqual('000D', encoder.encode())
        encoder = MobilyUnicodeEncoder('M')
        self.assertEqual('004D', encoder.encode())

    def test_arabic_string_from_api_docs(self):
        encoder = MobilyUnicodeEncoder('اهلا وسهلا بك مع mobily.ws')
        exp = '06270647064406270020064806330647064406270020062806430020064506390020006D006F00620069006C0079002E00770073'
        self.assertEqual(exp, encoder.encode())
