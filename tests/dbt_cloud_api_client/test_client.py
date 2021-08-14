import unittest
from unittest.mock import MagicMock, patch, PropertyMock

from dbt_cloud_api_client.client import DbtCloudClient
from dbt_cloud_api_client.account import Account


class DbtCloudClientTests(unittest.TestCase):

    def test_client_default_endpoint(self):

        expected = 'https://cloud.getdbt.com/api/v2/'

        actual = DbtCloudClient('token').endpoint

        self.assertEqual(expected, actual)

    def test_client_endpoint_with_custom_port(self):

        expected = 'https://cloud.getdbt.com:8080/api/v2/'

        actual = DbtCloudClient('token', port=8080).endpoint

        self.assertEqual(expected, actual)

    def test_client_endpoint_with_custom_host(self):

        expected = 'https://custom.com/api/v2/'

        actual = DbtCloudClient('token', host='https://custom.com').endpoint

        self.assertEqual(expected, actual)

    def test_client_endpoint_with_custom_version(self):

        expected = 'https://cloud.getdbt.com/api/latest/'

        actual = DbtCloudClient('token', api_version='latest').endpoint

        self.assertEqual(expected, actual)

    def test_client_get_accounts(self):

        with patch('dbt_cloud_api_client.client.Accounts') as m_accounts:
            type(m_accounts()).data = PropertyMock(return_value=['account'])

            client = DbtCloudClient('token', api_version='latest')

            accounts = client.get_accounts()

            m_accounts().get.assert_called_once_with()
            self.assertEqual(['account'], accounts)

    def test_client_get_account_by_id(self):

        with patch('dbt_cloud_api_client.client.Account') as m_account:
            client = DbtCloudClient('token', api_version='latest')

            account = client.get_account_by_id(12)

            m_account.assert_called_once_with(data={'id': 12}, client=client)
            m_account().get.assert_called_once_with()
            self.assertEqual(m_account(), account)

    def test_client_get_account_by_name(self):

        client = DbtCloudClient('token', api_version='latest')

        expected = Account({'id': 12, 'name': 'test'}, client=client)

        m_accounts = MagicMock()
        m_accounts.return_value = [expected]
        client.get_accounts = m_accounts

        actual = client.get_account_by_name('test')

        self.assertEqual(expected, actual)

    def test_client_get_account_by_name_raises(self):

        client = DbtCloudClient('token', api_version='latest')

        account = Account({'id': 12, 'name': 'test'}, client=client)
        expected = RuntimeError("Account '{}' not found.".format('not_real_account'))

        m_accounts = MagicMock()
        m_accounts.return_value = [account]
        client.get_accounts = m_accounts

        with self.assertRaises(RuntimeError) as e:
            client.get_account_by_name('not_real_account')

        actual = e.exception
        self.assertEqual(str(expected), str(actual))
