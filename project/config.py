import os

def get_env_variable(name):
    try:
        return os.environ.get(name)
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)

client_id = get_env_variable('CLIENT_ID')
user_id = 139224404