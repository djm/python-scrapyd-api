==================
python-scrapyd-api
==================

.. image:: https://badge.fury.io/py/python-scrapyd-api.png
    :target: http://badge.fury.io/py/python-scrapyd-api

.. image:: https://travis-ci.org/djm/python-scrapyd-api.png?branch=master
        :target: https://travis-ci.org/djm/python-scrapyd-api

.. image:: https://pypip.in/d/python-scrapyd-api/badge.png
        :target: https://pypi.python.org/pypi/python-scrapyd-api


A Python wrapper for working with Scrapyd_'s API_.

Allows a Python application to talk to, and therefore control, the Scrapy_
daemon Scrapyd_.

* Free software: BSD license.
* `Full documentation`_.
* On the `Python Package Index (PyPI)`_.
* Scrapyd's `API Documentation`_.

.. _Scrapy: http://scrapy.org/
.. _Scrapyd: https://github.com/scrapy/scrapyd
.. _API: http://scrapyd.readthedocs.org/en/latest/api.html
.. _Python Package Index (PyPI): https://pypi.python.org/pypi/python-scrapyd-api/
.. _Full documentation: http://python-scrapyd-api.rtfd.org
.. _API Documentation: http://scrapyd.readthedocs.org/en/latest/api.html

Install
-------

Easiest installation is via `pip`::

    pip install python-scrapyd-api

Quick Usage
-----------

Please refer to the full documentation_ for more detailed usage but to get you started:

.. code:: python

    >>> from scrapyd_api import ScrapydAPI
    >>> scrapyd = ScrapydAPI('http://localhost:6800')

.. _documentation: http://python-scrapyd-api.rtfd.org

**Add a project** egg as a new version:

.. code:: python

    >>> egg = open('some_egg.egg')
    >>> scrapyd.add_version('project_name', 'version_name', egg)
    # Returns the number of spiders in the project.
    3
    >>> egg.close()

**Cancel a scheduled job**:

.. code:: python

    >>> scrapyd.cancel('project_name', '14a6599ef67111e38a0e080027880ca6')
    # Returns True if the request was met with an OK response.
    True

**Delete a project** and all sibling versions:

.. code:: python

    >>> scrapyd.delete_project('project_name')
    # Returns True if the request was met with an OK response.
    True

**Delete a version** of a project:

.. code:: python

    >>> scrapyd.delete_version('project_name', 'version_name')
    # Returns True if the request was met with an OK response.
    True

**List all jobs** registered:

.. code:: python

    >>> scrapyd.list_jobs('project_name')
    # Returns a dict of running, finished and pending job lists.
    {
        'running': [
            {u'id': u'14a65...b27ce', u'spider': u'spider_name'},
            {u'id': u'78fe2...1278d', u'spider': u'spider_name2'},
        ]
        'finished': [
            ...
        ]
        'pending': [
            ...
        ]
    }

**List all projects** registered:

.. code:: python

    >>> scrapyd.list_projects()
    [u'ecom_project', u'estate_agent_project', u'car_project']

**List all spiders** available to a given project:

.. code:: python

    >>> scrapyd.list_spiders('project_name')
    [u'raw_spider', u'js_enhanced_spider', u'selenium_spider']

**List all versions** registered to a given project:

.. code:: python

    >>> scrapyd.list_versions('project_name'):
    [u'345', u'346', u'347', u'348']

**Schedule a job** to run with a specific spider:

.. code:: python

    # Schedule a job to run with a specific spider.
    >>> scrapyd.schedule('project_name', 'spider_name')
    # Returns the Scrapyd job id.
    u'14a6599ef67111e38a0e080027880ca6'

**Schedule a job** to run while passing override settings:

.. code:: python

    >>> settings = {'DOWNLOAD_DELAY': 2}
    >>> scrapyd.schedule('project_name', 'spider_name', settings=settings)
    u'25b6588ef67333e38a0e080027880de7'

**Schedule a job** to run while passing extra attributes to spider initialisation:

.. code:: python

    >>> scrapyd.schedule('project_name', 'spider_name', extra_attribute='value')
    # NB: 'project', 'spider' and 'settings' are reserved kwargs for this
    # method; extra attributes can be called any other Python-acceptable name.
    u'25b6588ef67333e38a0e080027880de7'


Contributing code and/or running the tests
------------------------------------------

Please see DEVELOPMENT.rst_ or refer to the `full documentation`_.

.. _DEVELOPMENT.rst: https://github.com/djm/python-scrapyd-api/blob/master/CONTRIBUTING.rst
.. _full documentation: http://python-scrapyd-api.rtfd.org


License
-------

2-clause BSD. See the full LICENSE_.

.. _LICENSE: https://github.com/djm/python-scrapyd-api/blob/master/LICENSE 
