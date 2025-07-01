from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
from pathlib import Path
import yaml
import os
sep = os.path.sep


white_list = {f'<{_}>' for _ in ['algorithm', 'array', 'chrono', 'cmath', 'functional', 'memory', 'optional',
                                 'string', 'string_view', 'utility', 'vector', 'deque', 'forward_list', 'list',
                                 'map', 'queue', 'set', 'stack', 'unordered_map', 'unordered_set', 'atomic',
                                 'thread', 'mutex', 'future', 'iostream', 'fstream', 'sstream', 'format', 'ranges',
                                 'mdspan', 'flat_map', 'flat_set']}


def _import_process(x: str) -> str:
    res = x
    if x.startswith('#include '):
        if (_mod := x[9:].strip()) in white_list:
            res = 'import ' + _mod + ';'
    return res


def simple_header_parser(txt: str, tag: str = '@exporter'):

    with open(txt, 'r', encoding='utf-8') as f:
        _tmp = f.readlines()

    # interpret exporter declaration, for fixed syntax
    _res, _ptr = [_ for _ in _tmp], False
    for i, (_v1, _v2) in enumerate(zip(_tmp, _res)):
        if _v1.startswith(f' * {tag}'):
            _ptr = True
        if _v1.startswith(' */') and _ptr:
            _res[i] = _v2 + 'export '
            _ptr = False
    _res = [_ for _ in (''.join(_res)).split('\n') if not _.startswith(f' * {tag}')]

    # for pre-processing
    _res = [_import_process(_) for _ in _res if _.strip() != '#pragma once']
    _import_lines, _other_lines = ([_ for _ in _res if _.startswith('import')],
                                   [_ for _ in _res if not _.startswith('import')])
    _res = _import_lines + _other_lines

    return _res


class fcppRecipe(ConanFile):
    name = "fcpp"
    version = "1.0.1"
    package_type = "library"

    # Optional metadata
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of tst package here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "src/*", "include/*"
    exports = "conandata.yml"

    generators = "VirtualBuildEnv", "VirtualRunEnv"
    conandata, headers, sources = None, None, None
    # requires = _requires

    def init(self):
        conandata_path = Path(self.recipe_folder) / "conandata.yml"
        self.conandata = yaml.safe_load(conandata_path.read_text())

        self.headers = self._file_detector("include", ["h", "hpp", "hxx"])
        self.sources = self._file_detector("src", ["c", "cpp", "cxx"])
        self._cppm_generator()

    def _file_detector(self, folder: str, obj: list[str]) -> list[tuple[str, str]]:
        entry, res = Path(self.recipe_folder) / folder, []
        for _obj in obj:
            res.extend(list(entry.rglob(f"*.{_obj}")))
        _tmp = [(os.path.dirname(str(file)), os.path.basename(str(file))) for file in res]
        return _tmp

    def _cppm_generator(self):
        _src = Path(self.recipe_folder) / 'src'
        _suffix = 'ixx' if os.name == 'nt' else 'cppm'

        for (k, v) in self.headers:
            _mod_name = v.split('.')[0]
            _content = [f'// Generated via simple_header_parser',
                        f'export module {_mod_name};'] + simple_header_parser(k + sep + v)
            _target_f = k.replace('include', 'src') + sep + _mod_name + f'.{_suffix}'
            with open(_target_f, 'w', encoding='utf-8') as f:
                f.write('\n'.join(_content))

    def build_requirements(self):
        self.build_requires("cmake/4.0.1")

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def requirements(self):
        for req in self.conandata.get('requirements'):
            self.requires(req)

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ['fcpp']