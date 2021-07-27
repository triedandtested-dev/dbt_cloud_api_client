import requests
import json

from .base import EndPoint
from .run import JobRun

JOBS_ENDPOINT = 'jobs/'


class Jobs(EndPoint):

    def __init__(self, account):
        self._account = account
        self._data = None

    def _get_token(self):
        return self._account.client.token

    @property
    def endpoint(self):
        return '{}{}'.format(self._account.endpoint, JOBS_ENDPOINT)

    @property
    def data(self):
        return self._data

    def reload(self):
        self._data = [Job.fromdict(data, self._account) for data in self._get_data(self.endpoint)]


class Job(EndPoint):

    def __init__(self, data, account):
        self._data = data
        self._account = account

    @classmethod
    def fromdict(cls, datadict, account):
        "Initialize Job from a DBT cloud data dictionary"
        return cls(datadict, account=account)

    def _get_token(self):
        return self._account.client.token

    @property
    def endpoint(self):
        return '{}{}{}/'.format(self._account.endpoint, JOBS_ENDPOINT, self.id)

    @property
    def id(self):
        return self._data['id']

    @property
    def name(self):
        return self._data['name']

    @property
    def data(self):
        return self._data

    def reload(self):
        self._data = self._get_data(self.endpoint)

    def run(self, cause, payload={}):

        # A run always needs a cause.
        payload['cause'] = cause

        # run uri
        endpoint = '{}{}'.format(self.endpoint, 'run/')

        return JobRun(self._post_data(endpoint, payload), self._account)
