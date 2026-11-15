import random
from flask import Blueprint, Flask, jsonify, request
from reservation import VALID_LABS, reservations

post_bp = Blueprint("post_bp", __name__)

REQUIRED_FIELDS = ("lab", "pc_number", "student_name", "date", "time_slot")


def create_unique_id():
    used_ids = {entry["reservation_id"] for entry in reservations}
    while True:
        candidate = f"RES-{random.randint(10000, 99999)}"
        if candidate not in used_ids:
            return candidate


def has_schedule_conflict(lab, pc_number, date, time_slot):
    for entry in reservations:
        if (
            entry["lab"] == lab
            and entry["pc_number"] == pc_number
            and entry["date"] == date
            and entry["time_slot"] == time_slot
        ):
            return True
    return False


@post_bp.route("/reservations", methods=["POST"])
def create_reservation():
    payload = request.get_json(silent=True) or {}

    for key in REQUIRED_FIELDS:
        if key not in payload or payload[key] in (None, ""):
            return jsonify({"error": f"Missing required field: {key}"}), 400

    if payload["lab"] not in VALID_LABS:
        return jsonify({"error": "Invalid lab name"}), 400

    pc_num = payload["pc_number"]
    if not isinstance(pc_num, int) or isinstance(pc_num, bool) or pc_num <= 0:
        return jsonify({"error": "Invalid field: pc_number must be a positive integer"}), 400

    if has_schedule_conflict(payload["lab"], pc_num, payload["date"], payload["time_slot"]):
        return jsonify({
            "error": (
                f"PC {pc_num} in {payload['lab']} "
                "is already reserved for that date and time slot"
            )
        }), 409

    created_record = {
        "reservation_id": create_unique_id(),
        "lab": payload["lab"],
        "pc_number": pc_num,
        "student_name": payload["student_name"],
        "date": payload["date"],
        "time_slot": payload["time_slot"],
    }
    reservations.append(created_record)

    return jsonify({
        "message": "Reservation created",
        "reservation": created_record,
    }), 201


if __name__ == "_main_":
    reservations.append({
        "reservation_id": "RES-62840",
        "lab": "Network-Lab",
        "pc_number": 4,
        "student_name": "Jose Rizal",
        "date": "2026-11-23",
        "time_slot": "08:00-10:00",
    })

    local_app = Flask(__name__)
    local_app.register_blueprint(post_bp)
    local_app.run(debug=True, port=5000)