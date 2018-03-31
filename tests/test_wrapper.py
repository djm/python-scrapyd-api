import pytest
from mock import MagicMock
from requests import Timeout

from scrapyd_api.compat import StringIO
from scrapyd_api.constants import (
    ADD_VERSION_ENDPOINT,
    CANCEL_ENDPOINT,
    FINISHED,
    PENDING
)
from scrapyd_api.wrapper import ScrapydAPI

HOST_URL = 'http://localhost'
AUTH = ('username', 'password')
PROJECT = 'project'
VERSION = '45'
SPIDER = 'spider'
JOB = 'd131dd02c5e6eec4693d9a0698aff95c'


def test_auth_gets_applied_when_client_is_not_supplied():
    """
    Auth details should get correctly passed to the client
    when no client is provided.
    """
    api = ScrapydAPI(HOST_URL, auth=AUTH)
    assert api.client.auth == AUTH


def test_auth_doesnt_get_applied_when_client_is_supplied():
    """
    Auth details should not get set on a passed client.
    Instantiated clients should handle auth themselves.
    """
    mock_client = MagicMock()
    api = ScrapydAPI(HOST_URL, auth=AUTH, client=mock_client)
    assert api.client.auth != AUTH


def test_build_url_with_default_endpoints():
    """
    Absolute URL constructor should form correct URL when
    the client is relying on the default endpoints.
    """
    api = ScrapydAPI('http://localhost')
    url = api._build_url(ADD_VERSION_ENDPOINT)
    assert url == 'http://localhost/addversion.json'
    # Test trailing slash on target.
    api = ScrapydAPI('http://localhost/')
    url = api._build_url(ADD_VERSION_ENDPOINT)
    assert url == 'http://localhost/addversion.json'


def test_build_url_with_custom_endpoints():
    """
    The absolute URL constructor should correctly form URL when
    the client has custom endpoints passed in.
    """
    custom_endpoints = {
        ADD_VERSION_ENDPOINT: '/addversion-custom.json'
    }
    api = ScrapydAPI('http://localhost', endpoints=custom_endpoints)
    url = api._build_url(ADD_VERSION_ENDPOINT)
    assert url == 'http://localhost/addversion-custom.json'
    # Test trailing slash on target.
    api = ScrapydAPI('http://localhost/', endpoints=custom_endpoints)
    url = api._build_url(ADD_VERSION_ENDPOINT)
    assert url == 'http://localhost/addversion-custom.json'
    # Test that endpoints that were not overridden by the custom_endpoints
    # still work as the defaults.
    url = api._build_url(CANCEL_ENDPOINT)
    assert url == 'http://localhost/cancel.json'


def test_build_url_with_non_existant_endpoint_errors():
    """
    Supplying _build_url with an endpoint that does not exist in
    the endpoints dictionary should result in a ValueError.
    """
    api = ScrapydAPI(HOST_URL)
    with pytest.raises(ValueError):
        api._build_url('does-not-exist')


def test_add_version():
    mock_client = MagicMock()
    mock_client.post.return_value = {
        'spiders': 3
    }
    api = ScrapydAPI(HOST_URL, client=mock_client)
    test_egg = StringIO('Test egg')
    rtn = api.add_version(PROJECT, VERSION, test_egg)
    assert rtn == 3  # The number of spiders uploaded.
    mock_client.post.assert_called_with(
        'http://localhost/addversion.json',
        data={
            'project': PROJECT,
            'version': VERSION
        },
        files={
            'egg': test_egg
        },
        timeout=None
    )


def test_cancelling_running_job():
    mock_client = MagicMock()
    mock_client.post.return_value = {
        'prevstate': 'running',
    }
    api = ScrapydAPI(HOST_URL, client=mock_client)
    rtn = api.cancel(PROJECT, JOB)
    assert rtn is 'running'
    mock_client.post.assert_called_with(
        'http://localhost/cancel.json',
        data={
            'project': PROJECT,
            'job': JOB
        },
        timeout=None
    )


def test_cancelling_pending_job():
    mock_client = MagicMock()
    mock_client.post.return_value = {
        'prevstate': 'pending',
    }
    api = ScrapydAPI(HOST_URL, client=mock_client)
    rtn = api.cancel(PROJECT, JOB)
    assert rtn is 'pending'
    mock_client.post.assert_called_with(
        'http://localhost/cancel.json',
        data={
            'project': PROJECT,
            'job': JOB
        },
        timeout=None
    )


def test_cancelling_with_specific_signal():
    mock_client = MagicMock()
    mock_client.post.return_value = {
        'prevstate': 'running',
    }
    api = ScrapydAPI(HOST_URL, client=mock_client)
    rtn = api.cancel(PROJECT, JOB, signal='TERM')
    assert rtn is 'running'
    mock_client.post.assert_called_with(
        'http://localhost/cancel.json',
        data={
            'project': PROJECT,
            'job': JOB,
            'signal': 'TERM'
        },
        timeout=None
    )


