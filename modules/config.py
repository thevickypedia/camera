import platform

system: str = platform.system()


class Settings:
    darwin: str = 'Darwin'
    windows: str = 'Windows'


settings = Settings()
