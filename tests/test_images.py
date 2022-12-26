from app import app

def register():
    url = '/api/register'
    res = app.test_client().post(url)
    res_json = res.json

    return res_json['username'], res_json['password']

def test_image_correct():
    username, password = register()
    url = '/api/images'
    res = app.test_client().get(url, auth=(username, password))
    res_json = res.json
    assert res.status_code == 200
    assert 'image' in res_json
    assert 'image_id' in res_json

def test_image_incorrect_username():
    username, password = register()
    url = '/api/images'
    res = app.test_client().get(url, auth=(username + '1', password))
    assert res.status_code == 401

def test_image_incorrect_password():
    username, password = register()
    url = '/api/images'
    res = app.test_client().get(url, auth=(username, password + '1'))
    assert res.status_code == 401