def test_delete_project():
    mock_client = MagicMock()
    mock_client.post.return_value = {}
    api = ScrapydAPI(HOST_URL, client=mock_client)
    rtn = api.delete_project(PROJECT)
    assert rtn is True
    mock_client.post.assert_called_with(
        'http://localhost/delproject.json',
        data={
            'project': PROJECT,
        },
        timeout=None
    )


def test_delete_version():
    mock_client = MagicMock()
    mock_client.post.return_value = {}
    api = ScrapydAPI(HOST_URL, client=mock_client)
    rtn = api.delete_version(PROJECT, VERSION)
    assert rtn is True
    mock_client.post.assert_called_with(
        'http://localhost/delversion.json',
        data={
            'project': PROJECT,
            'version': VERSION
        },
        timeout=None
    )


def test_job_status():
    mock_client = MagicMock()
    mock_client.get.return_value = {
        'pending': [{'id': 'abc'}, {'id': 'def'}],
        'running': [],
        'finished': [{'id': 'ghi'}],
    }
    api = ScrapydAPI(HOST_URL, client=mock_client)
    expected_results = (
        ('abc', PENDING),
        ('def', PENDING),
        ('ghi', FINISHED),
        ('xyz', '')
    )
    for job_id, expected_result in expected_results:
        rtn = api.job_status(PROJECT, job_id)
        assert rtn == expected_result


def test_list_jobs():
    mock_client = MagicMock()
    mock_client.get.return_value = {
        'pending': [{'id': 'abc'}, {'id': 'def'}],
        'running': [],
        'finished': [{'id': 'ghi'}],
    }
    api = ScrapydAPI(HOST_URL, client=mock_client)
    rtn = api.list_jobs(PROJECT)
    assert len(rtn) == 3
    assert sorted(rtn.keys()) == ['finished', 'pending', 'running']
    assert rtn['pending'] == [{'id': 'abc'}, {'id': 'def'}]
    assert rtn['finished'] == [{'id': 'ghi'}]
    assert rtn['running'] == []
    mock_client.get.assert_called_with(
        'http://localhost/listjobs.json',
        params={
            'project': PROJECT,
        },
        timeout=None
    )


def test_list_projects():
    mock_client = MagicMock()
    mock_client.get.return_value = {
        'projects': ['test', 'test2']
    }
    api = ScrapydAPI(HOST_URL, client=mock_client)
    rtn = api.list_projects()
    assert rtn == ['test', 'test2']
    mock_client.get.assert_called_with(
        'http://localhost/listprojects.json',
        timeout=None
    )


def test_list_spiders():
    mock_client = MagicMock()
    mock_client.get.return_value = {
        'spiders': ['spider', 'spider2']
    }
    api = ScrapydAPI(HOST_URL, client=mock_client)
    rtn = api.list_spiders(PROJECT)

    assert rtn == ['spider', 'spider2']
    mock_client.get.assert_called_with(
        'http://localhost/listspiders.json',
        params={
            'project': PROJECT,
        },
        timeout=None
    )


def test_list_versions():
    mock_client = MagicMock()
    mock_client.get.return_value = {
        'versions': ['version', 'version2']
    }
    api = ScrapydAPI(HOST_URL, client=mock_client)
    rtn = api.list_versions(PROJECT)
    assert rtn == ['version', 'version2']
    mock_client.get.assert_called_with(
        'http://localhost/listversions.json',
        params={
            'project': PROJECT,
        },
        timeout=None
    )


def test_schedule():
    mock_client = MagicMock()
    job_id = 'ce54b67080280d1ec69821bcb6a88393'
    settings = {
        'BOT_NAME': 'Firefox',
        'DOWNLOAD_DELAY': 2
    }
    kwargs = {'extra_detail': 'Test'}
    mock_client.post.return_value = {
        'jobid': job_id
    }
    api = ScrapydAPI(HOST_URL, client=mock_client)
    rtn = api.schedule(PROJECT, SPIDER, settings=settings, **kwargs)
    assert rtn == job_id
    args, kwargs = mock_client.post.call_args
    assert len(args) == 1
    assert args[0] == 'http://localhost/schedule.json'
    assert len(kwargs) == 2
    assert 'data' in kwargs
    data_kw = kwargs['data']
    assert 'project' in data_kw
    assert data_kw['project'] == PROJECT
    assert 'extra_detail' in data_kw
    assert data_kw['extra_detail'] == 'Test'
    assert 'setting' in data_kw
    assert sorted(data_kw['setting']) == ['BOT_NAME=Firefox',
                                          'DOWNLOAD_DELAY=2']
    assert 'spider' in data_kw
    assert data_kw['spider'] == SPIDER


def test_request_timeout():
    """
    The client should raise an exception when the server does not respond
    in time limit.
    """
    api = ScrapydAPI('http://httpbin.org/delay/5', timeout=1)
    with pytest.raises(Timeout):
        api.client.get(api.target, timeout=api.timeout)
