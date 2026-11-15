from flask import Blueprint, Flask, jsonify, request
from reservation import VALID_LABS, reservations

get_bp = Blueprint("get_bp", __name__)