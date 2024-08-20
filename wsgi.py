from app import create_app
from config import ProductionConfig

app = create_app(config_class=ProductionConfig)