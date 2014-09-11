import json

import responses
import pytest

from scrapyd_api.client import Client
from scrapyd_api.exceptions import ScrapydResponseError


SCRAPYD_RESPONSE_OK = {
    'status': 'ok',
    'example': 'Test',
    'another-example': 'Another Test',
}

SCRAPYD_RESPONSE_ERROR = {
    'status': 'error',
    'message': 'Test Error'
}

URL = 'http://localhost/'
AUTH = ('username', 'password')

OK_JSON = '{"status": "ok", "key": "value"}'
ERROR_JSON = '{"status": "error", "message": "some-error"}'
MALFORMED_JSON = 'this-aint-json'


@responses.activate
def test_get_handle_ok_response():
    """
    Test that a GET request uses the requests lib properly.
    """
    non_authed_client = Client()
    responses.add(responses.GET, URL, body=OK_JSON, status=200)
    non_authed_client.get(URL)
    assert len(responses.calls) == 1
    call = responses.calls[0]
    assert call.request.url == URL
    assert call.response.json() == json.loads(OK_JSON)
    # Test with some query string params.
    test_params = {'test': 'params'}
    url_with_query = URL + '?test=params'
    responses.add(responses.GET, url_with_query, body=OK_JSON, status=200)
    non_authed_client.get(URL, params=test_params)
    assert len(responses.calls) == 2
    call = responses.calls[1]
    assert call.response.json() == json.loads(OK_JSON)


@responses.activate
def test_post_handle_ok_response():
    """
    Test that a POST request uses the requests lib properly.
    """
    non_authed_client = Client()
    responses.add(responses.POST, URL, body=OK_JSON, status=200)
    test_data = {'test': 'json'}
    non_authed_client.post(URL, data=test_data)
    assert len(responses.calls) == 1
    call = responses.calls[0]
    assert call.response.json() == json.loads(OK_JSON)


@responses.activate
def test_handle_http_error_response():
    """
    Test that an 'Error' response from Scrapyd handles as desired.
    """
    non_authed_client = Client()
    responses.add(responses.GET, URL, body=MALFORMED_JSON, status=500)
    with pytest.raises(ScrapydResponseError) as excinfo:
        non_authed_client.get(URL)
    assert '500 error' in str(excinfo.value)


@responses.activate
def test_non_or_invalid_json_response_errors():
    """
    Test that a response from Scrapyd that does not parse as
    valid JSON raises the correct exception.
    """
    non_authed_client = Client()
    responses.add(responses.GET, URL, body=MALFORMED_JSON, status=200)
    with pytest.raises(ScrapydResponseError) as excinfo:
        non_authed_client.get(URL)
    assert 'invalid JSON' in str(excinfo.value)


@responses.activate
def test_scrapyd_error_response():
    """
    Test that a response from Scrapyd that does not parse as
    valid JSON raises the correct exception.
    """
    non_authed_client = Client()
    responses.add(responses.GET, URL, body=ERROR_JSON, status=200)
    with pytest.raises(ScrapydResponseError) as excinfo:
        non_authed_client.get(URL)
    assert 'some-error' in str(excinfo.value)


@responses.activate
def test_with_auth():
    """
    Test attaching basic auth creds results in correct headers.
    """
    authed_client = Client()
    authed_client.auth = AUTH
    # Test with just a URL call.
    responses.add(responses.GET, URL, body=OK_JSON, status=200)
    authed_client.get(URL)
    assert len(responses.calls) == 1
    call = responses.calls[0]
    assert 'Authorization' in call.request.headers
    assert 'Basic' in call.request.headers['Authorization']
