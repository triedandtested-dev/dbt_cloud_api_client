from .account import Accounts, Account


class DbtCloudClient:

    def __init__(self, token, host='https://cloud.getdbt.com', port=80, api_version='v2'):

        self._token = token
        self._host = host
        self._port = port
        self._api_version = api_version

    def get_accounts(self):
        accounts = Accounts(client=self)
        accounts.get()
        return accounts.data

    def get_account_by_id(self, id):
        account = Account(data={'id': id}, client=self)
        account.get()
        return account

    def get_account_by_name(self, name):

        for account in self.get_accounts():
            if account.name == name:
                return account

        raise RuntimeError("Account '{}' not found.".format(name))

    @property
    def endpoint(self):
        return '{host}{port}/api/{version}/'.format(
            host=self._host,
            port=':{}'.format(self._port) if self._port != 80 else '',
            version=self._api_version)

    @property
    def token(self):
        return self._token
