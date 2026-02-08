import subprocess
import sys
from pathlib import Path


def test_hello_output():
    """Test that hello.py prints 'Hello, World!'"""
    # Get the project root (parent of tests/)
    project_root = Path(__file__).parent.parent

    result = subprocess.run(
        [sys.executable, "hello.py"],
        capture_output=True,
        text=True,
        cwd=project_root
    )
    assert result.returncode == 0, f"Script failed with: {result.stderr}"
    assert "Hello, World!" in result.stdout, f"Expected 'Hello, World!' but got: {result.stdout}"
