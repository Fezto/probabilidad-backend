from flask import Blueprint, jsonify, request

from . import db
from .models import Student, Asignature, StudentAsignature
from .probability import asignature_probability, period_probability

api = Blueprint("main", __name__)

################################
# * Rutas para los estudiantes
################################
@api.route("/students", methods=["GET"])
def students():
    try:
        students = Student.query.all()
        result = []

        for student in students:
            # Obtenemos las asignaturas del estudiante
            asignatures = StudentAsignature.query.filter_by(student_id=student.id).all()

            # Preparamos las notas para la función de probabilidad
            materias = [
                [
                    asignature.first_partial,
                    asignature.second_partial,
                    asignature.third_partial,
                ]
                for asignature in asignatures
            ]

            # Calculamos la probabilidad
            general_probability, _ = period_probability(materias)

            # Agregamos el resultado
            result.append({
                "id": student.id,
                "name": student.name,
                "ap": student.ap,
                "am": student.am,
                "period": student.period,
                "probability": general_probability
            })

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

@api.route("/student/<int:id>", methods=["GET"])
def student(id):
    try:
        return Student.query.filter_by(id=id).all()
    except Exception as e:
        return jsonify({'error': str(e)})


@api.route("/student", methods=["POST"])
def add_student():
    try:
        data = request.json
        new_student = Student(
            name=data['name'],
            ap=data['ap'],
            am=data['am'],
            period=data['period']
        )
        db.session.add(new_student)
        db.session.commit()
        return jsonify({"message": "Estudiante agregado correctamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@api.route("/student/<int:id>", methods=["DELETE"])
def delete_student(id):
    try:
        student = Student.query.get(id)
        if student:
            db.session.delete(student)
            db.session.commit()
            return jsonify({"message": "Estudiante eliminado correctamente"}), 200
        return jsonify({"message": "Estudiante no encontrado"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


################################
# * Rutas para las materias
################################
@api.route("/asignatures", methods=["GET"])
def asignatures():
    try:
        return Asignature.query.all()
    except Exception as e:
        return jsonify({'error': str(e)})


# Rutas para las materias de los estudiantes
################################
# * Rutas para los materias de cada estudiante
################################

@api.route("/students_asignatures/<int:id>", methods=["GET"])
def students_asignatures(id):
    try:
        # Consultamos todas las asignaturas del estudiante con el id indicado
        subjects = StudentAsignature.query.filter_by(student_id=id).all()
        result = []
        for s in subjects:
            # Armamos la lista de parciales a partir del registro
            partials = [s.first_partial, s.second_partial, s.third_partial]
            prob = asignature_probability(partials)

            result.append({
                'id': s.id,
                'student_name': s.student.name,
                'asignature_name': s.asignature.name,
                'first_partial': s.first_partial,
                'second_partial': s.second_partial,
                'third_partial': s.third_partial,
                'average': s.average,
                'final_flag': s.final_flag,
                'probability': round(prob, 4)  # Ejemplo: 0.4500
            })
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
@api.route("/student_asignature", methods=["POST"])
def add_student_asignature():
    try:
        data = request.json
        new_record = StudentAsignature(
            student_id=data['student_id'],
            asignature_id=data['asignature_id']
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({"message": "Asignatura añadida al estudiante"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@api.route("/student_asignature/<int:id>", methods=["DELETE"])
def delete_student_asignature(id):
    try:
        record = StudentAsignature.query.get(id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return jsonify({"message": "Asignatura eliminada del estudiante"}), 200
        return jsonify({"message": "No se encontró la asignatura para el estudiante"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500





@api.route("/students_asignatures", methods=["PUT"])
def update_student_asignatures():
    data = request.json
    student_asignature_id = data.get('id')
    first_partial = data.get('first_partial')
    second_partial = data.get('second_partial')
    third_partial = data.get('third_partial')

    grade = StudentAsignature.query.get(student_asignature_id)

    grade.first_partial = first_partial
    grade.second_partial = second_partial
    grade.third_partial = third_partial
    grade.average = (first_partial + second_partial + third_partial) / 3
    grade.final_flag = True if (first_partial >= 70 and second_partial >= 70 and third_partial >= 70) else False
    grade.probability = asignature_probability([first_partial, second_partial, third_partial])

    db.session.commit()
    return jsonify({"message": "Notas actualizadas correctamente"}), 200


