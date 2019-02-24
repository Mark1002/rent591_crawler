"""Exception for API endpoints."""


class FormatError(Exception):
    """Format error exception."""

    def __init__(self, message):
        """Init."""
        self.message = message
        self.status_code = 400


class InternalError(Exception):
    """Internal error exception."""

    def __init__(self, message):
        """Init."""
        self.message = message
        self.status_code = 500
