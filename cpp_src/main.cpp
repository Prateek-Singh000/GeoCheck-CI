#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <chrono>

struct Point3D {
    double x, y, z;
};

struct BoundingBox {
    double xmin, xmax, ymin, ymax, zmin, zmax;
    
    bool contains(const Point3D& p) const {
        return (p.x >= xmin && p.x <= xmax &&
                p.y >= ymin && p.y <= ymax &&
                p.z >= zmin && p.z <= zmax);
    }
};

int main(int argc, char* argv[]) {
    // Default box: unit cube from (0,0,0) to (1,1,1)
    BoundingBox box = {0.0, 1.0, 0.0, 1.0, 0.0, 1.0};
    std::string inputFile;
    
    // Simple CLI parsing
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--input" && i+1 < argc) {
            inputFile = argv[++i];
        } else if (arg == "--box" && i+3 < argc) {
            box.xmin = std::stod(argv[++i]);
            box.xmax = std::stod(argv[++i]);
            box.ymin = std::stod(argv[++i]);
            box.ymax = std::stod(argv[++i]);
            box.zmin = std::stod(argv[++i]);
            box.zmax = std::stod(argv[++i]);
        } else if (arg == "--help") {
            std::cout << "Usage: aabb_engine --input <points.csv> [--box xmin xmax ymin ymax zmin zmax]\n";
            return 0;
        }
    }
    
    if (inputFile.empty()) {
        std::cerr << "Error: No input file specified. Use --input <filename>\n";
        return 1;
    }
    
    // Read points from CSV (format: x,y,z per line)
    std::ifstream file(inputFile);
    if (!file.is_open()) {
        std::cerr << "Error: Cannot open file " << inputFile << "\n";
        return 1;
    }
    
    std::vector<Point3D> points;
    std::string line;
    while (std::getline(file, line)) {
        std::stringstream ss(line);
        Point3D p;
        char comma;
        ss >> p.x >> comma >> p.y >> comma >> p.z;
        if (!ss.fail()) {
            points.push_back(p);
        }
    }
    file.close();
    
    // Process each point
    auto start = std::chrono::high_resolution_clock::now();
    for (const auto& p : points) {
        if (box.contains(p)) {
            std::cout << "INSIDE\n";
        } else {
            std::cout << "OUTSIDE\n";
        }
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    
    // Output performance info to stderr (so it doesn't interfere with regression tests)
    std::cerr << "Processed " << points.size() << " points in " << duration.count() << " ms\n";
    
    return 0;
}