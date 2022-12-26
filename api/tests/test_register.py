from main import app

def test_register():
    url = '/api/register'
    res = app.test_client().post(url)
    assert res.status_code == 201
    res_json = res.json
    assert 'username' in res_json
    assert 'password' in res_json
    assert type(res_json['username']) == str
    assert type(res_json['password']) == str