import os
from flask import Flask

app = Flask(__name__)

# Load secret key from environment variables
app.secret_key = os.getenv('SECRET_KEY')

if __name__ == '__main__':
    app.run(debug=True)