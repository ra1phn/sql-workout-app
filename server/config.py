import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        BASE_DIR, "instance", "workouts.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    