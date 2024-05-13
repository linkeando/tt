import os

from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from src.infrastructure.docs.api_loader import OpenApiLoader


class FlaskApp:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_app()
        return cls._instance

    def _init_app(self):
        self.app = Flask(__name__)
        self._load_env()
        self._init_swagger()
        self._enable_cors()
        #SocketManager(self._enable_socket())

    @staticmethod
    def _load_env():
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)

    def _init_swagger(self):
        base_directory = os.path.abspath(os.path.dirname(__file__))
        docs_directory = os.path.join(base_directory, '../', 'docs')
        swagger_loader = OpenApiLoader(docs_directory)
        swagger_config = swagger_loader.load_yaml_files()
        self.app.config['SWAGGER'] = {'openapi': '3.0.0'}
        return Swagger(self.app, config=swagger_config, merge=True)

    def _enable_cors(self):
        CORS(self.app)

    def _enable_socket(self):
        self.app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        return SocketIO(self.app, cors_allowed_origins='*', allow_unsafe_werkzeug=True)

    def create_app(self):
        return self.app
