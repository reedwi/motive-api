from api.motive import MotiveAPI
from helpers.data_helpers import parse_items
import requests
import os
import json

def get_all_data(token):
    for item in ['users', 'vehicles', 'assets']:
        api_module = MotiveAPI(item=item, token=token, request_type='install')
        all_raw_items = api_module.get_items()
        all_assets = parse_items(all_raw_items, item[:-1])
        data = {
            item: all_assets
        }
        requests.post(url=os.getenv('DUMP_URL'), data=data)
    