import unittest
from unittest.mock import MagicMock

import responses
from requests import Response

import json


from dbt_cloud_api_client.base import EndPoint


class TestEndpoint(EndPoint):

    def _get_token(self):
        return 'test_token'


class BaseTests(unittest.TestCase):

    def test_headers(self):

        expected = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test_token'
        }

        endpoint = TestEndpoint()

        self.assertEqual(expected, endpoint.__get_headers__())

    def test_token(self):

        expected = 'test_token'

        endpoint = TestEndpoint()

        self.assertEqual(expected, endpoint._get_token())

    @responses.activate
    def test_get_data(self):

        endpoint = TestEndpoint()

        json = {
            "status": {
                "code": 200,
                "is_success": True,
                "user_message": "string",
                "developer_message": "string"
            },
            'data': {'key': 'value'}
        }

        responses.add(responses.GET, 'http://test/api/1/foobar',
                      json=json, status=200)

        actual = endpoint._get_data('http://test/api/1/foobar')

        self.assertEqual(json['data'], actual)
        self.assertEqual(1, len(responses.calls))

        request = responses.calls[0].request

        self.assertEqual('http://test/api/1/foobar', request.url)
        self.assertEqual(endpoint.__get_headers__()['Content-Type'], request.headers['Content-Type'])
        self.assertEqual(endpoint.__get_headers__()['Authorization'], request.headers['Authorization'])

    @responses.activate
    def test_post_data(self):
        endpoint = TestEndpoint()

        test_payload = {
            "status": {
                "code": 200,
                "is_success": True,
                "user_message": "string",
                "developer_message": "string"
            },
            'data': {'key': 'value'}
        }

        payload = {'test': 'test'}

        responses.add(responses.POST, 'http://test/api/1/foobar',
                      json=test_payload, status=200)

        actual = endpoint._post_data('http://test/api/1/foobar', payload)

        self.assertEqual(test_payload['data'], actual)
        self.assertEqual(1, len(responses.calls))

        request = responses.calls[0].request

        self.assertEqual('http://test/api/1/foobar', request.url)
        self.assertEqual(json.dumps(payload), request.body)
        self.assertEqual(endpoint.__get_headers__()['Content-Type'], request.headers['Content-Type'])
        self.assertEqual(endpoint.__get_headers__()['Authorization'], request.headers['Authorization'])

    def test_handle_response_with_200(self):

        expected = {'payload': 'value'}

        test = Response()
        test.status_code = 200
        test.json = MagicMock(return_value={
            "status": {
                "code": 200,
                "is_success": True,
                "user_message": "string",
                "developer_message": "string"
            },
            'data': expected
        })

        endpoint = TestEndpoint()

        actual = endpoint._handle_response(test)

        self.assertEqual(expected, actual)

    def test_handle_response_with_200_no_data_raises(self):

        test = Response()
        test.status_code = 200
        test.json = MagicMock(return_value={
            "status": {
                "code": 200,
                "is_success": True,
                "user_message": "string",
                "developer_message": "string"
            }
        })

        with self.assertRaises(RuntimeError):

            TestEndpoint()._handle_response(test)

    def test_handle_response_with_200_no_status_raises(self):

        test = Response()
        test.status_code = 200
        test.json = MagicMock(return_value={
            "data": {}
        })

        with self.assertRaises(RuntimeError):

            TestEndpoint()._handle_response(test)

    def test_handle_response_with_400_raises(self):

        test = Response()
        test.status_code = 400
        test.json = MagicMock(return_value={
            "status": {
                "code": 200,
                "is_success": True,
                "user_message": "string",
                "developer_message": "string"
            }
        })

        with self.assertRaises(RuntimeError):

            TestEndpoint()._handle_response(test)

    def test_handle_response_with_404_raises(self):
        test = Response()
        test.status_code = 404
        test.json = MagicMock(return_value={
            "status": {
                "code": 200,
                "is_success": True,
                "user_message": "string",
                "developer_message": "string"
            }
        })

        with self.assertRaises(RuntimeError):
            TestEndpoint()._handle_response(test)

    def test_handle_response_with_200_bad_status_raises(self):

        test = Response()
        test.status_code = 200
        test.json = MagicMock(return_value={
            "status": {
                "code": 500,
                "is_success": True,
                "user_message": "string",
                "developer_message": "string"
            },
            'data': {}
        })

        with self.assertRaises(RuntimeError):
            TestEndpoint()._handle_response(test)


        # thing = ProductionClass()
        # thing.method = MagicMock(return_value=3)
        # thing.method(3, 4, 5, key='value')
        # 3
        # thing.method.assert_called_with(3, 4, 5, key='value')



