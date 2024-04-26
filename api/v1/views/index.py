#!/usr/bin/python3

from flask import Flask
from flask import jsonify
from models import storage
from api.v1.views import app_views
import os


@app_views.route('/status')
def status():
    """Returns a JSON response with "status": "OK"."""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def count():
    """
    Retrieves the number of each objects by type
    """
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
