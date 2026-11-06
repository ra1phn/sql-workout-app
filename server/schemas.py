
from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class WorkoutCreateSchema(Schema):
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(
        required=True,
        validate=validate.Range(min=1)
    )
    notes = fields.String(
        allow_none=True,
        validate=validate.Length(max=1000)
    )


class ExerciseCreateSchema(Schema):
    name = fields.String(
        required=True,
        validate=[
            validate.Length(min=1, max=100),
            validate.Regexp(r".*\S.*", error="Name cannot be empty")
        ]
    )
    category = fields.String(
        required=True,
        validate=[
            validate.Length(min=1, max=50),
            validate.Regexp(r".*\S.*", error="Category cannot be empty")
        ]
    )
    equipment_needed = fields.Boolean(required=True)


class WorkoutExerciseCreateSchema(Schema):
    reps = fields.Integer(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1)
    )
    sets = fields.Integer(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1)
    )
    duration_seconds = fields.Integer(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1)
    )

    @validates_schema
    def validate_exercise_details(self, data, **kwargs):
        reps = data.get("reps")
        sets = data.get("sets")
        duration = data.get("duration_seconds")

        if (reps is None) != (sets is None):
            raise ValidationError(
                "Reps and sets must be provided together."
            )

        if reps is None and duration is None:
            raise ValidationError(
                "Provide reps and sets, or a duration."
            )


class ExerciseSummarySchema(Schema):
    id = fields.Integer()
    name = fields.String()
    category = fields.String()
    equipment_needed = fields.Boolean()


class WorkoutSummarySchema(Schema):
    id = fields.Integer()
    date = fields.Date()
    duration_minutes = fields.Integer()
    notes = fields.String(allow_none=True)


class WorkoutExerciseForWorkoutSchema(Schema):
    id = fields.Integer()
    reps = fields.Integer(allow_none=True)
    sets = fields.Integer(allow_none=True)
    duration_seconds = fields.Integer(allow_none=True)
    exercise = fields.Nested(ExerciseSummarySchema)


class WorkoutExerciseForExerciseSchema(Schema):
    id = fields.Integer()
    reps = fields.Integer(allow_none=True)
    sets = fields.Integer(allow_none=True)
    duration_seconds = fields.Integer(allow_none=True)
    workout = fields.Nested(WorkoutSummarySchema)


class WorkoutSchema(Schema):
    id = fields.Integer()
    date = fields.Date()
    duration_minutes = fields.Integer()
    notes = fields.String(allow_none=True)
    workout_exercises = fields.Nested(
        WorkoutExerciseForWorkoutSchema,
        many=True
    )


class ExerciseSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    category = fields.String()
    equipment_needed = fields.Boolean()
    workout_exercises = fields.Nested(
        WorkoutExerciseForExerciseSchema,
        many=True
    )


workout_create_schema = WorkoutCreateSchema()
exercise_create_schema = ExerciseCreateSchema()
workout_exercise_create_schema = WorkoutExerciseCreateSchema()

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
