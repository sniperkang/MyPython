from __future__ import division
from __future__ import unicode_literals


try:
    import json
except ImportError:
    import simplejson as json

print json.dumps({'python':2.7})


print 10 / 3


s = 'am I an unicode?'
print isinstance(s, unicode)