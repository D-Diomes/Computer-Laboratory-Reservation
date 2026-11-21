from flask import Blueprint, jsonify, request
from reservation import reservations, VALID_LABS

put_bp = Blueprint("put_bp", __name__)

@put_bp.route("/reservations/<string:reservation_id>", methods=["PUT"])
def update_reservation(reservation_id):
    target = None
    for reservation in reservations:
        if reservation["reservation_id"] == reservation_id:
            target = reservation
            break

    if target is None:
        return jsonify({"error": "Reservation not found"}), 404

    data = request.get_json(silent=True) or {}
    required_fields = ["lab", "pc_number", "student_name", "date", "time_slot"]

    for field in required_fields:
        if field not in data or data[field] in (None, ""):
            return jsonify({"error": f"Missing required field: {field}"}), 400

    if data["lab"] not in VALID_LABS:
        return jsonify({"error": "Invalid lab name"}), 400

    if (
        not isinstance(data["pc_number"], int)
        or isinstance(data["pc_number"], bool)
        or data["pc_number"] <= 0
    ):
        return jsonify({"error": "Invalid field: pc_number must be a positive integer"}), 400

    for existing in reservations:
        if existing is target:
            continue  # a reservation must not conflict with itself
        if (
            existing["lab"] == data["lab"]
            and existing["pc_number"] == data["pc_number"]
            and existing["date"] == data["date"]
            and existing["time_slot"] == data["time_slot"]
        ):
            return (
                jsonify(
                    {
                        "error": (
                            f"PC {data['pc_number']} in {data['lab']} "
                            "is already reserved for that date and time slot"
                        )
                    }
                ),
                409,
            )

    target["lab"] = data["lab"]
    target["pc_number"] = data["pc_number"]
    target["student_name"] = data["student_name"]
    target["date"] = data["date"]
    target["time_slot"] = data["time_slot"]

    return jsonify(target), 200
