class Error(Exception):
    pass

class MissingHrefError(Error):
    """No href found for webpage link"""
    def __init__(self, msg):
        super().__init__(msg)

class Error404(Error):
    def __init__(self, msg):
        super().__init__(msg)