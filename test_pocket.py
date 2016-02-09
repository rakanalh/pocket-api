import responses
import pytest
from pocket import Pocket, PocketException


_consumer_key = 'test_consumer_key'
_access_token = 'test_access_token'
_pocket = None


def setup_function(function):
    global _pocket
    _pocket = Pocket(_consumer_key, _access_token)

def success_request_callback(request):
    return 200, {}, request.body

def failed_request_callback(request):
    return 400, {
        'X-Error-Code': '111',
        'X-Error': 'Failed request',
        'X-Limit-User-Limit': '500',
        'X-Limit-User-Remaining': '0',
        'X-Limit-User-Reset': '5000',
        'X-Limit-Key-Limit': '1000',
        'X-Limit-Key-Remaining': '500',
        'X-Limit-Key-Reset': '1000'
    }, request.body

def has_credentials(response):
    assert response['consumer_key'] == _consumer_key
    assert response['access_token'] == _access_token


@responses.activate
def test_retrieve():
    responses.add_callback(
        responses.POST, _pocket._get_url('get'),
        callback=success_request_callback,
        content_type='application/json',
    )

    response = _pocket.retrieve(count=10, offset=20)

    assert len(responses.calls) == 1
    has_credentials(response)

    assert response['count'] == 10
    assert response['offset'] == 20


@responses.activate
def test_add():
    responses.add_callback(
        responses.POST, _pocket._get_url('add'),
        callback=success_request_callback,
        content_type='application/json',
    )

    response = _pocket.add(url='test_url', tweet_id=5)
    assert len(responses.calls) == 1
    has_credentials(response)

    assert response['url'] == 'test_url'
    assert response['tweet_id'] == 5


@responses.activate
def test_empty_bulk():
    responses.add_callback(
        responses.POST, _pocket._get_url('send'),
        callback=success_request_callback,
        content_type='application/json',
    )

    _pocket.commit()
    assert len(responses.calls) == 0


@responses.activate
def test_add_bulk():
    responses.add_callback(
        responses.POST, _pocket._get_url('send'),
        callback=success_request_callback,
        content_type='application/json',
    )

    response = _pocket.bulk_add(123, url='test_url').commit()
    assert len(responses.calls) == 1
    assert response['actions'][0]['action'] == 'add'
    assert response['actions'][0]['item_id'] == 123
    assert response['actions'][0]['url'] == 'test_url'


@responses.activate
def test_reset():
    responses.add_callback(
        responses.POST, _pocket._get_url('send'),
        callback=success_request_callback,
        content_type='application/json',
    )

    _pocket.bulk_add(123, url='test_url').reset()
    assert len(responses.calls) == 0


@responses.activate
def test_archive_delete_readd():
    responses.add_callback(
        responses.POST, _pocket._get_url('send'),
        callback=success_request_callback,
        content_type='application/json',
    )

    response = _pocket.archive(123).delete(456).readd(789).commit()
    assert len(responses.calls) == 1
    assert response['actions'][0]['action'] == 'archive'
    assert response['actions'][0]['item_id'] == 123
    assert response['actions'][1]['action'] == 'delete'
    assert response['actions'][1]['item_id'] == 456
    assert response['actions'][2]['action'] == 'readd'
    assert response['actions'][2]['item_id'] == 789


@responses.activate
def test_favorite():
    responses.add_callback(
        responses.POST, _pocket._get_url('send'),
        callback=success_request_callback,
        content_type='application/json',
    )

    response = _pocket.favorite(123).unfavorite(123).commit()
    assert len(responses.calls) == 1
    assert response['actions'][0]['action'] == 'favorite'
    assert response['actions'][0]['item_id'] == 123
    assert response['actions'][1]['action'] == 'unfavorite'
    assert response['actions'][1]['item_id'] == 123

@responses.activate
def test_tags():
    responses.add_callback(
        responses.POST, _pocket._get_url('send'),
        callback=success_request_callback,
        content_type='application/json',
    )

    _pocket.tags_add(123, [1,2,3])
    _pocket.tags_remove(123, [2,3])
    _pocket.tags_replace(123, [4,5,6])
    _pocket.tag_rename('old_tag', 'new_tag')
    response = _pocket.commit()

    assert len(responses.calls) == 1
    assert response['actions'][0]['action'] == 'tags_add'
    assert response['actions'][0]['item_id'] == 123
    assert response['actions'][0]['tags'] == [1,2,3]
    assert response['actions'][1]['action'] == 'tags_remove'
    assert response['actions'][1]['item_id'] == 123
    assert response['actions'][1]['tags'] == [2,3]
    assert response['actions'][2]['action'] == 'tags_replace'
    assert response['actions'][2]['item_id'] == 123
    assert response['actions'][2]['tags'] == [4,5,6]
    assert response['actions'][3]['action'] == 'tag_rename'
    assert response['actions'][3]['old_tag'] == 'old_tag'
    assert response['actions'][3]['new_tag'] == 'new_tag'


@responses.activate
def test_failed_retrieve():
    responses.add_callback(
        responses.POST, _pocket._get_url('get'),
        callback=failed_request_callback,
        content_type='application/json',
    )

    with pytest.raises(PocketException):
        _pocket.retrieve()
