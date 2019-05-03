from project import config



def test_config_variables_are_valid(test_client):
    assert config.client_id
    assert config.user_id == 139224404