import sys 
import os
import pytest
import requests
import json
import warnings


#tests
class TestClass:
    # 1. Successful transact
    def test_one(self):
        url = 'http://localhost:5000/txion'
        headers = {'content-Type': 'application/json'}
        data = {"from": "dsdsfnj", "to":"fjlakdj", "amount": 2}
        payload = json.dumps(data, indent=4, sort_keys=True)
        r = requests.post(url, data = payload, headers = headers)
        print(r.text)
        assert r.text == "Transaction submission successful\n"


    def test_two(self):
        url = 'http://localhost:5000/blocks'
        r = requests.get(url)
        print(r.json())
        assert r.json()[0]["index"] == '0'
