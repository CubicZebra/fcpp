_`Metadata Configuration`
=========================

_`Project-level Settings`
-------------------------

The metadata.json file contains the metadata configuration for the fcpp project, including basic project
information, build configuration, and dependency definitions.

_`File Structure`
-----------------

The JSON file includes sections for basic project information (name, version, license, description), authors and
maintainers, build configuration (CMake version, C/C++ standards), module settings, dependency definitions, and
documentation configuration.

_`Key Settings`
---------------

Basic project information defines the package identity. Build configuration specifies tool versions and language
standards. Module settings control standard and user module usage. Dependencies are categorized into common,
C-specific, and C++-specific requirements. Documentation settings configure Doxygen generation.

Example configuration demonstrates how to set up a project with C++20 support, module generation, and common
dependencies like Boost and OpenCV.
