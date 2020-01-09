# -*- coding: utf-8 -*-
import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import (
    APIRequestFactory, APIClient,
    force_authenticate, APITestCase
)

from rest_framework.authtoken.models import Token


class NestedApiTests(APITestCase):

    def setUp(self):
        self.request_client = APIClient()
        self.user, self.is_created = User.objects.get_or_create(
            username='test',
            email='test@gmail.com',
            password='somedifficultpass'
        )
        self.url = reverse('nested')
        print(self.url)

        self.data = [
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
            },
            {
                "country": "ES",
                "city": "Madrid",
                "currency": "EUR",
                "amount": 9.9
            },
            {
                "country": "ES",
                "city": "Madrid",
                "currency": "EUR",
                "amount": 8.9
            },
            {
                "country": "UK",
                "city": "London",
                "currency": "GBP",
                "amount": 12.2
            },
            {
                "country": "UK",
                "city": "London",
                "currency": "FBP",
                "amount": 10.9
            }
        ]

    def tearDown(self):
        self.user.delete()
        # self.token.delete()

    def test_url(self):
        self.assertEquals(self.url, '/api/nested/')
        self.assertIsInstance(self.url, str)

    def test_not_authorized(self):
        uri = self.url + '?currency=EUR'
        r = self.request_client.post(uri)
        # No data no answer
        self.assertEquals(r.status_code, 401)

    def test_no_data_in_body(self):
        self.token = Token.objects.get(user=self.user)
        self.request_client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key
        )
        uri = self.url + '?currency=EUR'
        r = self.request_client.post(uri)
        # No data no answer
        self.assertEquals(r.status_code, 400)

    def test_positive(self):
        self.token = Token.objects.get(user=self.user)
        self.request_client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key
        )
        uri = self.url + '?currency=EUR'
        r = self.request_client.post(uri, data=self.data, format='json')
        self.assertEquals(r.status_code, 200)

    def test_empty_currency(self):
        self.token = Token.objects.get(user=self.user)
        self.request_client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key
        )
        uri = self.url + '?currency='
        r = self.request_client.post(uri, data=self.data, format='json')

        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.data), '{"": {}}')
