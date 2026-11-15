from flask import Blueprint, Flask, jsonify, request
from reservation import VALID_LABS, reservations

get_bp = Blueprint("get_bp", __name__)


@get_bp.route("/reservations", methods=["GET"])
def get_all_reservations():
    selected_lab = request.args.get("lab")

    if selected_lab is not None:
        if selected_lab not in VALID_LABS:
            return jsonify({"error": "Invalid lab name"}), 400

        matching_records = [
            item for item in reservations if item["lab"] == selected_lab
        ]
        return jsonify({
            "count": len(matching_records),
            "reservations": matching_records,
        }), 200

    return jsonify({
        "count": len(reservations),
        "reservations": reservations,
    }), 200


def find_reservation(res_id):
    for record in reservations:
        if record["reservation_id"] == res_id:
            return record
    return None


@get_bp.route("/reservations/<string:reservation_id>", methods=["GET"])
def get_single_reservation(reservation_id):
    record = find_reservation(reservation_id)
    if record is None:
        return jsonify({"error": "Reservation not found"}), 404
    return jsonify(record), 200


if __name__ == "__main__":
    reservations.append({
        "reservation_id": "RES-30914",
        "lab": "Basic-Lab",
        "pc_number": 10,
        "student_name": "Maria Clara",
        "date": "2026-11-22",
        "time_slot": "14:00-16:00",
    })

    test_app = Flask(__name__)
    test_app.register_blueprint(get_bp)
    test_app.run(debug=True, port=5000)