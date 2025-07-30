# A Modern C/CPP Library Build System

This project is a C/C++ library built using Conan 2.0 and CMake, featuring modern C++ standards support and module capabilities.

## Project Overview
- **Language**: C/C++
- **Build System**: CMake
- **Package Manager**: Conan 2.0
- **Module Support**: Optionally activated, when C++ standard ≥ 23
- **Component Structure**:
    - `c_part`: C-compatible library component
    - `cpp_part`: C++ library component with module support

## Features
- Supports C++ standards 17, 20, and 23
- Automatic module file generation (`.ixx`/`.cppm`) from headers/sources
- Cross-platform compatibility (Windows, Linux, macOS)
- Dual C and C++ interfaces with separate linkage targets
- Doxygen annotation support for symbol exporting (`@exporter`, `@attacher`)
- Conan-based dependency management

## Build Requirements
- Conan 2.0+
- CMake ≥ 3.28
- Compatible C/C++ compiler:
    - GCC
    - Clang
    - MSVC
    - Apple Clang

## Build Instructions

### 1. Install dependencies
```bash
conan install . --output-folder=build --build=missing
```

### 2. Configure with CMake
```bash
cd build
cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
```

### 3. Build the project
```bash
cmake --build .
```

### 4. Install the library
```bash
cmake --install .
```

## Usage in Other Projects

### Conan (package consumers)
Add to your `conanfile.py`:
```python
requires = "your_project_name/version"
```

### CMake Integration
```cmake
find_package(your_project_name REQUIRED)
target_link_libraries(your_target PRIVATE
    your_project_name::c_part     # C interface
    your_project_name::cpp_part   # C++ interface
)
```

## Project Structure
```
project-root/
├── conanfile.py         # Conan recipe
├── CMakeLists.txt       # CMake build configuration
├── metadata.json        # Project metadata (name, version, etc)
├── conandata.yml        # Dependency specifications
├── include/             # Public headers
│   ├── *.h              # C interface headers
│   └── *.hpp            # C++ interface headers
├── src/                 # Implementation files
│   ├── *.c              # C sources
│   ├── *.cpp            # C++ sources
│   └── (auto-generated) # Module files (*.ixx/*.cppm)
└── LICENSE              # Project license
```

## Module Generation
When `generate_modules_inplace` is enabled in `metadata.json`:
1. Header/source pairs automatically generate module files
2. `#include` directives are converted to `import` statements
3. Doxygen annotations control symbol visibility:
    - `@exporter`: Exports symbols in modules
    - `@attacher`: Attaches symbols to modules

## Compiler Support Matrix
| Feature          | MSVC | Clang | GCC | Apple Clang |
|------------------|------|-------|-----|-------------|
| C++ Modules      | ✓    | ✓     | ✓   | ✓           |
| C Compatibility  | ✓    | ✓     | ✓   | ✓           |
| Automatic Export | ✓    | ✓     | ✓   | ✓           |

## License
[Apache-2.0] - See included LICENSE file for details.