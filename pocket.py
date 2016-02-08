import requests


class Pocket:
    api_url = 'https://getpocket.com/v3'

    def __init__(self, consumer_key, access_token):
        self._consumer_key = consumer_key
        self._access_token = access_token

    def retrieve(self, state=None, favorite=None, tag=None, content_type=None,
                 sort=None, detailType=None, search=None, domain=None,
                 since=None, count=None, offset=None):
        # This is ugly!
        vars = locals()
        del vars['self']
        return self._make_request('get', **vars)

    def _make_request(self, action, **kwargs):
        kwargs.update({
            'consumer_key': self._consumer_key,
            'access_token': self._access_token
        })

        response = requests.post(
            self._get_url('get'),
            json=kwargs,
            headers=self._get_headers()
        )

        if response.status_code != requests.codes.ok:
            raise self._make_exception(response)

        return response.json()

    def _get_url(self, uri):
        return '{}/{}'.format(Pocket.api_url, uri)

    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'X-Accept': 'application/json',
        }

    def _make_exception(self, response):
        headers = response.headers

        return PocketException(
            headers['X-Error-Code'],
            headers['X-Error'],
            headers['X-Limit-User-Limit'],
            headers['X-Limit-User-Remaining'],
            headers['X-Limit-User-Reset'],
            headers['X-Limit-Key-Limit'],
            headers['X-Limit-Key-Remaining'],
            headers['X-Limit-Key-Reset']
        )


class PocketException(Exception):
    def __init__(self, code, message, user_limit=None,
                 user_remaining=None, user_reset=None,
                 key_limit=None, key_remaining=None, key_reset=None):
        for var_name, value in locals().items():
            if var_name == 'self':
                continue
            setattr(self, var_name, value)
