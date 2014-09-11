from __future__ import unicode_literals

from requests import Session

from .exceptions import ScrapydResponseError


class Client(Session):
    """
    The client is a thin wrapper around the requests Session class which
    allows us to wrap the response handler so that we can handle it in a
    Scrapyd-specific way.
    """

    def _handle_response(self, response):
        """
        Handles the response received from Scrapyd.
        """
        if not response.ok:
            raise ScrapydResponseError(
                "Scrapyd returned a {0} error: {1}".format(
                    response.status_code,
                    response.text))

        try:
            json = response.json()
        except ValueError:
            raise ScrapydResponseError("Scrapyd returned an invalid JSON "
                                       "response: {0}".format(response.text))
        if json['status'] == 'ok':
            json.pop('status')
            return json
        elif json['status'] == 'error':
            raise ScrapydResponseError(json['message'])

    def request(self, *args, **kwargs):
        response = super(Client, self).request(*args, **kwargs)
        return self._handle_response(response)
