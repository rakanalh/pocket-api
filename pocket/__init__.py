import sys
import requests


class Pocket:
    """
    A wrapper around GetPocket.com API V3.
    It provides methods that wrap all endpoints provided
    by getpocket.com and adds easy chainable bulk modification support.
    """
    api_url = 'https://getpocket.com/v3'

    auth_error_codes = [
        136, 138, 152,
        182, 185, 158,
        159
    ]

    def __init__(self, consumer_key, access_token=None):
        self._consumer_key = consumer_key
        self._access_token = access_token

        # Init list for bulk action storage
        self._bulk_actions = []

    def add(self, url, title=None, tags=None, tweet_id=None):
        """
        Add a URL to pocket
        See: https://getpocket.com/developer/docs/v3/add
        :param url: The url to add
        :param title: given title
        :param tags: A list of tags
        :param tweet_id: for tweet attribution
        :return: A dictionary containing the response result
        :rtype: dict
        """
        return self._make_request('add')

    def retrieve(self, state=None, favorite=None, tag=None, contentType=None,
                 sort=None, detailType=None, search=None, domain=None,
                 since=None, count=None, offset=None):
        """
        Retrieve the list of your articles
        See: https://getpocket.com/developer/docs/v3/retrieve
        :param state: filter by state
        :param favorite: only fetch favorite
        :param tag: filter by tag or _untagged_
        :param contentType: get article, video or image
        :param sort: sort by provided value
        :param detailType: defines the response details to return
        :param search: search term
        :param domain: search domain
        :param since: search modified since unix timestamp
        :param count: the number of required items
        :param offset: the position to start results from
        :return: A dictionary containing the response result
        :rtype: dict
        """
        return self._make_request('get')

    def bulk_add(self, item_id, ref_id=None, tags=None,
                 time=None, title=None, url=None):
        """
        Add an item to list
        See: https://getpocket.com/developer/docs/v3/modify
        :param item_id: int
        :param ref_id: tweet_id
        :param tags: list of tags
        :param time: time of action
        :param title: given title
        :param url: item url
        :return: self for chaining
        :rtype: Pocket
        """
        self._add_action('add')
        return self

    def archive(self, item_id, time=None):
        """
        Archive item
        See: https://getpocket.com/developer/docs/v3/modify
        :param item_id: int
        :param time: time of action
        :return: self for chaining
        :rtype: Pocket
        """
        self._add_action('archive')
        return self

    def readd(self, item_id, time=None):
        """
        Re-add item
        See: https://getpocket.com/developer/docs/v3/modify
        :param item_id: int
        :param time: time of action
        :return: self for chaining
        :rtype: Pocket
        """
        self._add_action('readd')
        return self

    def favorite(self, item_id, time=None):
        """
        Favorite item
        See: https://getpocket.com/developer/docs/v3/modify
        :param item_id: int
        :param time: time of action
        :return: self for chaining
        :rtype: Pocket
        """
        self._add_action('favorite')
        return self

    def unfavorite(self, item_id, time=None):
        """
        Unfavorite item
        See: https://getpocket.com/developer/docs/v3/modify
        :param item_id: int
        :param time: time of action
        :return: self for chaining
        :rtype: Pocket
        """
        self._add_action('unfavorite')
        return self

    def delete(self, item_id, time=None):
        """
        Delete item
        See: https://getpocket.com/developer/docs/v3/modify
        :param item_id: int
        :param time: time of action
        :return: self for chaining
        :rtype: Pocket
        """
        self._add_action('delete')
        return self

    def tags_add(self, item_id, tags, time=None):
        """
        Add tags to item
        See: https://getpocket.com/developer/docs/v3/modify
        :param item_id: int
        :param tags: list of tags
        :param time: time of action
        :return: self for chaining
        :rtype: Pocket
        """
        self._add_action('tags_add')
        return self

    def tags_remove(self, item_id, tags, time=None):
        """
        Remove tags in item
        See: https://getpocket.com/developer/docs/v3/modify
        :param item_id: int
        :param tags: list of tags
        :param time: time of action
        :return: self for chaining
        :rtype: Pocket
        """
        self._add_action('tags_remove')
        return self

    def tags_replace(self, item_id, tags, time=None):
        """
        Replace tags in item
        See: https://getpocket.com/developer/docs/v3/modify
        :param item_id: int
        :param tags: list of tags
        :param time: time of action
        :return: self for chaining
        :rtype: Pocket
        """
        self._add_action('tags_replace')
        return self

    def tags_clear(self, item_id, time=None):
        """
        Clear tags in item
        See: https://getpocket.com/developer/docs/v3/modify
        :param item_id: int
        :param time: time of action
        :return: self for chaining
        :rtype: Pocket
        """
        self._add_action('tags_clear')
        return self

    def tag_rename(self, old_tag, new_tag, time=None):
        """
        Rename a tag
        See: https://getpocket.com/developer/docs/v3/modify
        :param old_tag: old tag name
        :param new_tag: new tag name
        :param time: time of action
        :return: self for chaining
        :rtype: Pocket
        """
        self._add_action('tag_rename')
        return self

    def reset(self):
        """
        Empty bulk operations
        """
        self._bulk_actions = []

    def commit(self):
        """
        Dispatch bulk operations
        :return: A dict containing the request result
        :rtype: dict
        """
        if not self._bulk_actions:
            return

        return self._make_request(self._bulk_actions)

    def get_request_token(self, redirect_url):
        response = requests.post(
            self._get_url('oauth/request'),
            json={
                'consumer_key': self._consumer_key,
                'redirect_uri': redirect_url
            },
            headers=self._get_headers()
        )
        if response.status_code == requests.codes.ok:
            return response.json()['code']
        return None

    def get_user_profile(self, request_token):
        response = requests.post(
            self._get_url('oauth/authorize'),
            json={
                'consumer_key': self._consumer_key,
                'code': request_token
            },
            headers=self._get_headers()
        )
        if response.status_code == requests.codes.ok:
            return response.json()
        return None

    def get_access_token(self, request_token):
        user_profile = self.get_user_profile(request_token)
        if not user_profile:
            return
        return user_profile['access_token']

    def _add_action(self, action):
        """
        Register an action into bulk
        :param action: action name
        """
        kwargs = self._get_method_params()

        kwargs['action'] = action

        self._bulk_actions.append(kwargs)

    def _make_request(self, action):
        """
        Perform the request
        :param action: action name
        :return: a dict containing the request result
        :rtype: dict
        """
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
        """
        This method makes reading and filtering each method implemented
        in this class a more general approach. It reads the previous
        frame from Python and filters the params passed to the caller
        of _make_request.
        :return: a dictionary of caller's parameters and values
        :rtype: dict
        """
        caller = sys._getframe(2)
        var_names = list(caller.f_code.co_varnames)
        caller_locals = caller.f_locals

        var_names.remove('self')
        kwargs = {key: value for key, value in caller_locals.items()
                  if key in var_names and value is not None}
        return kwargs

    def _get_url(self, uri):
        """
        Construct the request URL
        :param uri: the required URI
        :return: The full URL
        :rtype: str
        """
        return '{}/{}'.format(Pocket.api_url, uri)

    def _get_headers(self):
        """
        Construct request headers
        :return: A dictionary of headers
        :rtype: dict
        """
        return {
            'Content-Type': 'application/json',
            'X-Accept': 'application/json',
        }

    def _make_exception(self, response):
        """
        In case of exception, construct the exception
        object that holds all important values returned by
        the response.
        :return: The exception instance
        :rtype: PocketException
        """
        headers = response.headers

        limit_headers = []
        if 'X-Limit-User-Limit' in headers:
            limit_headers = [
                headers['X-Limit-User-Limit'],
                headers['X-Limit-User-Remaining'],
                headers['X-Limit-User-Reset'],
                headers['X-Limit-Key-Limit'],
                headers['X-Limit-Key-Remaining'],
                headers['X-Limit-Key-Reset']
            ]

        x_error_code = int(headers['X-Error-Code'])
        exc = PocketException
        if x_error_code in self.auth_error_codes:
            exc = PocketAutException

        return exc(
            response.status_code,
            x_error_code,
            headers['X-Error'],
            *limit_headers
        )


class PocketException(Exception):
    """
    A class that holds all information that could be retrieved
    from the HTTP response.
    """
    def __init__(self, http_code, error_code, message, user_limit=None,
                 user_remaining=None, user_reset=None,
                 key_limit=None, key_remaining=None, key_reset=None):
        for var_name, value in locals().items():
            if var_name == 'self':
                continue
            setattr(self, var_name, value)


class PocketAutException(PocketException):
    """
    A class that defines errors in authenticating against Pocket
    """
    pass
