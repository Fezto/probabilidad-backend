from crypt import methods

from flask import Blueprint, jsonify
from .models import Student, Asignature, StudentAsignature

api = Blueprint("main", __name__)

@api.route("/students", methods=["GET"])
def students():
    try:
        return Student.query.all()
    except Exception as e:
        return jsonify({'error': str(e)})

@api.route("/asignatures", methods=["GET"])
def asignatures():
    try:
        return Asignature.query.all()
    except Exception as e:
        return jsonify({'error': str(e)})

@api.route("/students_asignatures", methods=["GET"])
def students_asignatures():
    try:
        return StudentAsignature.query.all()
    except Exception as e:
        return jsonify({'error': str(e)})