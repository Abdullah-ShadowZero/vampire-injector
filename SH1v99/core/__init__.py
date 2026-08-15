"""
core/__init__.py - Core Package
Contains the main payload building and encryption engine
"""

from .payload_builder import PayloadBuilder

__all__ = ['PayloadBuilder']
__version__ = '4.0'