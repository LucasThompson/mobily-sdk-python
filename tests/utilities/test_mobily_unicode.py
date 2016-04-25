# -*- coding: utf-8 -*-
import unittest
from mobily.utilities import MobilyApiUnicodeConverter


class TestMobilyUnicode(unittest.TestCase):
    def test_single_byte_characters_with_leading_zeros(self):
        self.assertEqual('000D', MobilyApiUnicodeConverter.convert('\r'))
        self.assertEqual('004D', MobilyApiUnicodeConverter.convert('M'))

    def test_multi_byte_characters(self):
        self.assertEqual('2022', MobilyApiUnicodeConverter.convert('•'))
        self.assertEqual('03C0', MobilyApiUnicodeConverter.convert('π'))

    def test_emoji_characters(self):
        grin_face = '😁'
        self.assertEqual('D83DDE01', MobilyApiUnicodeConverter.convert(grin_face))
        pile_of_poo = '💩'
        self.assertEqual('D83DDCA9', MobilyApiUnicodeConverter.convert(pile_of_poo))

    def test_arabic_string_from_api_docs(self):
        exp = '06270647064406270020064806330647064406270020062806430020064506390020006D006F00620069006C0079002E00770073'
        self.assertEqual(exp, MobilyApiUnicodeConverter.convert('اهلا وسهلا بك مع mobily.ws'))


if __name__ == '__main__':
    unittest.main()
