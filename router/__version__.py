from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("njupt-suan-api")
except PackageNotFoundError:
    __version__ = "dev"
