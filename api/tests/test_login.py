from main import app

def register():
    url = '/api/register'
    res = app.test_client().post(url)
    res_json = res.json

    return res_json['username'], res_json['password']

def test_login_correct():
    username, password = register()
    url = '/api/login'
    res = app.test_client().get(url, auth=(username, password))
    res_json = res.json
    assert res.status_code == 200
    assert 'duration' in res_json
    assert 'token' in res_json

def test_login_incorrect_username():
    username, password = register()
    url = '/api/login'
    res = app.test_client().get(url, auth=(username + '1', password))
    assert res.status_code == 401

def test_login_incorrect_password():
    username, password = register()
    url = '/api/login'
    res = app.test_client().get(url, auth=(username, password + '1'))
    assert res.status_code == 401

def test_login_empty_username():
    username, password = register()
    url = '/api/login'
    res = app.test_client().get(url, auth=('', password))
    assert res.status_code == 401

def test_login_empty_password():
    username, password = register()
    url = '/api/login'
    res = app.test_client().get(url, auth=(username, ''))
    assert res.status_code == 401