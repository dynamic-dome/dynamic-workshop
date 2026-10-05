"""
pytest test suite for access_control.py
Tests cover the intended behaviour of the tool.
"""

import json
import os
import pytest
import tempfile

import access_control


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def isolated_db(tmp_path, monkeypatch):
    """
    Redirect DB_FILE and LOG_DIR to a temp directory for every test
    so tests do not interfere with each other or the real database.
    """
    monkeypatch.setattr(access_control, "DB_FILE", str(tmp_path / "users.json"))
    monkeypatch.setattr(access_control, "LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setattr(
        access_control,
        "LOG_FILE",
        str(tmp_path / "logs" / "access.log"),
    )
    yield


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

class TestLoadDb:
    def test_returns_empty_structure_when_file_missing(self):
        db = access_control.load_db()
        assert db == {"users": []}

    def test_loads_existing_data(self, tmp_path, monkeypatch):
        db_path = tmp_path / "users.json"
        db_path.write_text(json.dumps({"users": ["alice", "bob"]}))
        monkeypatch.setattr(access_control, "DB_FILE", str(db_path))

        db = access_control.load_db()
        assert db["users"] == ["alice", "bob"]


# ---------------------------------------------------------------------------
# add_user
# ---------------------------------------------------------------------------

class TestAddUser:
    def test_add_new_user_returns_true(self):
        assert access_control.add_user("alice") is True

    def test_added_user_is_persisted(self):
        access_control.add_user("alice")
        db = access_control.load_db()
        assert "alice" in db["users"]

    def test_adding_duplicate_returns_false(self):
        access_control.add_user("alice")
        assert access_control.add_user("alice") is False

    def test_adding_duplicate_does_not_create_second_entry(self):
        access_control.add_user("alice")
        access_control.add_user("alice")
        db = access_control.load_db()
        assert db["users"].count("alice") == 1

    def test_add_multiple_users(self):
        access_control.add_user("alice")
        access_control.add_user("bob")
        access_control.add_user("charlie")
        assert access_control.list_users() == ["alice", "bob", "charlie"]


# ---------------------------------------------------------------------------
# remove_user
# ---------------------------------------------------------------------------

class TestRemoveUser:
    def test_remove_existing_user_returns_true(self):
        access_control.add_user("alice")
        assert access_control.remove_user("alice") is True

    def test_removed_user_is_no_longer_in_db(self):
        access_control.add_user("alice")
        access_control.remove_user("alice")
        assert "alice" not in access_control.list_users()

    def test_remove_nonexistent_user_returns_false(self):
        assert access_control.remove_user("ghost") is False

    def test_remove_does_not_affect_other_users(self):
        access_control.add_user("alice")
        access_control.add_user("bob")
        access_control.remove_user("alice")
        assert "bob" in access_control.list_users()


# ---------------------------------------------------------------------------
# check_access
# ---------------------------------------------------------------------------

class TestCheckAccess:
    def test_returns_true_for_known_user(self):
        access_control.add_user("alice")
        assert access_control.check_access("alice") is True

    def test_returns_false_for_unknown_user(self):
        assert access_control.check_access("nobody") is False

    def test_returns_false_after_user_removed(self):
        access_control.add_user("alice")
        access_control.remove_user("alice")
        assert access_control.check_access("alice") is False


# ---------------------------------------------------------------------------
# log_event
# ---------------------------------------------------------------------------

class TestLogEvent:
    def test_log_file_is_created(self):
        access_control.log_event("CHECK", "alice", success=True)
        assert os.path.exists(access_control.LOG_FILE)

    def test_log_entry_contains_username(self):
        access_control.log_event("ADD", "alice", success=True)
        with open(access_control.LOG_FILE) as f:
            content = f.read()
        assert "alice" in content

    def test_log_entry_contains_action(self):
        access_control.log_event("REMOVE", "bob", success=False)
        with open(access_control.LOG_FILE) as f:
            content = f.read()
        assert "REMOVE" in content

    def test_multiple_events_are_appended(self):
        access_control.log_event("ADD", "alice", success=True)
        access_control.log_event("CHECK", "bob", success=False)
        with open(access_control.LOG_FILE) as f:
            lines = f.readlines()
        assert len(lines) == 2
