_`fcpp Project Documentation`
=============================

_`Introduction`
---------------

fcpp is a modern C/C++ library development framework that integrates advanced build systems, dependency
management, and modular development support.

_`Main Features`
----------------

- Support for mixed C and C++ programming
- Built-in C++20 module support
- Conan-based dependency management
- Cross-platform build support (Windows/Linux/macOS)
- Automated code generation and processing
- Intelligent header and module conversion

_`Quick Start`
--------------

.. code-block:: bash

   # Install dependencies
   conan install .
   
   # Build the project
   conan build .

   # Create the package
   conan create .

_`Project Structure`
--------------------

::

   fcpp/
   ├── include/         # Header files
   ├── src/             # Source files
   ├── CMakeLists.txt   # CMake build configuration
   ├── conanfile.py     # Conan package configuration
   ├── metadata.json    # Project metadata
   └── LICENSE          # License file

_`Detailed Settings`
--------------------

For detailed settings in project-level meta, conan recipe, or cmake file, see:

.. toctree::
   CMakeList <components/cmake>
   Conanfile <components/conan>
   Metadata <components/meta>
   User concern contents <export>
   :numbered:
   :maxdepth: 2

_`License`
----------

This project is licensed under the Apache-2.0 License. See the LICENSE file for details.
