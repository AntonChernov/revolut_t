# -*- coding: utf-8 -*-
import argparse
import json
import os
import logging
from pprint import pprint

from pandas import read_json

logging.basicConfig(
    format='%(asctime)s %(message)s',
    level=logging.DEBUG)


class DataHandler(object):
    """
    Class handle the job related to nested
    """

    def __init__(
            self,
            file_path='',
            currency=None,
    ):
        self.currency = self.check_currency(currency)
        self.path_to_file = self.file_exist(file_path)
        logging.info('Path: {0}'.format(self.path_to_file))

    def check_currency(self, cur):
        """

        :param cur:
        :type cur: str
        :return: list of currency or TypeError
        :rtype:
        """
        if isinstance(cur, str):
            logging.debug('STR {0}'.format(cur))
            return cur.split(',')
        elif isinstance(cur, list):
            logging.debug('list {0}'.format(cur))
            return cur
        else:
            logging.debug('Bad {0}'.format(cur))
            raise TypeError('Unrecognized type of currency!')

    def file_exist(self, path):
        """
        Check path if path is file return path if path it is list return list
        :param path: path
        :type path: str
        :return: str or list or AttributeError
        :rtype:
        """
        if isinstance(path, str):
            _ = path if path else ''.join([os.path.curdir, '/data.json'])
            if os.path.exists(_) \
                    and os.path.isfile(_) \
                    and _.endswith('.json'):
                return _
            raise OSError('Path not exist or '
                          'file not found or '
                          'file not in json '
                          'format! {0}'.format(path))
        elif isinstance(path, list):
            return path
        else:
            raise AttributeError

    def data_file_reader(self):
        """
        Read file if self.path_to_file == str
        :return: path to file or load the object(list of dicts in our case)
        :rtype:
        """
        if isinstance(self.path_to_file, str) and self.path_to_file:
            with open(self.path_to_file, 'r') as f:
                readed_obj = f.read()
            logging.debug('Read data from file: {0}'.format(readed_obj))
            return json.loads(readed_obj)
        elif isinstance(self.path_to_file, list):
            return self.path_to_file

    def data_file_reader_pandas(self):
        """
        Read file use pandas lib
        :return: DataFrame
        :rtype:
        """
        self.df = read_json(self.path_to_file, orient='records')
        logging.debug('DF: {0}'.format(self.df))

    def result_builder_pandas(self, json_format=None):
        """
        Build a result
        :param json_format: None/something(True,1, 'asd' some not Null value)
        :type json_format:
        :return: If json_format --> response in json format
                 if None usual dict format will be use
        :rtype:
        """
        res = {}
        for cur in self.currency:
            d = self.aggregated_data[
                self.aggregated_data['currency'] == cur
            ]
            aggr = self.aggregate(d)
            res.update({cur: aggr})
        logging.debug('Result:{0}'.format(res))
        if not json_format:
            return pprint(res, indent=4)
        return json.dumps(res)

    def result_builder(self, json_format=None):
        """
        Build result without anu helping libs python
        :param json_format: json_format:
        None/something(True,1, 'asd' some not Null value)
        :type json_format:
        :return: If json_format --> response in json format
                 if None usual dict format will be use
        :rtype:
        :result example for: python nest.py --currency EUR,USD



        {
        'EUR': {
            'FR': {
                'Lyon': [
                    {'amount': 11.4}]
                },
            'ES': {
            'Madrid': [
                {
                    'amount': 9.9
                },
                {
                    'amount': 8.9
                }
            ]
            }
            },
            'USD': {
                'US': {
                    'Boston': [
                        {
                            'amount': 100
                        }
                    ]
                }
            }
        }
        """
        data = self.data_file_reader() #if not web else web
        logging.debug(data)
        res = {}
        for cur in self.currency:
            items = [item for item in data if item['currency'] == cur]
            logging.debug(items)
            countries_codes = {c['country'] for c in items}
            countries_data = {}
            for cc in countries_codes:
                countries_data.update(
                    {
                        # cc: {item['city']: [
                        #     {
                        #         'amount': item['amount']
                        #     }
                        # ]
                        cc: {
                            item['city']: self.item_amount(items, item['city'])
                        } for item in items if item['country'] == cc
                    }
                )
            res.update(
                {
                    cur: countries_data
                }
            )
        logging.debug(res)
        if not json_format:
            logging.debug(res)
            return res
        return json.dumps(res)

    def item_amount(self, items, city):
        """
        HElp method for collect more then one amout base on currency and city
        :param items: currency filtered items
        :type items:
        :param city: City name
        :type city:
        :return: list of amounts
        :rtype:
        """
        return [
            {'amount': item['amount']}
            for item in items if item['city'] == city
        ]

    def aggregate(self, data_frame):
        """
        Data aggregator based on Pandas lib
        :param data_frame: pandas DataFrame
        :type data_frame:
        :return: List of Currencies with cities and amount for each city
        :rtype:
        """
        country_codes = data_frame['country'].unique()
        logging.debug('CC: {0}'.format(country_codes))
        result = {}
        for country_code in country_codes:
            country = data_frame[data_frame['country'] == country_code]
            logging.debug('Country: {0}'.format(country))
            country_data = {}
            cities_names = country['city'].unique()
            for city in cities_names:
                c = data_frame[data_frame['city'] == city]
                logging.debug('City: {0}'.format(c))
                logging.debug('City type: {0}'.format(type(c)))
                country_data.update({
                    city: [
                        {'amount': row['amount']}
                        for index, row in c.iterrows()
                    ]
                })
            logging.debug('Country data: {0}'.format(country_data))
            result.update({country_code: country_data})
        logging.debug(result)
        return result


if __name__ == "__main__":
    """
    Entry point for CLI
    """
    input_args = argparse.ArgumentParser()
    input_args.add_argument(
        '--path',
        '-p',
        dest='file_path',
        default='',
        action='store',
        help='Path to "JSON" file.')

    input_args.add_argument(
        '--currency',
        '-cur',
        dest='currency',
        action='store',
        help='Currency name or names separated by "," '
    )

    args = input_args.parse_args()
    res = DataHandler(
        file_path=args.file_path,
        currency=args.currency,
    )

    res.result_builder(json_format=True)



