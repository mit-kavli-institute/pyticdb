"""Top-level package for PyTICDB."""
from .query import query_by_id, query_by_loc, query_raw

__all__ = ["query_by_id", "query_by_loc", "query_raw"]
__author__ = """William Fong"""
__email__ = "willfong@mit.edu"
__version__ = "0.1.1"
