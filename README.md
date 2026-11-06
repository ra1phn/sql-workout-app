
# Workout Application Backend

A REST API built with Python, Flask and SQLAlchemy for managing workouts and reusable exercises.

## Features

- Create, view and delete workouts.
- Create, view and delete exercises.
- Add reusable exercises to workouts.
- Track exercise repetitions, sets and duration.
- Validate incoming data using Marshmallow.
- Enforce database constraints and model validations.
- Serialize nested workout and exercise relationships.
- Automatically delete associated records when a workout or exercise is deleted.

## Technologies

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- SQLite
- Marshmallow
- Pipenv

## Project Structure

```text
sql-workout-app/
├── server/
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── schemas.py
│   ├── seed.py
│   └── migrations/
├── tests/
├── Pipfile
├── README.md
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd sql-workout-app
```

Install dependencies:

```bash
pipenv install
```

Activate the virtual environment:

```bash
pipenv shell
```

## Database Setup

Initialise migrations:

```bash
flask --app server.app db init
```

Create the initial migration:

```bash
flask --app server.app db migrate -m "Initial migration"
```

Apply migrations:

```bash
flask --app server.app db upgrade
```

Seed the database:

```bash
python -m server.seed
```

## Running the Application

```bash
python -m server.app
```

The API runs at:

```text
http://127.0.0.1:5555
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | View a workout and its exercises |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | View an exercise and its workouts |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

## Example Requests

### Create a Workout

POST `/workouts`

```json
{
    "date": "2026-11-06",
    "duration_minutes": 45,
    "notes": "Upper body workout"
}
```

### Create an Exercise

POST `/exercises`

```json
{
    "name": "Push Up",
    "category": "Strength",
    "equipment_needed": false
}
```

### Add an Exercise to a Workout

POST `/workouts/1/exercises/1/workout_exercises`

```json
{
    "reps": 12,
    "sets": 3
}
```

For a timed exercise:

```json
{
    "duration_seconds": 120
}
```

### Delete a Workout

DELETE `/workouts/1`

### Delete an Exercise

DELETE `/exercises/1`

## Validations

The application includes:

- Database constraints for required fields, unique records and positive numeric values.
- Model validations for exercise names, categories, dates and workout details.
- Marshmallow schema validations for incoming request data.
- Validation requiring reps and sets together, or a duration for an exercise association.

## Database Relationships

- A workout has many workout exercises.
- An exercise has many workout exercises.
- A workout has many exercises through workout exercises.
- An exercise has many workouts through workout exercises.

## Author

Ralph Njuguna