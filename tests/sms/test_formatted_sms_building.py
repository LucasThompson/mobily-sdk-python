import unittest
from mobily.sms import MobilyFormattedSMS


class TestFormattedSmsBuilding(unittest.TestCase):
    def test_generates_valid_msg_key_vars_added_in_same_order(self):
        msg = 'Hi (1), your subscription will end on (2).'
        numbers = ['966505555555', '966504444444']
        sms = MobilyFormattedSMS(None, numbers, 'NEW SMS', msg)
        sms.add_variable_for_number('966505555555', '(1)', 'Ahmad')
        sms.add_variable_for_number('966505555555', '(2)', '31/12/2013')
        sms.add_variable_for_number('966504444444', '(1)', 'Mohamed')
        sms.add_variable_for_number('966504444444', '(2)', '01/11/2013')
        exp_msg_key = '(1),*,Ahmad,@,(2),*,31/12/2013***(1),*,Mohamed,@,(2),*,01/11/2013'
        self.assertEqual(exp_msg_key, sms.generate_msg_key())

    def test_generates_valid_msg_key_vars_added_in_different_order(self):
        msg = 'Hi (1), your subscription will end on (2).'
        numbers = ['966505555555', '966504444444']
        sms = MobilyFormattedSMS(None, numbers, 'NEW SMS', msg)
        sms.add_variable_for_number('966504444444', '(1)', 'Mohamed')
        sms.add_variable_for_number('966505555555', '(1)', 'Ahmad')
        sms.add_variable_for_number('966504444444', '(2)', '01/11/2013')
        sms.add_variable_for_number('966505555555', '(2)', '31/12/2013')
        exp_msg_key = '(1),*,Ahmad,@,(2),*,31/12/2013***(1),*,Mohamed,@,(2),*,01/11/2013'
        self.assertEqual(exp_msg_key, sms.generate_msg_key())

    def test_throws_when_not_enough_value_sets(self):
        msg = 'Hi (1), your subscription will end on (2).'
        numbers = ['966505555555', '966504444444']
        sms = MobilyFormattedSMS(None, numbers, 'NEW SMS', msg)
        sms.add_variable_for_number('966505555555', '(1)', 'Ahmad')
        sms.add_variable_for_number('966505555555', '(2)', '31/12/2013')
        with self.assertRaises(ValueError):
            sms.generate_msg_key()

    def test_throws_when_value_sets_are_unbalanced(self):
        msg = 'Hi (1), your subscription will end on (2).'
        numbers = ['966505555555', '966504444444']
        sms = MobilyFormattedSMS(None, numbers, 'NEW SMS', msg)
        sms.add_variable_for_number('966505555555', '(1)', 'Ahmad')
        sms.add_variable_for_number('966505555555', '(2)', '31/12/2013')
        sms.add_variable_for_number('966504444444', '(1)', 'Mohamed')
        with self.assertRaises(ValueError):
            sms.generate_msg_key()


if __name__ == '__main__':
    unittest.main()
