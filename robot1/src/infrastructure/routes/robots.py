from flask import Blueprint, jsonify

from src.application.core.scrapping.scrapping_service import ScrapingService

robots_bp = Blueprint('robots', __name__)


@robots_bp.route('/curp', methods=['POST'])
def home_page():
    curp_data = ScrapingService().get_curp_data('NALE010526HCSNPDA6')
    if curp_data:
        return jsonify({'CURP': curp_data})
    else:
        return jsonify({'error': 'Error al obtener los datos de la CURP'}), 500


def init_app(app):
    app.register_blueprint(robots_bp)
