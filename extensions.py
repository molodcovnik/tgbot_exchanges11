import json
import requests
from config import exchanges

class APIException(Exception):
    pass


class Exchanges:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f'Валюта {base} не найдена!')

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f'Валюта {sym} не найдена!')

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/f22c740943b2bd73171fbacb/latest/{base_key}')
        s = json.loads(r.content)
        result = (s['conversion_rates'][sym_key] * amount)
        message = (f'{amount} {base} в {sym} : {round(result, 4)}')
        return message
