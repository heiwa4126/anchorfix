from importlib.metadata import version

from ._core import PythonInfo, anchorfix

__all__ = ["anchorfix", "PythonInfo"]
__version__ = version(__package__ or __name__)  # Python 3.9+ only
