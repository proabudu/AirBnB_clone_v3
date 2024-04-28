#!/usr/bin/python3

"""Init file for views module"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


# Imports from subfolders go here
from . import views.index  # Import from views.index subfolder
from . import views.states  # Import from views.states subfolder
