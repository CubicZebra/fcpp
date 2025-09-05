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

.. 【中文简介】
   conanfile.py 是 fcpp 项目的 Conan 包配置文件，负责依赖管理、包元数据处理和模块生成。
   主要功能包括：项目元数据初始化、依赖管理、模块文件生成与处理、构建配置生成和包信息定义。
   核心功能是通过PackageRecipe类从metadata.json加载项目信息，处理模块文件生成，管理依赖关系，
   并生成CMake构建配置。