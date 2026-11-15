from flask import Blueprint, Flask, jsonify
from reservation import reservations

delete_bp = Blueprint("delete_bp", __name__)


@delete_bp.route("/reservations/<string:reservation_id>", methods=["DELETE"])
def cancel_reservation(reservation_id):
    for idx in range(len(reservations)):
        if reservations[idx]["reservation_id"] == reservation_id:
            reservations.pop(idx)
            return jsonify({"message": f"Reservation {reservation_id} deleted"}), 200

    return jsonify({"error": "Reservation not found"}), 404


# Erik's branch demo runner
if __name__ == "__main__":
    reservations.extend([
        {
            "reservation_id": "RES-77310",
            "lab": "Basic-Lab",
            "pc_number": 2,
            "student_name": "Carlo Mendoza",
            "date": "2026-11-22",
            "time_slot": "10:00-12:00",
        },
        {
            "reservation_id": "RES-88412",
            "lab": "Network-Lab",
            "pc_number": 9,
            "student_name": "Sofia Lim",
            "date": "2026-11-24",
            "time_slot": "15:00-17:00",
        },
    ])

    runner_app = Flask(__name__)
    runner_app.register_blueprint(delete_bp)
    runner_app.run(debug=True, port=5000)