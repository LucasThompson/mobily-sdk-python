# -*- coding: utf-8 -*-
import unittest
from mobily.utilities import MobilyUnicodeEncoder


class TestMobilyUnicode(unittest.TestCase):
    def test_single_byte_characters_with_leading_zeros(self):
        encoder = MobilyUnicodeEncoder('\r')
        self.assertEqual('000D', encoder.encode())
        encoder = MobilyUnicodeEncoder('M')
        self.assertEqual('004D', encoder.encode())

    def test_multi_byte_characters(self):
        encoder = MobilyUnicodeEncoder('•')
        self.assertEqual('2022', encoder.encode())
        encoder = MobilyUnicodeEncoder('π')
        self.assertEqual('03C0', encoder.encode())

    def test_emoji_characters(self):
        grin_face = '😁'
        encoder = MobilyUnicodeEncoder(grin_face)
        self.assertEqual('D83DDE01', encoder.encode())
        pile_of_poo = '💩'
        encoder = MobilyUnicodeEncoder(pile_of_poo)
        self.assertEqual('D83DDCA9', encoder.encode())

    def test_arabic_string_from_api_docs(self):
        encoder = MobilyUnicodeEncoder('اهلا وسهلا بك مع mobily.ws')
        exp = '06270647064406270020064806330647064406270020062806430020064506390020006D006F00620069006C0079002E00770073'
        self.assertEqual(exp, encoder.encode())
