"""
users: create table
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        "CREATE TABLE users (id SERIAL PRIMARY KEY, firstname VARCHAR(255) NOT NULL)",
        "DROP TABLE users",
    )
]
