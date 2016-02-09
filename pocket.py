import sys
import requests


class Pocket:
    api_url = 'https://getpocket.com/v3'

    def __init__(self, consumer_key, access_token):
        self._consumer_key = consumer_key
        self._access_token = access_token

        self._bulk_actions = []

    def add(self, url, title=None, tags=None, tweet_id=None):
        return self._make_request('add')

    def retrieve(self, state=None, favorite=None, tag=None, contentType=None,
                 sort=None, detailType=None, search=None, domain=None,
                 since=None, count=None, offset=None):
        return self._make_request('get')

    def bulk_commit(self):
        pass

    def bulk_add(self, item_id, ref_id=None, tags=None,
                 time=None, title=None, url=None):
        self._add_action('add')
        return self

    def archive(self, item_id, time=None):
        self._add_action('archive')
        return self

    def readd(self, item_id, time=None):
        self._add_action('readd')
        return self

    def favorite(self, item_id, time=None):
        self._add_action('favorite')
        return self

    def unfavorite(self, item_id, time=None):
        self._add_action('unfavorite')
        return self

    def delete(self, item_id, time=None):
        self._add_action('delete')
        return self

    def tags_add(self, item_id, tags, time=None):
        self._add_action('tags_add')
        return self

    def tags_remove(self, item_id, tags, time=None):
        self._add_action('tags_remove')
        return self

    def tags_replace(self, item_id, tags, time=None):
        self._add_action('tags_replace')
        return self

    def tags_clear(self, item_id, time=None):
        self._add_action('tags_clear')
        return self

    def tag_rename(self, old_tag, new_tag, time=None):
        self._add_action('tag_rename')
        return self

    def reset(self):
        self._bulk_actions = []

    def commit(self):
        self._make_request(self._bulk_actions)

    def _add_action(self, action):
        kwargs = self._get_method_params()

        kwargs['action'] = action

        self._bulk_actions.append(kwargs)

    def _make_request(self, action):
        if isinstance(action, list):
            kwargs = {'actions': action}
            action = 'send'
        else:
            kwargs = self._get_method_params()

        kwargs.update({
            'consumer_key': self._consumer_key,
            'access_token': self._access_token
        })

        response = requests.post(
            self._get_url(action),
            json=kwargs,
            headers=self._get_headers()
        )

        if response.status_code != requests.codes.ok:
            raise self._make_exception(response)

        return response.json()

    def _get_method_params(self):
        caller = sys._getframe(2)
        var_names = list(caller.f_code.co_varnames)
        caller_locals = caller.f_locals

        var_names.remove('self')
        kwargs = {key: value for key, value in caller_locals.items()
                  if key in var_names and value is not None}
        return kwargs

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
            response.status_code,
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
    def __init__(self, http_code, error_code, message, user_limit=None,
                 user_remaining=None, user_reset=None,
                 key_limit=None, key_remaining=None, key_reset=None):
        for var_name, value in locals().items():
            if var_name == 'self':
                continue
            setattr(self, var_name, value)
