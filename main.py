import json
import random
import requests
from concurrent.futures import ThreadPoolExecutor
from db_code import data_symbol

proxies = []
with open('proxy.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        proxy = "http://" + line.strip()
        proxies.append(proxy)


def async_search_full_name_token(symbol_to_find):
    proxy = random.choice(proxies)
    proxies_dict = {
        "http": proxy,
    }

    url = 'https://api.coingecko.com/api/v3/coins/list'
    response = requests.get(url, proxies=proxies_dict)
    coins_list = response.json()
    for coin in coins_list:
        if coin['symbol'] == symbol_to_find:
            return coin['name']


def async_get_token_contract(symbol, network):
    proxy = random.choice(proxies)
    proxies_dict = {
        "http": proxy,
    }

    url = f'https://api.coingecko.com/api/v3/coins/{symbol.lower()}?localization=false'
    response = requests.get(url, proxies=proxies_dict)
    token_info = response.json()

    platforms = token_info.get('platforms', {})
    contract = platforms.get(network, {})

    return {network: contract}


def process_item(item):
    symbol = item['symbol']
    if symbol[3:] == "USDT":
        new_item = {key: value for key, value in item.items() if key != 'symbol'}
        new_item = json.dumps(new_item)

        symbol_short = symbol[:3].lower()

        full_name_symbol = async_search_full_name_token(symbol_short)

        contract_token = {
            "ethereum": async_get_token_contract(full_name_symbol, "ethereum"),
            "binance-smart-chain": async_get_token_contract(full_name_symbol, "binance-smart-chain")
        }

        contract_token_json = json.dumps(contract_token)
        print(symbol, new_item, contract_token_json)
        print("+++++++++++++++++++++++++++++++++")
        data_symbol(symbol, new_item, contract_token_json)


def quotes_and_symbols():
    url_tickers = 'https://api.bitget.com/api/spot/v1/market/tickers'
    response = requests.get(url_tickers)

    if response.status_code == 200:
        result = response.json()

        items = result['data']

        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(process_item, items)


quotes_and_symbols()
