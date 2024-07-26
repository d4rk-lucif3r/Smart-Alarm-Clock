"""This is the main Flask application that runs the web server."""

import os
from flask import Flask, jsonify

app = Flask(__name__)

# Fetching the secret key from environment variables
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret')

@app.route('/')
def home():
    """Home route that returns a welcome message."""
    return jsonify({"message": "Welcome to the Flask Application!"})

if __name__ == '__main__':
    app.run(debug=True)