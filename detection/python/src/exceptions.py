class Error(Exception):
    """Base class for other exceptions"""
    pass


class InvalidImageError(Error):
    """Raised when the image is invalid"""
    def __init__(self, e: Exception):
        super().__init__(str(e))
