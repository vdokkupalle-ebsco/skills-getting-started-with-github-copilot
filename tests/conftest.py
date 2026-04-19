import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module

_original_activities = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = copy.deepcopy(_original_activities)


@pytest.fixture
def client():
    return TestClient(app_module.app)
