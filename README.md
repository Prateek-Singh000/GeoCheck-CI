# GeoCheck‑CI

[![CI](https://github.com/Prateek-Singh000/GeoCheck-CI/actions/workflows/ci.yml/badge.svg)](https://github.com/Prateek-Singh000/GeoCheck-CI/actions/workflows/ci.yml)

**Automated Geometry Integrity & Performance Validator** – a production‑ready framework that bridges high‑performance C++ geometry kernels with enterprise‑grade Python quality automation. Designed to mirror the workflows of **Software Development Engineers (SDE)** and **Software Quality Engineers (SQE)** at companies like Autodesk.

---

## ✨ Key Features

### 🚀 SDE Component (C++ Engine)
- Fast point‑in‑axis‑aligned‑box checker (linear scan, ready for AABB tree upgrade)
- CLI interface with `--input` and `--box` arguments
- Modern C++17, STL, compiled with `-O3` optimisations
- Cross‑platform (Windows / Linux / macOS)

### 🧪 SQE Component (Python Framework)
- **Fuzzing** – generates 10k / 100k / 1M random points + corrupt CSV files
- **Benchmarking** – measures time and memory, produces `matplotlib` graphs
- **Regression suite** – `pytest` tests with golden dataset
- **CI/CD** – GitHub Actions runs all tests on every push

---

## 🛠️ Tech Stack

| Area | Technologies |
|------|--------------|
| Core engine | C++17, STL, CMake |
| Quality automation | Python 3, `pytest`, `psutil`, `matplotlib` |
| CI/CD | GitHub Actions (Ubuntu + Windows runners) |
| Version control | Git |

---

## 🚀 Getting Started

### Prerequisites
- C++ compiler (g++ 6.3+ or Visual Studio)
- Python 3.7+ with `pip`
- Git

### Clone & Build

```bash
git clone https://github.com/Prateek-Singh000/GeoCheck-CI.git
cd GeoCheck-CI
g++ -std=c++17 -O3 -Wall cpp_src/main.cpp -o aabb_engine   # Linux/macOS
# or on Windows: g++ -std=c++17 -O3 -Wall cpp_src/main.cpp -o aabb_engine.exe## 🧱 Architecture
