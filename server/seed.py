
from datetime import date, timedelta

from server.app import app
from server.models import db, Workout, Exercise, WorkoutExercise


with app.app_context():
    db.create_all()

    if Exercise.query.count() == 0:
        exercises = [
            Exercise(
                name="Push Up",
                category="Strength",
                equipment_needed=False
            ),
            Exercise(
                name="Squat",
                category="Strength",
                equipment_needed=False
            ),
            Exercise(
                name="Running",
                category="Cardio",
                equipment_needed=False
            )
        ]

        db.session.add_all(exercises)

    if Workout.query.count() == 0:
        workouts = [
            Workout(
                date=date.today(),
                duration_minutes=45,
                notes="Upper body workout"
            ),
            Workout(
                date=date.today() - timedelta(days=1),
                duration_minutes=30,
                notes="Cardio and lower body workout"
            )
        ]

        db.session.add_all(workouts)

    db.session.commit()

    if WorkoutExercise.query.count() == 0:
        first_workout = Workout.query.first()
        second_workout = Workout.query.order_by(
            Workout.id.desc()
        ).first()

        push_up = Exercise.query.filter_by(name="Push Up").first()
        squat = Exercise.query.filter_by(name="Squat").first()
        running = Exercise.query.filter_by(name="Running").first()

        if first_workout and push_up:
            db.session.add(
                WorkoutExercise(
                    workout=first_workout,
                    exercise=push_up,
                    reps=12,
                    sets=3
                )
            )

        if first_workout and squat:
            db.session.add(
                WorkoutExercise(
                    workout=first_workout,
                    exercise=squat,
                    reps=15,
                    sets=3
                )
            )

        if second_workout and running:
            db.session.add(
                WorkoutExercise(
                    workout=second_workout,
                    exercise=running,
                    duration_seconds=1200
                )
            )

    db.session.commit()

    print("Database seeded successfully!")
