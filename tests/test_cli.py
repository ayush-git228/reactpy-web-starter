import pytest
from unittest.mock import patch, MagicMock
from reactpy_web_starter.cli import read_requirements

def test_read_requirements(tmp_path):
    requirements = tmp_path / "requirements.txt"
    requirements.write_text("reactpy\npandas\n# comment\n\n")
    assert read_requirements(requirements) == ["reactpy", "pandas"]
