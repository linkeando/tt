from src.infrastructure.utils.route_loader import RouteLoader
from src.infrastructure.utils.app import FlaskApp

app = FlaskApp().app
route_manager = RouteLoader(app, "src.infrastructure.routes").register_routes()

if __name__ == '__main__':
    app.run(debug=True, port=8080)
