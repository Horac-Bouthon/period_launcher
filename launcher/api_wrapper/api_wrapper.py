import requests
import json
from json_wrapper.json_wrapper import JsonWrapper

import logging
import api_wrapper


class ApiWrapper:

    def post_json(self, json_obj):
        r = requests.post(self.url, json=json_obj, headers={"Content-Type": "application/json"})
        self.logger.debug('Post (json) response: {}'.format(r))
        self.logger.debug('Post (json) response text: {}'.format(r.text))

    def __init__(self, url):
        self.logger = logging.getLogger(api_wrapper.LOGGER_NAME)
        self.url = url
        self.logger.info('Create: {}'.format(repr(self)))

    def __repr__(self):
        return "ApiWrapper('{}')"\
            .format(self.url)

    def __str__(self):
        return self.url
