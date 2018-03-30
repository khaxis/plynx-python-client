class Client(object):
    def __init__(self, endpoint=None, token=None):
        self.endpoint = endpoint or 'http://127.0.0.1:5000/plynx/api/v0'
        self.token = token or ''
