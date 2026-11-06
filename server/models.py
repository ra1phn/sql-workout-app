
from datetime import date

from flask_sqlalchemy import SQLAlchemy  # type: ignore[import-not-found]
from sqlalchemy import CheckConstraint, UniqueConstraint  # type: ignore[import-not-found]
from sqlalchemy.orm import validates  # type: ignore[import-not-found]


db = SQLAlchemy()


class Workout(db.Model):
    __tablename__ = "workouts"

    __table_args__ = (
        CheckConstraint(
            "duration_minutes > 0",
            name="check_workout_duration"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )

    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        viewonly=True,
        overlaps="workout_exercises,workout,exercise"
    )

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ValueError("Workout duration must be a positive integer")
        return value

    @validates("date")
    def validate_date(self, key, value):
        if not isinstance(value, date):
            raise ValueError("Workout date must be a valid date")
        return value


class Exercise(db.Model):
    __tablename__ = "exercises"

    __table_args__ = (
        UniqueConstraint("name", name="unique_exercise_name"),
        CheckConstraint(
            "length(trim(name)) > 0",
            name="check_exercise_name"
        ),
        CheckConstraint(
            "length(trim(category)) > 0",
            name="check_exercise_category"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        viewonly=True,
        overlaps="workout_exercises,workout,exercise"
    )

    @validates("name")
    def validate_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Exercise name cannot be empty")
        if len(value) > 100:
            raise ValueError("Exercise name cannot exceed 100 characters")
        return value.strip()

    @validates("category")
    def validate_category(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Exercise category cannot be empty")
        if len(value) > 50:
            raise ValueError("Category cannot exceed 50 characters")
        return value.strip()

    @validates("equipment_needed")
    def validate_equipment(self, key, value):
        if not isinstance(value, bool):
            raise ValueError("Equipment needed must be true or false")
        return value


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    __table_args__ = (
        UniqueConstraint(
            "workout_id",
            "exercise_id",
            name="unique_workout_exercise"
        ),
        CheckConstraint(
            "reps IS NULL OR reps > 0",
            name="check_positive_reps"
        ),
        CheckConstraint(
            "sets IS NULL OR sets > 0",
            name="check_positive_sets"
        ),
        CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds > 0",
            name="check_positive_exercise_duration"
        ),
        CheckConstraint(
            "(reps IS NULL AND sets IS NULL) OR "
            "(reps IS NOT NULL AND sets IS NOT NULL)",
            name="check_reps_and_sets_together"
        ),
        CheckConstraint(
            "(reps IS NOT NULL AND sets IS NOT NULL) OR "
            "duration_seconds IS NOT NULL",
            name="check_exercise_details"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id", ondelete="CASCADE"),
        nullable=False
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id", ondelete="CASCADE"),
        nullable=False
    )

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship(
        "Workout",
        back_populates="workout_exercises"
    )

    exercise = db.relationship(
        "Exercise",
        back_populates="workout_exercises"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validate_details()

    @validates("reps", "sets", "duration_seconds")
    def validate_positive_values(self, key, value):
        if value is not None:
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                raise ValueError(f"{key} must be a positive integer")
        return value

    def validate_details(self):
        if self.reps is None and self.sets is None and self.duration_seconds is None:
            raise ValueError("Provide reps and sets, or a duration")

        if (self.reps is None) != (self.sets is None) and self.duration_seconds is None:
            raise ValueError("Reps and sets must be provided together")
