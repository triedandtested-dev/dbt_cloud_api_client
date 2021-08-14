from .base import EndPoint

RUN_ENDPOINT = 'runs/'

RUN_STATUS = {
    1: 'Queued',
    2: 'Starting',
    3: 'Running',
    10: 'Success',
    20: 'Error',
    30: 'Cancelled'
}


class JobRun(EndPoint):

    def __init__(self, data, account):
        self._data = data
        self._account = account

    def _get_token(self):
        return self._account.client.token

    @property
    def id(self):
        return self._data['id']

    @property
    def status(self):
        return RUN_STATUS[self._data['status']]

    @property
    def data(self):
        return self._data

    @property
    def endpoint(self):
        return '{}{}{}/'.format(self._account.endpoint, RUN_ENDPOINT, self.id)

    def is_finished(self):
        return self._data['finished_at'] is not None

    def reload(self):
        self._data = self._get_data(self.endpoint)
