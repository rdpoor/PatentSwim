import json
import requests

class PatentFactory(object):

    def __init__(self):
        self._patents = {}

    def find_patent(self, patent_id):
        """
        Return a previously loaded patent, or None if not present.
        """
        return self._patents.get(str(patent_id), None)

    def clear(self):
        """
        Discard all loaded patents.
        """
        self._patents.clear()

    def patents(self):
        """
        Return the dict of loaded patents.
        """
        return self._patents

    MAX_PATENTS_PER_QUERY = 25  # empirical

    def get_patents(self, patent_ids):
        """
        Return a dict of {patent_id:patent, ...}, using cached values when
        available or fetching from patentsview.org via their API.
        """
        # coerce patent numbers to strings.
        patent_ids = [str(p) for p in patent_ids]
        # find the difference between requested and already fetched patents
        missing_ids = list(set(patent_ids) - self._patents.keys())
        while len(missing_ids) > 0:
            # request up to MAX_PATENTS_PER_QUERY at a time
            slice = missing_ids[:self.MAX_PATENTS_PER_QUERY]
            print('requesting {} patents...'.format(len(slice)), end='')
            patents_attributes = self._fetch_patents_details(slice)
            print('got {} patents'.format(len(patents_attributes)))
            self._intern_patents(patents_attributes)
            # advance to the next slice
            missing_ids = missing_ids[self.MAX_PATENTS_PER_QUERY:]

        # Return a dict of patent numbers and their patents
        return {k: self._patents[k] for k in patent_ids}

    def _intern_patents(self, patents_attributes):
        """
        Store patent_attributes for a list of patents.
        """
        for patent_attributes in patents_attributes:
            self._intern_patent(patent_attributes)

    def _intern_patent(self, patent_attributes):
        """
        Store the patent_attributes in the data store, indexed by patent_id.
        """
        patent_id = patent_attributes['patent_number']
        self._patents[patent_id] = patent_attributes

    PATENT_API_ENDPOINT = 'www.patentsview.org/api/patents/query'

    def _fetch_patents_details(self, patent_ids):
        """
        Perform a POST to query the patentsview.org API.  Return the JSON
        formatted attributes for the requested patents.
        """
        uri = 'https://' + self.PATENT_API_ENDPOINT
        payload = self._make_post_payload(patent_ids)
        print('requesting payload={}'.format(json.dumps(payload)))
        r = requests.post(uri, data=json.dumps(payload))
        # print('request headers = {}'.format(r.request.headers))
        print('response headers = {}'.format(r.headers))
        return r.json()['patents']

    PATENT_ATTRIBUTES = [
        'patent_number',
        'patent_date',
        'cited_patent_number',
        'cited_patent_title',
        'cited_patent_date',
        'citedby_patent_number',
        'citedby_patent_title',
        'citedby_patent_date',
        'patent_abstract',
        'patent_title',
        ]

    def _make_post_payload(self, patent_ids):
        """
        Create a query for the patentsview.org API requesting details on a list
        of patent numbers.  Returns a dict.
        """
        # coerce patent_ids to strings
        ids = [str(p) for p in patent_ids]
        return {'q':{'patent_number':ids}, 'f':self.PATENT_ATTRIBUTES}
