_`CMakeLists Configuration`
===========================

_`Overview`
-----------

The CMakeLists.txt file is the core build configuration file for the fcpp project, responsible for project building,
dependency management, and module compilation.

_`Key Features`
---------------

- Project initialization and metadata parsing
- Automatic source file collection and target creation
- Dependency management and linking
- C++ module support configuration
- Installation rule definition

_`Main Configurations`
----------------------

The CMake configuration automatically reads project information from metadata.json, collects source files from
include and src directories, creates separate static libraries for C and C++ components, and configures module
support for C++23 and above.

Platform-specific module compilation is handled with appropriate settings for MSVC (.ixx files) and
GCC/Clang (.cppm files). The configuration also includes installation rules for libraries and headers.
