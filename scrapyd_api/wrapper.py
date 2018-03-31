from __future__ import unicode_literals

from copy import deepcopy

from . import constants
from .client import Client
from .compat import (
    iteritems,
    urljoin
)


class ScrapydAPI(object):
    """
    Provides a thin Pythonic wrapper around the Scrapyd API. The public methods
    come in two types: first class, those that wrap a Scrapyd API endpoint
    directly; and derived, those that use a one or more Scrapyd API endpoint(s)
    to provide functionality that is unique to this wrapper.
    """

    def __init__(self, target='http://localhost:6800', auth=None,
                 endpoints=None, client=None, timeout=None):
        """
        Instantiates the ScrapydAPI wrapper for use.

        Args:
          target (str): the hostname/port to hit with requests.
          auth (str, str): a 2-item tuple containing user/pass details. Only
                           used when `client` is not passed.
          endpoints: a dictionary of custom endpoints to apply on top of
                     the pre-existing defaults.
          client: a pre-instantiated requests-like client. By default, we use
                  our own client. Override for your own needs.
          timeout: timeout for client requests in seconds, either as a float
                   or a (connect timeout, read timeout) tuple

        """
        if endpoints is None:
            endpoints = {}

        if client is None:
            client = Client()
            client.auth = auth

        self.target = target
        self.client = client
        self.timeout = timeout
        self.endpoints = deepcopy(constants.DEFAULT_ENDPOINTS)
        self.endpoints.update(endpoints)

    def _build_url(self, endpoint):
        """
        Builds the absolute URL using the target and desired endpoint.
        """
        try:
            path = self.endpoints[endpoint]
        except KeyError:
            msg = 'Unknown endpoint `{0}`'
            raise ValueError(msg.format(endpoint))
        absolute_url = urljoin(self.target, path)
        return absolute_url

    def add_version(self, project, version, egg):
        """
        Adds a new project egg to the Scrapyd service. First class, maps to
        Scrapyd's add version endpoint.
        """
        url = self._build_url(constants.ADD_VERSION_ENDPOINT)
        data = {
            'project': project,
            'version': version
        }
        files = {
            'egg': egg
        }
        json = self.client.post(url, data=data, files=files,
                                timeout=self.timeout)
        return json['spiders']

    def cancel(self, project, job, signal=None):
        """
        Cancels a job from a specific project. First class, maps to
        Scrapyd's cancel job endpoint.
        """
        url = self._build_url(constants.CANCEL_ENDPOINT)
        data = {
            'project': project,
            'job': job,
        }
        if signal is not None:
            data['signal'] = signal
        json = self.client.post(url, data=data, timeout=self.timeout)
        return json['prevstate']

    def delete_project(self, project):
        """
        Deletes all versions of a project. First class, maps to Scrapyd's
        delete project endpoint.
        """
        url = self._build_url(constants.DELETE_PROJECT_ENDPOINT)
        data = {
            'project': project,
        }
        self.client.post(url, data=data, timeout=self.timeout)
        return True

    def delete_version(self, project, version):
        """
        Deletes a specific version of a project. First class, maps to
        Scrapyd's delete version endpoint.
        """
        url = self._build_url(constants.DELETE_VERSION_ENDPOINT)
        data = {
            'project': project,
            'version': version
        }
        self.client.post(url, data=data, timeout=self.timeout)
        return True

    def job_status(self, project, job_id):
        """
        Retrieves the 'status' of a specific job specified by its id. Derived,
        utilises Scrapyd's list jobs endpoint to provide the answer.
        """
        all_jobs = self.list_jobs(project)
        for state in constants.JOB_STATES:
            job_ids = [job['id'] for job in all_jobs[state]]
            if job_id in job_ids:
                return state
        return ''  # Job not found, state unknown.

    def list_jobs(self, project):
        """
        Lists all known jobs for a project. First class, maps to Scrapyd's
        list jobs endpoint.
        """
        url = self._build_url(constants.LIST_JOBS_ENDPOINT)
        params = {'project': project}
        jobs = self.client.get(url, params=params, timeout=self.timeout)
        return jobs

    def list_projects(self):
        """
        Lists all deployed projects. First class, maps to Scrapyd's
        list projects endpoint.
        """
        url = self._build_url(constants.LIST_PROJECTS_ENDPOINT)
        json = self.client.get(url, timeout=self.timeout)
        return json['projects']

    def list_spiders(self, project):
        """
        Lists all known spiders for a specific project. First class, maps
        to Scrapyd's list spiders endpoint.
        """
        url = self._build_url(constants.LIST_SPIDERS_ENDPOINT)
        params = {'project': project}
        json = self.client.get(url, params=params, timeout=self.timeout)
        return json['spiders']

    def list_versions(self, project):
        """
        Lists all deployed versions of a specific project. First class, maps
        to Scrapyd's list versions endpoint.
        """
        url = self._build_url(constants.LIST_VERSIONS_ENDPOINT)
        params = {'project': project}
        json = self.client.get(url, params=params, timeout=self.timeout)
        return json['versions']

    def schedule(self, project, spider, settings=None, **kwargs):
        """
        Schedules a spider from a specific project to run. First class, maps
        to Scrapyd's scheduling endpoint.
        """

        url = self._build_url(constants.SCHEDULE_ENDPOINT)
        data = {
            'project': project,
            'spider': spider
        }
        data.update(kwargs)
        if settings:
            setting_params = []
            for setting_name, value in iteritems(settings):
                setting_params.append('{0}={1}'.format(setting_name, value))
            data['setting'] = setting_params
        json = self.client.post(url, data=data, timeout=self.timeout)
        return json['jobid']
