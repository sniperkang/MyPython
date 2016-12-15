try:
    import json
except ImportError:
    import simplejson as json

print json.dumps({'python':2.7})
