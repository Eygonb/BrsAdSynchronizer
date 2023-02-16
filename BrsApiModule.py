import json
import requests


def get_students():
    return json.loads(requests.get('http://brs.cs.vsu.ru/brs/public_api/students').content)


def set_student_login(student_id, login):
    return json.loads(
        requests.post('http://brs.cs.vsu.ru/brs/public_api/students/' + student_id, {'login': login}).content)
    pass
