# -*- coding: utf-8 -*-
import unittest
from mobily.utilities import MobilyUnicodeConverter


class TestMobilyUnicode(unittest.TestCase):
    def test_single_byte_characters_with_leading_zeros(self):
        self.assertEqual('000D', MobilyUnicodeConverter('\r').convert())
        self.assertEqual('004D', MobilyUnicodeConverter('M').convert())

    def test_multi_byte_characters(self):
        self.assertEqual('2022', MobilyUnicodeConverter('•').convert())
        self.assertEqual('03C0', MobilyUnicodeConverter('π').convert())

    def test_emoji_characters(self):
        grin_face = '😁'
        self.assertEqual('D83DDE01', MobilyUnicodeConverter(grin_face).convert())
        pile_of_poo = '💩'
        self.assertEqual('D83DDCA9', MobilyUnicodeConverter(pile_of_poo).convert())

    def test_arabic_string_from_api_docs(self):
        exp = '06270647064406270020064806330647064406270020062806430020064506390020006D006F00620069006C0079002E00770073'
        self.assertEqual(exp, MobilyUnicodeConverter('اهلا وسهلا بك مع mobily.ws').convert())


if __name__ == '__main__':
    unittest.main()
