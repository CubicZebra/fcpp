_`Conanfile Configuration`
==========================

_`Usage`
--------

The conanfile.py is the Conan package configuration file for the fcpp project, responsible for dependency management,
package metadata processing, and module generation.

_`Main Features`
----------------

- Project metadata initialization
- Dependency management
- Module file generation and processing
- Build configuration generation
- Package information definition

_`Core Functionality`
---------------------

The PackageRecipe class handles project initialization by loading information from metadata.json. It processes
module files by generating them from .hpp and .cpp files, handling export and attach markers. Dependency management
is implemented by loading requirements from conandata.yml.

The configuration generates CMake toolchain and dependencies files, and defines package components with their
dependencies. Special features include C header compatibility processing and comment marker handling for
export/attach operations.
