from compatibility import SUPPORTED_CATALOGS
from client import request_payload

def grade():
    payload = request_payload([{'id': 'one'}])
    return payload.get('schemaVersion') == 1 and SUPPORTED_CATALOGS == {1, 2}
