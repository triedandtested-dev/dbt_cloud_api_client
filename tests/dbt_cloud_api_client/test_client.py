import unittest
# from unittest.mock import MagicMock

from dbt_cloud_api_client.client import DbtCloudClient


class DbtCloudClientTests(unittest.TestCase):
    # expected = 'https://cloud.getdbt.com/api/v2/accounts/'

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
