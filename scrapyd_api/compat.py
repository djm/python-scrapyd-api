# This library is a cut down version of the `six` package; it
# is designed to contain exactly & only what we need to support
# Python 2 & 3 concurrently.
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


if PY3:
    import io
    StringIO = io.StringIO

    def iteritems(d, **kw):
        return iter(d.items(**kw))
else:  # PY2
    import StringIO
    StringIO = StringIO.StringIO

    def iteritems(d, **kw):
        return iter(d.iteritems(**kw))

try:
    # Python 3
    from urllib.parse import urljoin
except ImportError:
    # Python 2
    from urlparse import urljoin
