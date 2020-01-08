# -*- coding: utf-8 -*-
import unittest


class CLITests(unittest.TestCase):

    def setUp(self) -> None:
        self.correct_data = [
            {
                "country": "US",
                "city": "Boston",
                "currency": "USD",
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
            }
        ]

        self.empty_data = []


