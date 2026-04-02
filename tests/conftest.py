from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture
def client():
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def restore_activities():
    activities_snapshot = deepcopy(app_module.activities)

    yield

    app_module.activities.clear()
    app_module.activities.update(activities_snapshot)


@pytest.fixture
def activity_name():
    return "Chess Club"


@pytest.fixture
def new_student_email():
    return "new.student@mergington.edu"


@pytest.fixture
def existing_student_email(activity_name):
    return app_module.activities[activity_name]["participants"][0]