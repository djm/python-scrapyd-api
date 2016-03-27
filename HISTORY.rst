.. :changelog:

History
-------

2.0.0 (2016-02-27)
++++++++++++++++++

Why Version 2? This package has been production ready and stable in use
for over a year now, so it's ready  to commit to a stable API /w semver.
Version 1 has deliberately been skipped to make it absolutely clear that
this release contains a breaking change:

Breaking changes:

* The cancel job endpoint now returns `True` on hearing a successful reply
  from the Scrapyd API; before it would have returned `True` only if the
  cancelled job was previously running, but this resulted in us incorrectly
  reporting `False` when a *pending* job was actually cancelled.

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
