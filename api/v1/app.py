#!/usr/bin/python3

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os

# Create an instance of Flask
app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def close_storage(exception):
    # # Call storage.close() to release resources.
    storage.close()


if __name__ == "__main__":

    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    app.run(host=host, port=port, threaded=True)
