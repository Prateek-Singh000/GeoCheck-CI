import subprocess
import pytest
import os
import time

GOLDEN_INPUT = "data/golden/cube_corners.csv"
GOLDEN_OUTPUT = "data/golden/cube_corners_expected.txt"
ENGINE = "aabb_engine.exe"

def run_engine(input_file, box_args=""):
    """Run the engine and return stdout lines, stderr, and return code"""
    cmd = f"{ENGINE} --input {input_file} {box_args}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    stdout_lines = result.stdout.strip().split("\n")
    # Filter only INSIDE/OUTPUT lines (ignore empty lines)
    stdout_lines = [line for line in stdout_lines if line in ("INSIDE", "OUTSIDE")]
    return stdout_lines, result.stderr, result.returncode

def test_golden_regression():
    """Compare engine output with golden expected output"""
    assert os.path.exists(ENGINE), f"Engine not found at {ENGINE}. Run compilation first."
    assert os.path.exists(GOLDEN_INPUT), f"Golden input not found at {GOLDEN_INPUT}"
    output_lines, stderr, rc = run_engine(GOLDEN_INPUT)
    
    with open(GOLDEN_OUTPUT, "r") as f:
        expected = [line.strip() for line in f.readlines() if line.strip()]
    
    assert output_lines == expected, f"Mismatch: got {output_lines}, expected {expected}"
    assert rc == 0, f"Engine returned error: {stderr}"

def test_engine_does_not_crash_on_corrupt():
    """Ensure corrupt file doesn't crash (may return error, but not hang)"""
    corrupt_file = "data/fuzz_inputs/corrupt.csv"
    if not os.path.exists(corrupt_file):
        pytest.skip("Corrupt file not found. Run fuzzer.py first.")
    start = time.time()
    _, stderr, rc = run_engine(corrupt_file)
    elapsed = time.time() - start
    assert elapsed < 5.0, f"Engine took too long ({elapsed:.2f}s) on corrupt file"
    # Return code can be 0 or 1; just ensure it finished
    assert rc in (0, 1), f"Unexpected return code {rc}"

def test_performance_not_regressed():
    """Check that engine processes 10k points in less than 2 seconds (adjust as needed)"""
    small_file = "data/fuzz_inputs/10k_points.csv"
    if not os.path.exists(small_file):
        pytest.skip("Run fuzzer.py first")
    start = time.perf_counter()
    _, _, rc = run_engine(small_file)
    elapsed = time.perf_counter() - start
    assert rc == 0, "Engine failed on small file"
    # Your benchmark showed ~211ms for 10k points, so 2 seconds is very safe
    assert elapsed < 2.0, f"Too slow: {elapsed:.2f}s for 10k points"