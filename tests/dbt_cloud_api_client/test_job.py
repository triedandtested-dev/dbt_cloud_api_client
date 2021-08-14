import unittest
# from unittest.mock import MagicMock

from dbt_cloud_api_client.job import JOBS_ENDPOINT, Jobs, Job
from dbt_cloud_api_client.account import Account
from dbt_cloud_api_client.client import DbtCloudClient


class JobTests(unittest.TestCase):

    account = Account({'id': 1234}, DbtCloudClient(''))

    def test_jobs_endpoint(self):

        expected = '{}{}'.format(self.account.endpoint, JOBS_ENDPOINT)

        actual = Jobs(account=self.account).endpoint

        self.assertEqual(expected, actual)

    def test_job_endpoint(self):

        expected = '{}{}1232/'.format(self.account.endpoint, JOBS_ENDPOINT)

        actual = Job({'id': 1232}, account=self.account).endpoint

        self.assertEqual(expected, actual)

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
