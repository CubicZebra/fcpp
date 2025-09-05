# A Modern C/CPP Library Build System

This project is a C/C++ library built using Conan 2.0, featuring modern C and C++ standards support and module 
capabilities.

## Badges

![GitHub License](https://img.shields.io/github/license/CubicZebra/fcpp)
[![CodeFactor](https://www.codefactor.io/repository/github/cubiczebra/fcpp/badge)](https://www.codefactor.io/repository/github/cubiczebra/fcpp)

## Project Overview

- **Language**: C/C++
- **Library Build System**: Python with Conan 2.0
- **File Build System**: Doxygen, Graphviz, Sphinx
- **Module Support**: Optionally activated, when C++ standard ≥ 23
- **Component Structure**:
    - pairwise header and source assumption
    - strict suffix constraint, (.h, .c) for C part, and (.hpp, .cpp) for C++ part
    - documenting system uses .dox for pure docstring, .cxx for examples codes

## Features

- Conan-based modern dependency management
- Supports C++ standards 17, 20, and 23
- Automatic module file generation (`.ixx`/`.cppm`) from headers/sources
- Cross-platform compatibility (Windows, Linux, macOS)
- Dual C and C++ interfaces with separate linkage targets
- Doxygen annotation support for object exporting (`@exporter`, `@attacher`)
- Automation documenting system via Doxygen and Sphinx
- Importation, derivation and call relationship illustration through Graphviz

## Build Requirements

- Conan 2.0+
- Compatible C/C++ compiler:
    - GCC
    - Clang
    - MSVC
    - Apple Clang

## Crash Course of Build

### 1. Build then test your library

```bash
conan create . -s build_type=Debug --build=missing
```

### 2. Build documentations

```bash
python ./docs/build.py
```

### 3. Add requirements

Add your desired library in *conandata.yml* where dependency graph is computed through, then modify the 
**dependencies** field in *metadata.json*, to link the targets in the proper way (no need modification
on *CMakeLists.txt*).

Requirements for your project can be the package archived on [Conan Center](https://conan.io/center), or user 
built ones. If the later, more detailed configuration is in discussion.

## Project Structure

```
project-root/
├── conanfile.py             # Conan recipe
├── CMakeLists.txt           # CMake build framework
├── metadata.json            # Project metadata configuration (name, version, etc)
├── conandata.yml            # Dependency specifications, Conan plugin support
├── LICENSE                  # Project license
├── include/                 # Public headers
│   ├── *.h                  # C interface headers
│   └── *.hpp                # C++ interface headers
├── src/                     # Implementation files
│   ├── *.c                  # C sources
│   ├── *.cpp                # C++ sources
│   └── *.ixx/*.cppm         # Auto-generated Module files (in experimental)
└── docs/                    # Documentations root
    ├── doxygen/             # Doxygen system main root
    │   ├── dox/             # Pure documentations' folder
    │   │   ├── demos/       # Examples catelogue
    │   │   │   ├── *.dox    # Documenting docstring
    │   │   │   └── *.cxx    # Example codes
    │   │   └── *.dox        # Main pages and etc
    │   └── ...
    ├── sphinx/              # Sphinx system main root
    │   ├── source/          # Source files of sphinx system
    │   ├── locales/         # Pot files for internalization
    │   └── ...
    └── images/              # Static images for doxygen/sphinx system
```

## Module Generation

When `generate_modules_inplace` is enabled in `metadata.json`:

1. Header/source pairs automatically generate module files
2. `#include` directives are converted to `import` statements
3. Doxygen annotations control symbol visibility:
    - `@exporter`: Exports symbols in modules
    - `@attacher`: Attaches symbols to modules

This feature is experimental now, however, the specific syntax can make the existing project a ease 
migration to fit the future C++ standard.

## Compiler Support Matrix

| Feature          | MSVC | Clang | GCC | Apple Clang |
|------------------|------|-------|-----|-------------|
| C++ Modules      | ✓    | ✓     | ✓   | ✓           |
| C Compatibility  | ✓    | ✓     | ✓   | ✓           |
| Automatic Export | ✓    | ✓     | ✓   | ✓           |

## License

[Apache-2.0] - See included LICENSE file for details.