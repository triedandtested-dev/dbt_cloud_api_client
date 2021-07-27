from abc import ABCMeta, abstractmethod
import requests
import json


class EndPoint(metaclass=ABCMeta):

    @abstractmethod
    def _get_token(self):
        pass

    def __get_headers__(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self._get_token())
        }

    def _get_data(self, url):
        response = requests.get(url, headers=self.__get_headers__())
        return self._handle_response(response)

    def _post_data(self, url, payload):
        response = requests.post(url, data=json.dumps(payload), headers=self.__get_headers__())
        return self._handle_response(response)

    def _handle_response(self, response):

        if response.status_code != 200:
            raise RuntimeError(response.json())

        payload = response.json()

        if 'status' not in payload.keys():
            raise RuntimeError('"status" not in response {}'.format(payload))

        if payload['status']['code'] != 200:
            raise RuntimeError(payload)

        if 'data' not in payload.keys():
            raise RuntimeError('"data" not in response {}'.format(payload))

        return payload['data']
