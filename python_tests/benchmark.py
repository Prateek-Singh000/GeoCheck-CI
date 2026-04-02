import subprocess
import time
import psutil
import csv
import matplotlib.pyplot as plt
import os
import platform

if platform.system() == "Windows":
    ENGINE = "aabb_engine.exe"
else:
    ENGINE = "./aabb_engine"

def benchmark_engine(csv_file, box_args=""):
    cmd = f"{ENGINE} --input {csv_file} {box_args}"
    process = psutil.Process()
    mem_before = process.memory_info().rss / 1024 / 1024
    start_time = time.perf_counter()
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    end_time = time.perf_counter()
    mem_after = process.memory_info().rss / 1024 / 1024
    mem_used = max(0, mem_after - mem_before)
    elapsed_ms = (end_time - start_time) * 1000
    point_count = 0
    for line in result.stderr.splitlines():
        if "Processed" in line:
            parts = line.split()
            try:
                point_count = int(parts[1])
            except:
                pass
    return {
        "file": os.path.basename(csv_file),
        "points": point_count,
        "time_ms": elapsed_ms,
        "memory_mb": mem_used,
        "returncode": result.returncode,
    }

def run_benchmark_suite():
    results = []
    sizes = ["10k_points.csv", "100k_points.csv", "1M_points.csv"]
    for size in sizes:
        path = f"data/fuzz_inputs/{size}"
        if os.path.exists(path):
            print(f"Benchmarking {size}...")
            res = benchmark_engine(path)
            results.append(res)
            print(f"  Time: {res['time_ms']:.2f} ms, Memory: {res['memory_mb']:.2f} MB")
    corrupt_path = "data/fuzz_inputs/corrupt.csv"
    if os.path.exists(corrupt_path):
        print(f"Testing corrupt file {corrupt_path}...")
        res = benchmark_engine(corrupt_path)
        print(f"  Return code: {res['returncode']}")
        results.append(res)
    with open("benchmark_output.csv", "w", newline="") as f:
        fieldnames = ["file", "points", "time_ms", "memory_mb", "returncode"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            row = {k: r[k] for k in fieldnames if k in r}
            writer.writerow(row)
    valid = [r for r in results if r["points"] > 0 and r["returncode"] == 0]
    if valid:
        points = [r["points"] for r in valid]
        times = [r["time_ms"] for r in valid]
        plt.figure()
        plt.plot(points, times, 'o-')
        plt.xlabel("Number of points")
        plt.ylabel("Time (ms)")
        plt.title("Performance: Time vs Input Size")
        plt.grid(True)
        plt.savefig("benchmark_time.png")
        print("Saved benchmark_time.png")
        mems = [r["memory_mb"] for r in valid]
        plt.figure()
        plt.plot(points, mems, 's-', color='green')
        plt.xlabel("Number of points")
        plt.ylabel("Memory (MB)")
        plt.title("Memory Usage vs Input Size")
        plt.grid(True)
        plt.savefig("benchmark_memory.png")
        print("Saved benchmark_memory.png")
    else:
        print("No valid benchmark results")

if __name__ == "__main__":
    if not os.path.exists("data/fuzz_inputs/10k_points.csv"):
        print("Run python_tests/fuzzer.py first.")
    else:
        run_benchmark_suite()