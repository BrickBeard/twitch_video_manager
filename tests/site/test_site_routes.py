from pytest import mark
from tests.conftest import get_
from project.site import views
from flask import url_for, request


@mark.site
def test_index_as_expected(test_client):
    view_ = get_(test_client, 'site.index')
    assert view_.response.status_code == 200
    
def test_videos_highlight_as_expected(test_client):
    view_ = get_(test_client, 'site.videos_highlight')
    assert view_.response.status_code == 200

