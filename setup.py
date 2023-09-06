"""setup file"""
from flask import Flask
from app import app


def setup_database(**kwargs):
    """setup database"""
    pass


def setup(app: Flask, **kwargs) -> None:
    """setup app"""
    setup_database(**kwargs)
