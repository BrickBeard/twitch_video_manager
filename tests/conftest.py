from pytest import fixture
import requests
from flask import request, url_for
from collections import namedtuple
from project import create_app

base_url = 'http://localhost:5000{}'


# Test Fixtures
@fixture(scope='session')
def app():
    app_ = create_app('test.cfg')
    print(app_.config)
    ctx = app_.app_context()
    ctx.push()
    
    yield app_

    ctx.pop()

@fixture(scope='session')
def test_client(app):
    return app.test_client()


# Request Method
def get_(test_client, view, **kwargs):
    response = namedtuple('response', 'response request_path')
    with test_client as tc:
        response_ = tc.get(url_for(view), follow_redirects=True)
        request_ = request.path 
        return response(response_, request_)

def get_live(test_client, view, **kwargs):
    response = requests.get(url_for(view))