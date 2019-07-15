from flask import jsonify, Blueprint, request
from project.models import db

# Blueprint Declaration
admin = Blueprint(
    'admin',
    __name__
)

# Admin Endpoints
@admin.route('/sql', methods=['POST'])
def all_users():
    payload = request.get_json()
    if 'update' in payload and payload['update'] is not None:
        try: 
            query = payload['update']
            db.engine.execute(query)
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    if 'select' in payload:
        try:
            result = db.engine.execute(payload['select']).fetchall()
            res = [dict(r.items()) for r in result]
            return jsonify(res), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    if 'update' not in payload: 
        return jsonify({'error': 'please include a valid query'}), 400
    return jsonify({"success": "your query was processed"}), 200