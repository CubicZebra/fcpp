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

.. 【中文简介】
   CMakeLists.txt 是 fcpp 项目的核心构建配置文件，负责项目构建、依赖管理和模块编译。
   主要功能包括：项目初始化和元数据解析、源文件自动收集与目标创建、依赖管理及链接、
   C++模块支持配置和安装规则定义。配置自动从metadata.json读取项目信息，为C++23及以上版本
   配置模块支持，并处理不同平台的模块编译设置。