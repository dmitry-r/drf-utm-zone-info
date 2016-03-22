import logging

import requests

logger = logging.getLogger(__name__)

HTTPError = requests.HTTPError


class RESTApiJWTClient:
    """
    REST Client Base Class With JWT enabled authentication

    Can be either extended through inheritance or created using the params `service_base` and `login_url`

    :param service_base: the base url
    :param login_url: the relative path to the login url
    """

    service_base = 'http://localhost/api/'
    login_url = '/jwt-auth/'

    def __init__(self, service_base=None, login_url=None):
        if service_base:
            self.service_base = service_base
        if login_url:
            self.login_url = login_url
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
        }
        self.client = requests.session()
        self.token = None

    def get(self, url, params=None, **kwargs):
        response = requests.get(self._to_fully_qualified_url(url), params=params, **self._data_dict(**kwargs))
        raise_for_status(response)
        return response

    def post(self, url, json_data=None, **kwargs):
        response = requests.post(self._to_fully_qualified_url(url), json=json_data, **self._data_dict(**kwargs))
        raise_for_status(response)
        return response

    def auth(self, username, password):
        login_url = self._to_fully_qualified_url(self.login_url)
        login_data = dict(username=username, password=password, next=self.service_base)
        response = self.post(login_url, json_data=login_data, headers=dict(Referer=login_url))
        self.token = response.json().get('token')
        return response

    def authorized_get(self, url, params=None, **kwargs):
        self._make_request_authorized()
        return self.get(url, params, **kwargs)

    def authorized_post(self, url, json_data=None, **kwargs):
        self._make_request_authorized()
        return self.post(url, json_data, **kwargs)

    def _data_dict(self, **kwargs):
        headers = self.headers.copy()
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))
        return dict(headers=headers, **kwargs)

    def _is_colliding_slashes(self, url):
        return self.service_base.endswith('/') and url.startswith('/')

    def _to_fully_qualified_url(self, url):
        if url.startswith('http'):
            return url
        base_url = self.service_base[:-1] if (self._is_colliding_slashes(url)) else self.service_base
        return base_url + url

    def _make_request_authorized(self):
        if not self.token:
            raise Exception('Unauthorized request. Assure you call `auth()` before making a request.')
        # TODO: comply to jwt and check if key is valid, if it needs reinitialization etc
        self.headers['Authorization'] = 'JWT {token}'.format(token=self.token)


def raise_for_status(response):
    response.raise_for_status()


def errors(http_error):
    return http_error.response.json()
