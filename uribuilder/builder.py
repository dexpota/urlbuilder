from .uri import SCHEME, FRAGMENT, QUERY
from .exceptions import UriBuildingException
from collections import namedtuple
from urllib import parse
import urllib


class UriBuilder:
    def scheme(self, value):
        if SCHEME.match(value) is None:
            raise UriBuildingException()
        self._scheme = value
        return self

    def host(self, value):
        self._host = value
        return self

    def port(self, value):
        self._port = value
        return self

    def path(self, value):
        self._path = value
        return self

    def fragment(self, value):
        if FRAGMENT.match(value) is None:
            raise UriBuildingException()
        self._fragment = value
        return self

    def params(self, value):
        self._params = value
        return self

    def add_parameter(self, key, value):
        self.parameters.append((key, value))
        return self

    def __init__(self):
        self._scheme = ""
        self._host = ""
        self._port = ""
        self._path = ""
        self._params = ""
        self._userinfo = None
        self._query = None
        self._fragment = ""

        self.parameters = []

    def build(self):
        # TODO Check if we got all parameters

        Uri = namedtuple("Uri", ['scheme', 'netloc',
                                 'path', 'params', 'query', 'fragment'])
        # Parse parameters and produce a query string
        q = parse.urlencode(self.parameters)

        _netloc = self._build_netloc(self._userinfo, self._host, self._port)

        u = Uri(scheme=self._scheme, netloc=_netloc, path=self._path,
                params=self._params, query=q, fragment=self._fragment)
        return urllib.parse.urlunparse(u)

    def parse(self):
        raise NotImplementedError()

    @staticmethod
    def _build_netloc(userinfo, host, port):
        netloc = []

        if userinfo is not None:
            netloc.append("{userinfo}@".format(userinfo=userinfo))

        netloc.append(host)

        if port is not None:
            netloc.append(":{port}".format(port=port))

        return "".join(netloc)
