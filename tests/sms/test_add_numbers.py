# -*- coding: utf-8 -*-
import unittest
from mobily.sms import MobilySMS


class TestAddNumbers(unittest.TestCase):
    def test_empty_list(self):
        sms = MobilySMS(None)
        self.assertEqual('', sms.get_numbers_as_csv())

    def test_produces_well_formed_csv(self):
        sms = MobilySMS(None)
        sms.add_number('12345678910')
        sms.add_number('23456789101')
        self.assertEqual('12345678910,23456789101', sms.get_numbers_as_csv())

if __name__ == '__main__':
    unittest.main()
