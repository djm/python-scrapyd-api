import pytest
from mock import MagicMock

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
    Test that auth details get correctly passed to the client when
    no client is provided.
    """
    api = ScrapydAPI(HOST_URL, auth=AUTH)
    assert api.client.auth == AUTH


def test_auth_doesnt_get_applied_when_client_is_supplied():
    """
    Test that auth details do not get set on a passed client. Instantiated
    clients should handle authentication themselves.
    """
    mock_client = MagicMock()
    api = ScrapydAPI(HOST_URL, auth=AUTH, client=mock_client)
    assert api.client.auth != AUTH


def test_build_url_with_default_endpoints():
    """
    Test that the absolute URL constructor correctly forms URL when
    the ScrapydAPI is relying on the default endpoints.
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
    Test that the absolute URL constructor correctly forms URL when
    the ScrapydAPI had custom endpoints passed in.
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
    Test that supplying _build_url with an endpoint that does not
    exist in the endpoints dictionary results in a ValueError.
    """
    api = ScrapydAPI(HOST_URL)
    with pytest.raises(ValueError):
        api._build_url('does-not-exist')


def test_add_version():
    """
    Test the method which handles adding a new version of a project.
    """
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
        }
    )


def test_cancel():
    """
    Test the method which handles cancelling a spider job.
    """
    mock_client = MagicMock()
    mock_client.post.return_value = {
        'prevstate': 'running',
    }
    api = ScrapydAPI(HOST_URL, client=mock_client)
    rtn = api.cancel(PROJECT, JOB)
    assert rtn is True
    mock_client.post.assert_called_with(
        'http://localhost/cancel.json',
        data={
            'project': PROJECT,
            'job': JOB
        }
    )


def test_delete_project():
    """
    Test the method which handles deleting a project.
    """
    mock_client = MagicMock()
    mock_client.post.return_value = {}
    api = ScrapydAPI(HOST_URL, client=mock_client)
    rtn = api.delete_project(PROJECT)
    assert rtn is True
    mock_client.post.assert_called_with(
        'http://localhost/delproject.json',
        data={
            'project': PROJECT,
        }
    )


def test_delete_version():
    """
    Test the method which handles deleting a version of a project.
    """
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
        }
    )


def test_job_status():
    """
    Test the method which handles retrieving the status of a given job.
    """
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
    """
    Test the method which handles listing jobs on the server.
    """
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
        }
    )


def test_list_projects():
    """
    Test the method which handles listing projects on the server.
    """
    mock_client = MagicMock()
    mock_client.get.return_value = {
        'projects': ['test', 'test2']
    }
    api = ScrapydAPI(HOST_URL, client=mock_client)
    rtn = api.list_projects()
    assert rtn == ['test', 'test2']
    mock_client.get.assert_called_with(
        'http://localhost/listprojects.json',
    )


def test_list_spiders():
    """
    Test the method which handles listing all spiders in a project.
    """
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
    )


def test_list_versions():
    """
    Test the method which handles listing all versions of a project.
    """
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
    )


def test_schedule():
    """
    Test the method which handles scheduling a new job.
    """
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
    assert len(kwargs) == 1
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
