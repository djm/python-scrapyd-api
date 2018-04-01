# Contributing

`python-scrapyd-api` is free & open-source software and therefore every little
bit helps. Whether you're simply correcting a typo or bringing the release
up-to-date with 3rd party changes, all help is welcome and very appreciated.


## Reporting Bugs

Please report bugs by utilising [Github Issues][issues]. Simply check if your issue
exists first, and if not, submit a new issue.

[issues]: https://github.com/djm/python-scrapyd-api/issues

If you are reporting a bug:

* Detailed steps to reproduce the bug.
* Your operating system name and any versions of software (if applicable).
* Include any details about your local setup that might be helpful in
  troubleshooting.
* A pull request would be most appreciated but even just submitting the bug
  is very helpful, thanks!

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests, especially if fixing a regression.
2. If the pull request adds functionality, the docs should be updated to
   document that functionality.
3. The pull request should work for Python 2.6, 2.7, 3.3 and 3.4.
   Check [TravisCI][travis] and make sure that the tests pass for all supported Python versions.

 [travis]: https://travis-ci.org/djm/python-scrapyd-api/pull_requests

## Submitting Code

Ready to contribute? Here's how to set up `python-scrapyd-api` for local development.

1. Fork the `python-scrapyd-api` repo on GitHub.

2. Clone your fork locally:

        $ git clone git@github.com:your_name_here/python-scrapyd-api.git

3. Install your local copy into a `virtualenv`. Assuming you have `virtualenvwrapper` installed, this is how you set up your fork for local development:

        $ mkvirtualenv python-scrapyd-api
        $ cd python-scrapyd-api/
        $ python setup.py develop

4. Install the requirements needed to develop on `python-scrapyd-api`. That
   includes doc writing and testing tools:

        $ pip install -r requirements.txt


5. Create a branch for local development:

        $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

6. When you're done making changes, check the following things:

   a. That your changes pass the flake8 linter (use common sense though):

        $ pip install flake8
        $ flake8 python-scrapyd-api tests

   b. That the tests still run:

        $ python setup.py test

   c. That the tests run for all supported versions of Python. This requires tox and having the various versions of Python installed:

        $ pip install tox
        $ tox

7. Add yourself to the `AUTHORS.md` file as a contributor.

8. Commit your changes and push your branch to GitHub. Please use a suitable
   git commit message (summary line, two line breaks, detailed description):

        $ git add .
        $ git commit
        $ git push origin name-of-your-bugfix-or-feature

9. Submit a pull request through the GitHub website.


## How to run the tests

To run the tests:

```bash
$ python setup.py test
# or use PyTest directly:
$ py.test
```

To see coverage:

```bash
# In the terminal:
$ py.test --cov scrapyd_api tests/
# As a browseable HTML report:
$ make coverage

```

## Other development commands

Please run `make help` or see the [Makefile][makefile] for other development related commands.

[makefile]: https://github.com/djm/python-scrapyd-api/blob/master/Makefile
