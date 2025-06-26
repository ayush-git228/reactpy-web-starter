from pathlib import Path
import sys
import os

# Add the project root to sys.path so you can import from templates
sys.path.insert(0, str(Path(__file__).parent.parent))

from templates.shared.components.Button import Button
from reactpy import html

def test_button():
    button = Button("Click me")
    rendered = str(button)
    assert "Click me" in rendered
