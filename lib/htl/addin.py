import requests


class HTLAddin():
    def __init__(self, addin_id, hdd_id, key):
        self.addin_id = addin_id
        self.hdd_id = hdd_id
        self.key = key

    def check_license(self):
        url = 'http://addin.htlcnn.net/license'
        data = {
            'addin_id': self.addin_id,
            'hdd_id': self.hdd_id,
            'key': self.key
        }
        res = requests.post(url, data=data)
        if res.status_code == 200:
            return True

    def execute(self):
