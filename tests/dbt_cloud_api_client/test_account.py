import unittest
from unittest.mock import MagicMock, patch, PropertyMock

from dbt_cloud_api_client.account import ACCOUNTS_ENDPOINT, Accounts, Account
from dbt_cloud_api_client.client import DbtCloudClient
from dbt_cloud_api_client.job import Job


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

    def test_account_from_dict(self):

        data = {
            'id': 1232,
            'name': 'expected_name'
        }

        account = Account.fromdict(data, client=self.client)

        self.assertEqual(1232, account.id)
        self.assertEqual('expected_name', account.name)
        self.assertEqual(self.client, account.client)

    def test_account_get_calls_get_data(self):

        data = {
            'id': 1232,
            'name': 'expected_name'
        }
        account = Account.fromdict(data, client=self.client)
        account._get_data = MagicMock()

        account.get()

        account._get_data.assert_called_once_with(account.endpoint)

    def test_account_get_jobs(self):

        data = {
            'id': 1232,
            'name': 'expected_name'
        }

        with patch('dbt_cloud_api_client.account.Jobs') as mJobs:

            type(mJobs()).data = PropertyMock(return_value=['job'])

            account = Account.fromdict(data, client=self.client)

            jobs = account.get_jobs()

            mJobs().reload.assert_called_once_with()
            self.assertEqual(['job'], jobs)

    def test_account_get_job_by_id(self):

        data = {'id': 1232}

        with patch('dbt_cloud_api_client.account.Job') as mJob:
            account = Account.fromdict(data, client=self.client)

            job = account.get_job_by_id(12)

            mJob.assert_called_once_with(data={'id': 12}, account=account)
            mJob().reload.assert_called_once_with()
            self.assertEqual(mJob(), job)

    def test_account_get_job_by_name(self):

        account = Account.fromdict({'id': 1232}, client=self.client)

        expected = Job.fromdict({'id': 12, 'name': 'test'}, account)

        mJobs = MagicMock()
        mJobs.return_value = [expected]
        account.get_jobs = mJobs

        job = account.get_job_by_name('test')

        self.assertEqual(expected, job)

    def test_account_get_job_by_name_raises(self):

        expected = RuntimeError("Job '{}' not found.".format('not_real_job'))

        account = Account.fromdict({'id': 1232}, client=self.client)

        mJobs = MagicMock()
        mJobs.return_value = [Job.fromdict({'id': 12, 'name': 'test'}, account)]
        account.get_jobs = mJobs

        with self.assertRaises(RuntimeError) as e:
            account.get_job_by_name('not_real_job')

        actual = e.exception
        self.assertEqual(str(expected), str(actual))
