import requests
from authlib.integrations.requests_client import OAuth2Session
import os
from dotenv import load_dotenv
from pprint import pprint
from helpers.logger import get_logger
load_dotenv()

class MotiveAPI():
    """
    Class that can be used to access the motive API
    Initializes some constant variables and passes to a dynamic function to get values
    """    
    def __init__(self, request_type=None, per_page=100, item=None, token=None, refresh_token=None):
        self.CLIENT_ID = os.getenv('CLIENT_ID')
        self.CLIENT_SECRET = os.getenv('CLIENT_SECRET')
        self.REDIRECT_URI = os.getenv('REDIRECT_URI')
        self.REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
        self.INSTALL_REFRESH_TOKEN = refresh_token
        self.request_type = request_type
        self.token = token
        self.base_url = 'https://api.gomotive.com/v1/'
        self.headers = {
            'Authorization': f'Bearer {self._token}',
            'Accept': 'application/json'
        }
        self.item = item
        self.per_page = per_page
        self.has_more = True
        self.page_number = 1
        self.logger = get_logger(f'motive_api.{__name__}')
    
    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, x):
        if self.request_type == 'install':
            self._token = x
        else:
            self._token = self.get_refresh()
        
    def auth(self):
        url = 'https://api.gomotive.com/oauth/authorize'
        client = OAuth2Session(
            client_id=self.CLIENT_ID,
            client_secret=self.CLIENT_SECRET,
            scope=['users.read', 'vehicles.read', 'eld_devices.read', 'assets.read'],
            redirect_uri=self.REDIRECT_URI
        )
        uri, state = client.create_authorization_url(url)
        return uri

    def get_refresh(self):
        # CHeck if access token is still valid
        url = f'{self.base_url}{self.item}'
        params = {
            'per_page': 1,
            'page_no': 1
        }
        headers = {
            'Authorization': f'Bearer {os.getenv("TOKEN")}',
            'Accept': 'application/json'
        }
        api_req = requests.get(
            url=url,
            headers=headers,
            params=params
        )
        pprint(api_req)
        if api_req.status_code == 200:
            return os.getenv('TOKEN')

        # Generate new access token
        url = 'https://api.gomotive.com/oauth/token'
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.REFRESH_TOKEN,
            'redirect_uri': self.REDIRECT_URI,
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET
        }
        res = requests.post(url=url, data=data)

        try:
            token = res.json()['access_token']
            return token
        except:
            return os.getenv('TOKEN')

    def get_items(self):
        url = f'{self.base_url}{self.item}'
        params = {
            'per_page': self.per_page,
            'page_no': self.page_number
        }
        items = []
        while self.has_more:
            pprint(self.headers)
            api_req = requests.get(
                url=url,
                headers=self.headers,
                params=params
            )
            pprint(api_req.text)
            try:
                api_req_json = api_req.json()
            except:
                self.logger.error(f'ERROR GETTING ITEMS: {api_req.text}')
                self.has_more = False
                return items
            
            items.extend(api_req_json[self.item])

            if len(items) == api_req_json['pagination']['total']:
                self.has_more = False
            else:
                params['page_no'] = api_req_json['pagination']['page_no'] + 1

        return items
