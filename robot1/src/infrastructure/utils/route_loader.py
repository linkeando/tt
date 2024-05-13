import pkgutil
import importlib
import logging
from flask import Blueprint


class RouteLoader:
    def __init__(self, app, package_name):
        """
        Inicializa el RouteManager.

        Args:
            app: La aplicación Flask.
            package_name: El nombre del paquete donde se encuentran los módulos de las rutas.
        """
        self.app = app
        self.package_name = package_name
        self.routes_without_prefix = ['home']
        self.logger = logging.getLogger(__name__)

    def register_routes(self):
        """
        Registra las rutas definidas en los módulos del paquete.
        """
        try:
            package = importlib.import_module(self.package_name)
            for _, module_name, _ in pkgutil.iter_modules(package.__path__):
                module = importlib.import_module(f"{self.package_name}.{module_name}")
                if hasattr(module, "init_app") and callable(getattr(module, "init_app")):
                    blueprint = Blueprint(module_name, __name__)
                    module.init_app(blueprint)
                    url_prefix = f"/{module_name}" if module_name not in self.routes_without_prefix else ""
                    self.app.register_blueprint(blueprint, url_prefix=url_prefix)
                else:
                    self.logger.warning(f"El módulo {module_name} no tiene el método 'init_app'.")
        except ImportError as e:
            self.logger.error(f"Error al importar el paquete {self.package_name}: {e}")
        except Exception as e:
            self.logger.error(f"Error al registrar rutas: {e}")
