# noinspection PyUnresolvedReferences
"""This is a space for custom exceptions and errors masking defaults with meaningful names.

>>> Exceptions

"""


class CameraError(SystemError):
    """Custom ``SystemError`` to indicate problems in describing connected video devices.

    >>> CameraError

    """


class UnsupportedOS(OSError):
    """Custom ``OSError`` raised when initiated in an unsupported operating system.

    >>> UnsupportedOS

    """
