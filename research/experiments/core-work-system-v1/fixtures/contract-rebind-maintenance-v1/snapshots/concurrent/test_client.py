from client import request_payload

def test_schema_version():
    assert request_payload([{'id': 'one'}])['schemaVersion'] == 1
