"""Async typed client for the official Clash Royale REST API."""

from .client import Client
from .errors import *
from .errors import __all__ as _errors
from .models import *
from .models import __all__ as _models

__version__ = "1.0.0"
__all__ = ["Client", "__version__"] + _errors + _models
