
import os

from flask import Flask, jsonify, request

try:
    from flask_migrate import Migrate
except ModuleNotFoundError:  # pragma: no cover - optional dependency in some environments
    Migrate = None

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server.config import Config
from server.models import db, Workout, Exercise, WorkoutExercise
from server.schemas import (
    workout_create_schema,
    exercise_create_schema,
    workout_exercise_create_schema,
    workout_schema,
    workouts_schema,
    exercise_schema,
    exercises_schema
)


app = Flask(__name__)

app.config.from_object(Config)

os.makedirs(app.instance_path, exist_ok=True)

db.init_app(app)
migrate = Migrate(app, db, directory="server/migrations")


@app.route("/")
def home():
    return jsonify({
        "message": "Workout Application API is running"
    }), 200


# GET /workouts
@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.order_by(Workout.id).all()
    return jsonify(workouts_schema.dump(workouts)), 200


# GET /workouts/<id>
@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    return jsonify(workout_schema.dump(workout)), 200


# POST /workouts
@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json(silent=True)

    try:
        workout_data = workout_create_schema.load(data or {})
        workout = Workout(**workout_data)

        db.session.add(workout)
        db.session.commit()

        return jsonify(workout_schema.dump(workout)), 201

    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    except (ValueError, IntegrityError) as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400


# DELETE /workouts/<id>
@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)

    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    db.session.delete(workout)
    db.session.commit()

    return jsonify({
        "message": "Workout deleted successfully"
    }), 200


# GET /exercises
@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.order_by(Exercise.id).all()
    return jsonify(exercises_schema.dump(exercises)), 200


# GET /exercises/<id>
@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404

    return jsonify(exercise_schema.dump(exercise)), 200


# POST /exercises
@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json(silent=True)

    try:
        exercise_data = exercise_create_schema.load(data or {})
        exercise = Exercise(**exercise_data)

        db.session.add(exercise)
        db.session.commit()

        return jsonify(exercise_schema.dump(exercise)), 201

    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    except (ValueError, IntegrityError) as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400


# DELETE /exercises/<id>
@app.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)

    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404

    db.session.delete(exercise)
    db.session.commit()

    return jsonify({
        "message": "Exercise deleted successfully"
    }), 200


# POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"]
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)

    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404

    data = request.get_json(silent=True)

    try:
        exercise_data = workout_exercise_create_schema.load(data or {})

        existing = WorkoutExercise.query.filter_by(
            workout_id=workout_id,
            exercise_id=exercise_id
        ).first()

        if existing:
            return jsonify({
                "error": "This exercise is already in the workout"
            }), 409

        workout_exercise = WorkoutExercise(
            workout=workout,
            exercise=exercise,
            **exercise_data
        )

        workout_exercise.validate_details()

        db.session.add(workout_exercise)
        db.session.commit()

        return jsonify({
            "message": "Exercise added to workout successfully",
            "workout_exercise": {
                "id": workout_exercise.id,
                "workout_id": workout_exercise.workout_id,
                "exercise_id": workout_exercise.exercise_id,
                "reps": workout_exercise.reps,
                "sets": workout_exercise.sets,
                "duration_seconds": workout_exercise.duration_seconds
            }
        }), 201

    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

    except (ValueError, IntegrityError) as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5555)
