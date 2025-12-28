# event_routes.py
from flask import Blueprint, jsonify, request, abort
from models.event import Event
from utils.db import db
from flask_cors import CORS
from utils.decorators import *
import traceback
from sqlalchemy import or_, and_

event_bp = Blueprint('event', __name__)

# =========================
# 📌 FILTER EVENTS
# =========================
@event_bp.route('/filtre', methods=['POST'])
@check_expiration()
def filtre_event():
    try:
        data = request.get_json()
        valid_columns = {col.name for col in Event.__table__.columns}

        # Extract date range filters
        start_date = data.pop('start_datetime', None)
        end_date = data.pop('end_datetime', None)

        # Validate keys
        sent_keys = set(data.keys())
        invalid_keys = sent_keys - valid_columns
        if invalid_keys:
            abort(400, description=f"Champs invalides: {', '.join(invalid_keys)}")

        query = Event.query

        # Apply attribute filters
        for attr, value in data.items():
            query = query.filter(getattr(Event, attr) == value)

        # Date range filter
        if start_date and end_date:
            query = query.filter(
                and_(
                    Event.start_datetime >= start_date,
                    Event.end_datetime <= end_date
                )
            )

        events = query.all()
        events_list = [event.to_dict() for event in events]
        return jsonify(entries=events_list), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500
    finally:
        db.session.close()


# =========================
# 📌 GET DISTINCT COLUMN VALUES
# =========================
def extract_distinct_values(data):
    if not data:
        return {}
    columns = ["category", "city", "country", "organizer"]
    distinct_by_column = {col: set() for col in columns}
    for row in data:
        for col in columns:
            if row.get(col):
                distinct_by_column[col].add(row[col])
    return {col: list(values) for col, values in distinct_by_column.items()}


@event_bp.route('/colonnes', methods=['GET'])
def get_event_columns():
    try:
        events = Event.query.all()
        events_list = [event.to_dict() for event in events]
        columns_list = extract_distinct_values(events_list)

        return jsonify(columns_list), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500
    finally:
        db.session.close()


# =========================
# 📌 GET ALL EVENTS
# =========================
@event_bp.route('/', methods=['GET'])
def get_all_events():
    try:
        events = Event.query.all()
        events_list = [event.to_dict() for event in events]
        return jsonify(entries=events_list), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500
    finally:
        db.session.close()


# =========================
# 📌 GET SINGLE EVENT
# =========================
@event_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    try:
        event = Event.query.get(event_id)
        if event is None:
            return jsonify(message='Event non trouvé'), 404

        return jsonify(event=event.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500
    finally:
        db.session.close()


# =========================
# 📌 CREATE EVENT
# =========================
@event_bp.route('/', methods=['POST'])
@role_required("admin")
def create_event():
    try:
        data = request.get_json()
        valid_columns = {col.name for col in Event.__table__.columns}

        # Validate keys
        sent_keys = set(data.keys())
        invalid_keys = sent_keys - valid_columns
        if invalid_keys:
            abort(400, description=f"Champs invalides: {', '.join(invalid_keys)}")

        new_event = Event(**data)
        db.session.add(new_event)
        db.session.commit()

        return jsonify(message='Event ajouté avec succès'), 200
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify(error=str(e)), 500
    finally:
        db.session.close()


# =========================
# 📌 BULK UPLOAD EVENTS
# =========================
@event_bp.route('/upload', methods=['POST'])
def upload_events():
    try:
        datas = request.get_json()
        for data in datas:
            valid_columns = {col.name for col in Event.__table__.columns}
            sent_keys = set(data.keys())
            invalid_keys = sent_keys - valid_columns
            if invalid_keys:
                abort(400, description=f"Invalid fields: {', '.join(invalid_keys)}")

            new_event = Event(**data)
            db.session.add(new_event)

        db.session.commit()
        return jsonify(message="Liste d'événements ajoutée avec succès"), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500
    finally:
        db.session.close()


# =========================
# 📌 UPDATE EVENT
# =========================
@event_bp.route('/<int:event_id>', methods=['PUT'])
@role_required("admin")
def update_event(event_id):
    try:
        event = Event.query.get(event_id)
        if event is None:
            abort(404, description='Event non trouvé')

        data = request.get_json()
        valid_columns = {col.name for col in Event.__table__.columns}
        sent_keys = set(data.keys())
        invalid_keys = sent_keys - valid_columns
        if invalid_keys:
            abort(400, description=f"Champs invalides: {', '.join(invalid_keys)}")

        for key, value in data.items():
            setattr(event, key, value)

        db.session.commit()
        return jsonify(message='Event mis à jour avec succès'), 200
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify(error=str(e)), 500
    finally:
        db.session.close()


# =========================
# 📌 DELETE EVENT
# =========================
@event_bp.route('/<int:event_id>', methods=['DELETE'])
@role_required("admin")
def delete_event(event_id):
    try:
        event = Event.query.get(event_id)
        if event is None:
            abort(404, description='Event non trouvé')

        db.session.delete(event)
        db.session.commit()
        return jsonify(message='Event supprimé avec succès'), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500
    finally:
        db.session.close()


# =========================
# 📌 CORS + AUTH
# =========================
CORS(event_bp, origins='*', allow_headers=["Content-Type"])

@event_bp.before_request
@loggedin()
def handle_preflight():
    if request.method == 'OPTIONS':
        response = event_bp.make_default_options_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE')
        return response
