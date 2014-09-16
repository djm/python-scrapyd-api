Development
===========

Thanks for wanting to help out!

* Bugs/feature requests should be filed using the Github Issues system.
* Code contributions/pull requests, please read CONTRIBUTING.RST_ first.

How to get the project up and running
-------------------------------------

To get started:

.. code:: bash

    $ git clone git@github.com:djm/python-scrapyd-api.git
    $ mkvirtualenv python-scrapyd-api
    $ cd python-scrapyd-api
    $ python setup.py develop
    $ pip install -r require

How to run the tests
--------------------

To run the tests:

.. code:: bash

    $ python setup.py test
    # or use PyTest directly:
    $ py.test

To see coverage:

.. code:: bash

    # In the terminal:
    $ py.test --cov scrapyd_api tests/
    # As a browseable HTML report:
    $ make coverage


Other development commands
--------------------------

Please run ``make help`` or see the Makefile_ for other development related commands.

.. _CONTRIBUTING.rst: https://github.com/djm/python-scrapyd-api/blob/master/CONTRIBUTING.rst
.. _Makefile: https://github.com/djm/python-scrapyd-api/blob/master/Makefile
