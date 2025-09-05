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
   :numbered:
   :maxdepth: 2

_`License`
----------

This project is licensed under the Apache-2.0 License. See the LICENSE file for details.

.. 【中文简介】
   fcpp 是一个现代化的 C/C++ 库开发框架，集成了先进的构建系统、依赖管理和模块化开发支持。
   主要特性包括：C/C++混合编程支持、C++20模块支持、基于Conan的依赖管理、跨平台构建、
   自动化代码生成和处理，以及智能头文件与模块转换功能。