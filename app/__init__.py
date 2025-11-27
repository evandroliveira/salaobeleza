from app.models.db import db
import importlib

__all__ = ['db']


def __getattr__(name: str):
	"""Lazily resolve attributes from the top-level `run` module.

	This allows WSGI servers configured with `gunicorn app:app` to
	import the `app` object even though the main Flask factory lives
	in `run.py`. We avoid importing `run` at package import time to
	reduce circular import risks; the import happens only when the
	attribute is requested (PEP 562).
	"""
	if name == 'app':
		mod = importlib.import_module('run')
		return getattr(mod, 'app')
	raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
