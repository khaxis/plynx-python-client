import os

class Client(object):
    def __init__(self, endpoint=None, token_path=None):
        self.endpoint = endpoint or \
            os.environ.get('PLYNX_ENDPOINT', '') or \
            'http://plynx.com/plynx/api/v0'

        token_path = token_path or \
            os.environ.get('PLYNX_TOKEN_PATH', '') or \
            os.path.join(os.path.expanduser("~"), '.plynx_token')

        with open(token_path) as f:
            self.refresh_token = f.readline().rstrip()
        print self.refresh_token
