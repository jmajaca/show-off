class Error(Exception):
    """Base class for other exceptions"""
    pass


class ImageDimensionsTooLargeError(Error):
    """Raised when the image dimensions are too large"""
    def __init__(self, expected_max_height: int, actual_height: int, expected_max_width: int, actual_width: int):
        super().__init__(f'Image dimensions are too large, expected max height {expected_max_height}px got '
                         f'{actual_height}px, expected max width {expected_max_width}px got {actual_width}px')


class ImageByteSizeTooLargeError(Error):
    """Raised when the image byte size is too large"""
    pass
