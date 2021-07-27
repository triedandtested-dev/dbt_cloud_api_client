import unittest

from dbt_cloud_api_client.account import ACCOUNTS_ENDPOINT, Accounts, Account
from dbt_cloud_api_client.client import DbtCloudClient


class AccountTests(unittest.TestCase):

    client = DbtCloudClient('token')

    def test_accounts_endpoint(self):

        expected = '{}{}'.format(self.client.endpoint, ACCOUNTS_ENDPOINT)

        actual = Accounts(client=self.client).endpoint

        self.assertEqual(expected, actual)

    def test_account_endpoint(self):

        expected = '{}{}1232/'.format(self.client.endpoint, ACCOUNTS_ENDPOINT)

        actual = Account({'id': 1232}, client=self.client).endpoint

        self.assertEqual(expected, actual)

    def test_accounts_token(self):

        expected = self.client.token

        actual = Accounts(client=self.client)._get_token()

        self.assertEqual(expected, actual)

    def test_accounts_data(self):

        expected = 'expected_data'

        accounts = Accounts(client=self.client)
        accounts._data = expected

        self.assertEqual(expected, accounts.data)

    def test_account_token(self):

        expected = self.client.token

        actual = Account({'id': 1232}, client=self.client)._get_token()

        self.assertEqual(expected, actual)

    def test_account_data(self):

        expected = 'expected_data'

        account = Account({'id': 1232}, client=self.client)
        account._data = expected

        self.assertEqual(expected, account.data)

    def test_account_name(self):

        data = {
            'id': 1232,
            'name': 'expected_name'
        }

        account = Account(data, client=self.client)

        self.assertEqual(data['name'], account.name)

    def test_account_with_no_id_raises(self):

        with self.assertRaises(RuntimeError):
            Account({}, client=self.client)

    def test_account_client(self):

        data = {
            'id': 1232,
            'name': 'expected_name'
        }

        account = Account(data, client=self.client)

        self.assertEqual(self.client, account.client)


    # def test_client_endpoint_with_custom_port(self):
    #
    #     expected = 'https://cloud.getdbt.com:8080/api/v2/'
    #
    #     actual = DbtCloudClient('token', port=8080).endpoint
    #
    #     self.assertEqual(expected, actual)
    #
    # def test_client_endpoint_with_custom_host(self):
    #
    #     expected = 'https://custom.com/api/v2/'
    #
    #     actual = DbtCloudClient('token', host='https://custom.com').endpoint
    #
    #     self.assertEqual(expected, actual)
    #
    # def test_client_endpoint_with_custom_version(self):
    #
    #     expected = 'https://cloud.getdbt.com/api/latest/'
    #
    #     actual = DbtCloudClient('token', api_version='latest').endpoint
    #
    #     self.assertEqual(expected, actual)
