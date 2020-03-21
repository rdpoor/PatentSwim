import bottle
from bottle import response, hook
from patent_factory import PatentFactory
import re

"""
Handle RESTful requests for patent info, return JSON formatted data
"""

app = bottle.app()
patent_factory = PatentFactory()

@app.route('/api/patents/<ids>')
def get_patents(ids):
    """
    Return a dict of {patent_number: dict, ...}, looking up patents from the
    online service if needed.
    """
    # Transform '1234, 4567' into ['1234','4567']
    ids = ids.replace(' ','').split(',')
    return patent_factory.get_patents(ids)  # return dict of {number: <patent> ...}

@app.route('/api/patent/<id>')
def get_patent(id):
    """
    Return a singleton dict of {patent_number:dict}, or None if the patent has
    not been fetched.
    """
    patent = patent_factory.find_patent(id)
    if patent is not None:
        print('get_patent({}) => {}'.format(id, patent))
        return patent
    else:
        return None

@hook('after_request')
def enable_cors():
    # TODO: Why does setting this to 'http://localhost' or
    # 'http://localhost/*' fail?
    response.headers['Access-Control-Allow-Origin'] = '*'

def runServer(host='localhost', port=8080, debug=True):
    bottle.run(app, host=host, port=port, debug=debug)
