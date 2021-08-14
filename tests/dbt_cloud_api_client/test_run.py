import unittest
from unittest.mock import MagicMock

from dbt_cloud_api_client.run import JobRun, RUN_ENDPOINT, RUN_STATUS
from dbt_cloud_api_client.account import Account
from dbt_cloud_api_client.client import DbtCloudClient


class JobRunTests(unittest.TestCase):

    account = Account({'id': 1234}, DbtCloudClient('token'))

    def test_run_token(self):

        expected = 'token'

        actual = JobRun({'id': 234}, account=self.account)._get_token()

        self.assertEqual(expected, actual)

    def test_run_id(self):

        actual = JobRun({'id': 1232}, account=self.account)

        self.assertEqual(1232, actual.id)

    def test_run_status(self):

        run = JobRun({'id': 1232}, account=self.account)
        for code in RUN_STATUS.keys():
            run._data['status'] = code
            self.assertEqual(RUN_STATUS[code], run.status)

    def test_run_endpoint(self):
        expected = '{}{}{}/'.format(self.account.endpoint, RUN_ENDPOINT, 345)

        actual = JobRun(data={'id': 345}, account=self.account).endpoint

        self.assertEqual(expected, actual)

    def test_run_is_finished(self):

        run = JobRun(data={'id': 345}, account=self.account)

        run._data['finished_at'] = None
        self.assertFalse(run.is_finished())

        run._data['finished_at'] = 'complete'
        self.assertTrue(run.is_finished())

    def test_run_reload(self):
        data = {
            'id': 1232,
            'name': 'expected_name'
        }

        run = JobRun(data, self.account)
        run._get_data = MagicMock(return_value=data)

        run.reload()

        run._get_data.assert_called_once_with(run.endpoint)
