# -*- coding: utf-8 -*-
import unittest

from nest import DataHandler


class CLITests(unittest.TestCase):

    def setUp(self):
        self.test_correct_data_gud_state = {
            'EUR': {
                'FR': {'Lyon': [{'amount': 11.4}]},
                'ES': {'Madrid': [{'amount': 9.9}, {'amount': 8.9}]}
            }
        }

        self.not_full_data = [
            {
                "country": "US",
                "city": "Boston",
                "amount": 100
            },
            {
                "country": "FR",
                "city": "Paris",
                "currency": "EUR",
                "amount": 20
            },
            {
                "country": "FR",
                "city": "Lyon",
                "currency": "EUR",
                "amount": 11.4
            },
        ]

    def test_correct_data(self):
        d_builder = DataHandler(currency='EUR')
        res = d_builder.result_builder()
        self.assertIsNotNone(res)
        self.assertEquals(res, self.test_correct_data_gud_state)

    def test_empty_data(self):
        d_builder = DataHandler(currency='')
        res = d_builder.result_builder()
        self.assertEquals(res, {'': {}})

    def test_data_not_full(self):
        d_builder = DataHandler(file_path=self.not_full_data,currency='USD',)

        with self.assertRaises(KeyError):
            res = d_builder.result_builder()


