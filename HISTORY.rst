.. :changelog:

History
-------

2.1.0 (2018-03-31)
++++++++++++++++++

* Introduces the `timeout` keyword argument, which allows the caller to specify
  a timeout after which requests to the scrapyd server give up. This works as
  per the underlying `requests` library, and raises `requests.exceptions.Timeout`
  when the timeout is exceeded. See docs for usage.


2.0.1 (2016-02-27)
++++++++++++++++++

v2.0.0 shipped with docs which were slightly out of date for the cancel
endpoint, this release corrects that.

2.0.0 (2016-02-27)
++++++++++++++++++

Why Version 2? This package has been production ready and stable in use
for over a year now, so it's ready  to commit to a stable API /w semver.
Version 1 has deliberately been skipped to make it absolutely clear that
this release contains a breaking change:

Breaking changes:

* The cancel job endpoint now returns the previous state of the successfully
  cancelled spider rather than a simple boolean True/False. This change was
  made because:
    a) the boolean return was relatively useless and actually hiding data the
       scrapyd API passes us as part of the cancel endpoint response.
    b) before this change, the method would have returned `True` only if the
       cancelled job was previously running, and this resulted in us incorrectly
       reporting `False` when a *pending* job was cancelled.
  This may require no changes to your codebase but nevertheless it is a change
  in a public API, thus the requirement for major version bumping.

Other changes:

* The cancel job endpoint now accepts a `signal` keyword argument which is
  the termination signal Scrapyd uses to cancel the spider job. If not
  specified, the value is not sent to the scrapyd endpoint at all, therefore
  allows scrapyd control over which default signal gets used (currently `TERM`).


0.2.0 (2015-01-14)
++++++++++++++++++

* Added the new ``job_status`` method which can retrieve the job status of a
  specific job from a project. See docs for usage.
* Increased and improved test coverage.

0.1.0 (2014-09-16)
++++++++++++++++++

* First release on PyPI.
