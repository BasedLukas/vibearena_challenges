"""
Pytest tests for the performance takehome challenge.
Tests verify correctness and measure cycle count performance.
"""

import os
import sys
from functools import lru_cache

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frozen_problem import (
    Machine,
    build_mem_image,
    reference_kernel2,
    Tree,
    Input,
    N_CORES,
)
from perf_takehome import KernelBuilder


@lru_cache(maxsize=None)
def kernel_builder(forest_height: int, n_nodes: int, batch_size: int, rounds: int):
    """Cached kernel builder to avoid rebuilding for repeated tests."""
    kb = KernelBuilder()
    kb.build_kernel(forest_height, n_nodes, batch_size, rounds)
    return kb


def run_kernel_test(forest_height: int, rounds: int, batch_size: int) -> int:
    """Run kernel and return cycle count. Raises AssertionError if incorrect."""
    forest = Tree.generate(forest_height)
    inp = Input.generate(forest, batch_size, rounds)
    mem = build_mem_image(forest, inp)

    kb = kernel_builder(forest.height, len(forest.values), len(inp.indices), rounds)

    machine = Machine(mem, kb.instrs, kb.debug_info(), n_cores=N_CORES)
    machine.enable_pause = False
    machine.enable_debug = False
    machine.run()

    for ref_mem in reference_kernel2(mem):
        pass

    inp_values_p = ref_mem[6]
    assert (
        machine.mem[inp_values_p : inp_values_p + len(inp.values)]
        == ref_mem[inp_values_p : inp_values_p + len(inp.values)]
    ), "Incorrect output values"

    return machine.cycle


BASELINE = 147734


@lru_cache(maxsize=None)
def get_cycles() -> int:
    """Get cycle count, cached. Returns 2x baseline if correctness fails."""
    try:
        return run_kernel_test(10, 16, 256)
    except AssertionError:
        return BASELINE * 2


# =============================================================================
# Correctness Tests
# =============================================================================

def test_kernel_correctness():
    """Verify kernel produces correct output across multiple runs."""
    for _ in range(8):
        run_kernel_test(10, 16, 256)


# =============================================================================
# Performance Tests - Cycle Count Thresholds
# =============================================================================

def test_beats_baseline():
    """Solution must beat the baseline cycle count."""
    cycles = get_cycles()
    assert cycles < BASELINE, f"Got {cycles} cycles, need < {BASELINE}"


def test_starter_code_level():
    """Beat the starter code performance level (18532 cycles)."""
    cycles = get_cycles()
    assert cycles < 18532, f"Got {cycles} cycles, need < 18532"


def test_good_solution():
    """Achieve a good solution (~2164 cycles)."""
    cycles = get_cycles()
    assert cycles < 2164, f"Got {cycles} cycles, need < 2164"


def test_great_solution():
    """Achieve a great solution (~1790 cycles)."""
    cycles = get_cycles()
    assert cycles < 1790, f"Got {cycles} cycles, need < 1790"


def test_excellent_solution():
    """Achieve an excellent solution (~1579 cycles)."""
    cycles = get_cycles()
    assert cycles < 1579, f"Got {cycles} cycles, need < 1579"


def test_outstanding_solution():
    """Achieve an outstanding solution (~1548 cycles)."""
    cycles = get_cycles()
    assert cycles < 1548, f"Got {cycles} cycles, need < 1548"


def test_exceptional_solution():
    """Achieve an exceptional solution (~1487 cycles)."""
    cycles = get_cycles()
    assert cycles < 1487, f"Got {cycles} cycles, need < 1487"


def test_optimal_solution():
    """Achieve near-optimal solution (~1363 cycles)."""
    cycles = get_cycles()
    assert cycles < 1363, f"Got {cycles} cycles, need < 1363"
