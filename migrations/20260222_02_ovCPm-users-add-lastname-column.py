"""
users: add lastname column
"""

from yoyo import step

__depends__ = {'20260222_01_JirdZ-users-create-table'}

steps = [
    step(
        "ALTER TABLE users ADD COLUMN lastname VARCHAR(255)",
        "ALTER TABLE users DROP COLUMN lastname",
    )
]
