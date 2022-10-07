import platform
from enum import Enum

system: str = platform.system()


class Settings(str, Enum):
    """Settings used by camera.py.

    >>> Settings

    """

    darwin: str = 'Darwin'
    windows: str = 'Windows'


settings = Settings
