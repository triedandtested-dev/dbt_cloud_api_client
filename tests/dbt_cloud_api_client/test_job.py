import unittest
from unittest.mock import MagicMock

from dbt_cloud_api_client.job import JOBS_ENDPOINT, Jobs, Job
from dbt_cloud_api_client.account import Account
from dbt_cloud_api_client.client import DbtCloudClient


class JobTests(unittest.TestCase):

    account = Account({'id': 1234}, DbtCloudClient('token'))

    def test_jobs_token(self):

        expected = 'token'

        actual = Jobs(account=self.account)._get_token()

        self.assertEqual(expected, actual)

    def test_jobs_endpoint(self):

        expected = '{}{}'.format(self.account.endpoint, JOBS_ENDPOINT)

        actual = Jobs(account=self.account).endpoint

        self.assertEqual(expected, actual)

    def test_jobs_data(self):

        expected = ['expected']

        jobs = Jobs(account=self.account)
        jobs._data = expected

        actual = jobs.data

        self.assertEqual(expected, actual)

    def test_jobs_reload(self):

        data = {
            'id': 1232,
            'name': 'expected_name'
        }

        job = Job(data, self.account)

        jobs = Jobs(account=self.account)
        jobs._get_data = MagicMock(return_value=[data])

        jobs.reload()

        jobs._get_data.assert_called_once_with(jobs.endpoint)
        self.assertEqual([job], jobs.data)

    def test_job_with_no_id_raises(self):

        with self.assertRaises(RuntimeError):
            Job({}, account=self.account)

    def test_job_token(self):

        expected = 'token'

        actual = Job({'id': 234}, account=self.account)._get_token()

        self.assertEqual(expected, actual)

    def test_job_endpoint(self):

        expected = '{}{}1232/'.format(self.account.endpoint, JOBS_ENDPOINT)

        actual = Job({'id': 1232}, account=self.account).endpoint

        self.assertEqual(expected, actual)

    def test_job_reload(self):

        data = {
            'id': 1232,
            'name': 'expected_name'
        }

        job = Job(data, self.account)
        job._get_data = MagicMock(return_value=data)

        job.reload()

        job._get_data.assert_called_once_with(job.endpoint)
        self.assertEqual(1232, job.id)
        self.assertEqual('expected_name', job.name)

    def test_job_run(self):

        payload = {
            'cause': 'trigger'
        }

        job = Job({'id': 433}, self.account)
        job._post_data = MagicMock(return_value={})

        job.run(cause='trigger')

        job._post_data.assert_called_once_with('{}{}'.format(job.endpoint, 'run/'), payload)
