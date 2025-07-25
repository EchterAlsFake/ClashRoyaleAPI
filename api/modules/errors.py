class InvalidAPIToken(Exception):
    def __init__(self, msg):
        self.msg = msg


class RateLimitExceeded(Exception):
    def __init__(self, msg):
        self.msg = msg


class APIError(Exception):
    def __init__(self, msg):
        self.msg = msg


class InvalidParameter(Exception):
    def __init__(self, msg):
        self.msg = msg