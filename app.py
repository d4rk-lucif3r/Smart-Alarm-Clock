from flask import Flask
from config import DevelopmentConfig

def create_app(config_class=DevelopmentConfig):
    """Create and configure the app."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register blueprints and setup other app components here

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()