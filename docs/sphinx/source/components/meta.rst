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

.. 【中文简介】
   metadata.json 是 fcpp 项目的元数据配置文件，包含项目基本信息、构建配置和依赖定义。
   文件结构包括：基本项目信息（名称、版本、许可证、描述）、作者和维护者信息、构建配置
   （CMake版本、C/C++标准）、模块设置、依赖定义和文档配置。关键配置项涵盖了项目标识、
   构建工具设置、模块使用和依赖管理等方面。