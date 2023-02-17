import json
import requests


class BrsApiModule:
    def __init__(self):
        self.api_url = 'http://brs.cs.vsu.ru/brs/public_api/'

    def get_students(self):
        return json.loads(requests.get(self.api_url + 'students').content)

    def set_student_login(self, student_id, login):
        return json.loads(
            requests.post(self.api_url + 'students/' + student_id, {'login': login}).content)
        pass
