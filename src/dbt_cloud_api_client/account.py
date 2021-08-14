from .base import EndPoint
from .job import Jobs, Job

ACCOUNTS_ENDPOINT = 'accounts/'


class Accounts(EndPoint):

    def __init__(self, client):
        self._client = client
        self._data = None

    def _get_token(self):
        return self._client.token

    @property
    def endpoint(self):
        return '{}{}'.format(self._client.endpoint, ACCOUNTS_ENDPOINT)

    @property
    def data(self):
        return self._data

    def get(self):
        self._data = [Account.fromdict(data, self._client) for data in self._get_data(self.endpoint)]


class Account(EndPoint):

    def __init__(self, data, client=None):

        self._client = client
        self._data = data

        if 'id' not in data.keys():
            raise RuntimeError("'id' is a required entry in data.")

        for key in data.keys():
            self.__setattr__(key, self._data[key])

    def _get_token(self):
        return self._client.token

    @property
    def endpoint(self):
        return '{}{}{}/'.format(self._client.endpoint, ACCOUNTS_ENDPOINT, self.__getattribute__('id'))

    @classmethod
    def fromdict(cls, datadict, client):
        """Initialize Account from a DBT cloud data dictionary"""
        return cls(datadict, client=client)

    @property
    def data(self):
        return self._data

    @property
    def client(self):
        return self._client

    def get(self):
        self._data = self._get_data(self.endpoint)
        for key in self._data.keys():
            self.__setattr__(key, self._data[key])

    def get_jobs(self):

        jobs = Jobs(account=self)
        jobs.reload()

        return jobs.data

    def get_job_by_id(self, id):
        job = Job(data={'id': id}, account=self)
        job.reload()
        return job

    def get_job_by_name(self, name):
        for job in self.get_jobs():
            if job.name == name:
                return job

        raise RuntimeError("Job '{}' not found.".format(name))
