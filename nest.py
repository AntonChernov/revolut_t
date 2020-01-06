# -*- coding: utf-8 -*-
import argparse
import json
import os
import logging

logging.basicConfig(
    format='%(asctime)s %(message)s',
    level=logging.DEBUG)


class DataHandler(object):

    def __init__(
            self,
            file_path=None,
            currency=None,
            country=None,
            city=None):
        self.currency = currency
        self.country = country
        self.city = city
        self.path_to_file = self.file_exist(file_path)
        logging.info('Path: {0}'.format(self.path_to_file))

    def file_exist(self, path):
        _ = path if path else ''.join([os.path.curdir, '/data.json'])
        if os.path.exists(_) \
                and os.path.isfile(_) \
                and _.endswith('.json'):
            return _
        raise OSError('Path not exist or '
                      'file not found or '
                      'file not in json '
                      'format! {0}'.format(path))

    def data_file_reader(self):
        with open(self.path_to_file, 'r') as f:
            logging.debug(f)
            logging.debug(f.readlines())
            result = json.loads(f.readlines())

        logging.debug('Result: {0}'.format(result))
        return result

    def data_parser(self):
        raise NotImplemented

    def vars(self):
        logging.info('Variables: {0}'.format(
            [self.city, self.city, self.path_to_file]))


if __name__ == "__main__":
    """
    currency country city
    """
    input_args = argparse.ArgumentParser()
    input_args.add_argument(
        '--path',
        '-p',
        dest='file_path',
        action='store',
        help='Path to "JSON" file.')

    input_args.add_argument(
        '--country',
        '-c',
        dest='country',
        action='store',
        help='Country name or names separated by "," ')

    input_args.add_argument(
        '--city',
        '-ci',
        dest='city',
        action='store',
        help='City name or names separated by "," ')

    input_args.add_argument(
        '--currency',
        '-cur',
        dest='currency',
        action='store',
        help='Currency name or names separated by "," '
    )

    args = input_args.parse_args()
    print(args)
    print(type(args))
    res = DataHandler(
        file_path=args.file_path,
        currency=args.currency,
        country=args.country,
        city=args.city)
    res.data_file_reader()



