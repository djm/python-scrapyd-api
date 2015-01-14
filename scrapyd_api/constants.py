from __future__ import unicode_literals

ADD_VERSION_ENDPOINT = 'add_version'
CANCEL_ENDPOINT = 'cancel'
DELETE_PROJECT_ENDPOINT = 'delete_project'
DELETE_VERSION_ENDPOINT = 'delete_version'
LIST_JOBS_ENDPOINT = 'list_jobs'
LIST_PROJECTS_ENDPOINT = 'list_projects'
LIST_SPIDERS_ENDPOINT = 'list_spiders'
LIST_VERSIONS_ENDPOINT = 'list_versions'
SCHEDULE_ENDPOINT = 'schedule'

DEFAULT_ENDPOINTS = {
    ADD_VERSION_ENDPOINT: '/addversion.json',
    CANCEL_ENDPOINT: '/cancel.json',
    DELETE_PROJECT_ENDPOINT: '/delproject.json',
    DELETE_VERSION_ENDPOINT: '/delversion.json',
    LIST_JOBS_ENDPOINT: '/listjobs.json',
    LIST_PROJECTS_ENDPOINT: '/listprojects.json',
    LIST_SPIDERS_ENDPOINT: '/listspiders.json',
    LIST_VERSIONS_ENDPOINT: '/listversions.json',
    SCHEDULE_ENDPOINT: '/schedule.json',
}

FINISHED = 'finished'
PENDING = 'pending'
RUNNING = 'running'

JOB_STATES = [FINISHED, PENDING, RUNNING]
