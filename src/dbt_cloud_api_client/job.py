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

        if 'id' not in data.keys():
            raise RuntimeError("'id' is a required entry in data.")

        for key in data.keys():
            self.__setattr__(key, self._data[key])

    @classmethod
    def fromdict(cls, datadict, account):
        """Initialize Job from a DBT cloud data dictionary"""
        return cls(datadict, account=account)

    def _get_token(self):
        return self._account.client.token

    @property
    def endpoint(self):
        return '{}{}{}/'.format(self._account.endpoint, JOBS_ENDPOINT, self.__getattribute__('id'))

    def reload(self):
        self._data = self._get_data(self.endpoint)
        for key in self._data.keys():
            self.__setattr__(key, self._data[key])

    def run(self, cause, payload={}):

        # A run always needs a cause.
        payload['cause'] = cause

        # run uri
        endpoint = '{}{}'.format(self.endpoint, 'run/')

        return JobRun(data=self._post_data(endpoint, payload), account=self._account)

    def __eq__(self, other):
        if isinstance(other, Job):
            return self._data == other._data

        return False
