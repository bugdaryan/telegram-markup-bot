from app import app
from tests import app_url

def test_get_labels():
    url = app_url + 'api/labels'
    res = app.test_client().get(url)
    res_json = res.json()
    assert res.status_code == 200
    assert type(res_json) == dict
    assert 'label' in res_json
    assert type(res_json['label']) == list
    assert 'id' in res_json
    assert type(res_json['id']) == list
    