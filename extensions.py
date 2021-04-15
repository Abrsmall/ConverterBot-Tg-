import requests
import json
from config import APIkey, keys


class APIException(Exception):
    pass


class ValueConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise (f'Не удается обработать валюту {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise (f'Не удается обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise (f'Не удалось обработать количество {amount}')

        try:
            amount > 0
        except ValueError:
            raise ('Количество валюты не может быть меньше 0')


        conv = [base_ticker, quote_ticker]
        q = '_'.join(conv)
        r = requests.get(f'https://free.currconv.com/api/v7/convert?q={q}&compact=ultra&apiKey={APIkey}')
        kurs = (json.loads(r.content)[q])
        result = float(kurs) * float(amount)

        return result