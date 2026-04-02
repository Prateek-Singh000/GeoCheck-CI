import random
import os

def generate_random_csv(filename, num_points):
    """Generate a CSV file with random 3D points (x,y,z) in range -10..10"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        for _ in range(num_points):
            x = random.uniform(-10, 10)
            y = random.uniform(-10, 10)
            z = random.uniform(-10, 10)
            f.write(f"{x},{y},{z}\n")
    print(f"Generated {num_points} points in {filename}")

def generate_corrupt_csv(filename):
    """Generate a CSV with intentionally bad data (non-numeric, empty lines)"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        f.write("abc,def,ghi\n")        # non-numeric
        f.write("1.0,2.0\n")            # missing column
        f.write(",,,\n")                # empty
        f.write("1.0,2.0,3.0\n")        # valid
        f.write("1.0e10,2.0e10,3.0e10\n")  # huge numbers
    print(f"Generated corrupt CSV: {filename}")

if __name__ == "__main__":
    # Generate files for testing
    generate_random_csv("data/fuzz_inputs/10k_points.csv", 10000)
    generate_random_csv("data/fuzz_inputs/100k_points.csv", 100000)
    generate_random_csv("data/fuzz_inputs/1M_points.csv", 1000000)
    generate_corrupt_csv("data/fuzz_inputs/corrupt.csv")
    print("\nFuzzing files created in data/fuzz_inputs/")