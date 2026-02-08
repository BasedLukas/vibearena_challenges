"""
Pytest tests for the droppedaneuralnet puzzle.
Verifies the solution permutation matches the expected hash.
"""

import hashlib
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from solution import SOLUTION

EXPECTED_HASH = "093be1cf2d24094db903cbc3e8d33d306ebca49c6accaa264e44b0b675e7d9c4"


def test_solution_format():
    """Verify solution is a valid permutation of 0-96."""
    assert len(SOLUTION) == 97, f"Expected 97 numbers, got {len(SOLUTION)}"
    assert set(SOLUTION) == set(range(97)), "Solution must be a permutation of 0-96"


def test_solution_correct():
    """Verify solution matches the expected hash."""
    canonical = ','.join(str(x) for x in SOLUTION)
    solution_hash = hashlib.sha256(canonical.encode()).hexdigest()
    assert solution_hash == EXPECTED_HASH, f"Incorrect. Your hash: {solution_hash[:16]}..."
