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

    def _handle_json_response(self, response):
        """
        Handles the response received from Scrapyd.
        """
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
        """
        Takes not_json to signal whether response should be parsed as json or
        not.
        """
        not_json = 'not_json' in kwargs and kwargs['not_json']
        if 'not_json' in kwargs:
            del kwargs['not_json']
        response = super(Client, self).request(*args, **kwargs)
        self._handle_response(response)
        if not_json:
            return response.text
        else:
            return self._handle_json_response(response)
