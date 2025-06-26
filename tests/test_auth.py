import pytest
from pathlib import Path
import sys
import os
sys.path.insert(0, str(Path(__file__).parent.parent))
from templates.auth.backend.auth import register_user, verify_password

def test_register_and_verify_user(tmp_path, monkeypatch):
    import templates.auth.backend.auth as auth
    monkeypatch.setattr(auth, "USER_DB_PATH", tmp_path / "users.json")
    assert register_user("testuser", "testpass") is True
    assert verify_password("testuser", "testpass") is True
    assert verify_password("testuser", "wrongpass") is False
