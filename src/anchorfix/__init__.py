from importlib.metadata import version

from ._core import DuplicateIdError, process_html, process_html_file

__all__ = ["process_html", "process_html_file", "DuplicateIdError"]
__version__ = version(__package__ or __name__)  # Python 3.9+ only
