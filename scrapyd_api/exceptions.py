from __future__ import unicode_literals


class ScrapydError(Exception):
    """
    Base class for Scrapyd API exceptions.
    """
    default_detail = 'Scrapyd Error'

    def __init__(self, detail=None):
        self.detail = detail or self.default_detail

    def __str__(self):
        return self.detail

    def __repr__(self):
        return '{0}("{1}")'.format(self.__class__.__name__, self.detail)


class ScrapydResponseError(ScrapydError):

    default_detail = 'Scrapyd Response Error'
