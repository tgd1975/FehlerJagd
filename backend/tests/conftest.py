"""Test-Setup: temporäre DB + Stub-Scoring, VOR jedem App-Import gesetzt."""

import os
import tempfile

# Muss vor dem Import von app.config gesetzt sein (Settings liest Env beim Laden).
_tmp_db = os.path.join(tempfile.gettempdir(), "fehlerjagd_test.db")
if os.path.exists(_tmp_db):
    os.remove(_tmp_db)
os.environ.setdefault("FJ_DB_URL", f"sqlite:///{_tmp_db}")
os.environ.setdefault("FJ_SCORING", "stub")

import pytest  # noqa: E402

from app.db import init_db  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _db():
    init_db()
    yield


@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    from app.main import app
    with TestClient(app) as c:
        yield c
