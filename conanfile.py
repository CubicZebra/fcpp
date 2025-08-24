from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps, cmake_layout
from typing import Literal
from pathlib import Path
import yaml
import os
sep = os.path.sep


white_list = {f'<{_}>' for _ in ['algorithm', 'array', 'chrono', 'cmath', 'functional', 'memory', 'optional',
                                 'string', 'string_view', 'utility', 'vector', 'deque', 'forward_list', 'list',
                                 'map', 'queue', 'set', 'stack', 'unordered_map', 'unordered_set', 'atomic',
                                 'thread', 'mutex', 'future', 'iostream', 'fstream', 'sstream', 'format', 'ranges',
                                 'mdspan', 'flat_map', 'flat_set']}
_is_valid_import = (lambda x, c: x.startswith('#include ') and x[9:].strip() in c)
conan_targets = {
    'Eigen3::Eigen': 'eigen::eigen',
    'ZLIB::ZLIB': 'zlib::zlib'
}


def _get_export_objects(x: list[str], tag: Literal['@exporter', '@attacher'] = '@exporter') -> list[str]:
    _cache = (''.join(x)).split('\n\n')  # TODO: maybe \n*3 is better (consider the namespace in CPP)?
    _export_objs = [_ for _ in _cache if tag in _]

    container = []
    for _obj in _export_objs:
        _obj = [_ for _ in _obj.split('\n') if _ != '']
        _res, _ptr = [_ for _ in _obj], False
        for i, (_v1, _v2) in enumerate(zip(_obj, _res)):
            if _v1.startswith(f' * {tag}'):
                _ptr = True
            if _v1.startswith(' */') and _ptr:
                _res[i] = _v2 + '\nexport '
                _ptr = False
        _res = '\n'.join([_ for _ in _res if not _.startswith(f' * {tag}')])
        if tag == '@exporter':
            _res = _res.replace('export \n','export ')
        else:  # @attacher
            _res = _res.replace('export \n', '')
        container.append(_res)

    return container


def _source_file_loader(txt: str) -> list[str]:
    with open(txt, 'r', encoding='utf-8') as f:
        _tmp = f.readlines()
    return _tmp


def _load_file(x: str) -> str:
    with open(x, 'r', encoding='utf-8') as f:
        res = f.readlines()
    return ''.join(res)


def _pragma_in_import(x: list[str]) -> tuple[bool, int]:
    # return the pragma once line in conan import wrapper, as its index if exists (-1 if not)
    _has_pragma, _idx = False, -1
    for i, _l in enumerate(x):
        if _l.startswith('#pragma once'):
            _has_pragma = True
            _idx = i
        if _l.strip() == '// Conan::ImportEnd':
            break
    return _has_pragma, _idx


class PackageRecipe(ConanFile):

    package_type = "library"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = ["CMakeLists.txt", "src/*", "include/*", "metadata.json", "LICENSE"]
    exports = ["conandata.yml", "metadata.json", "LICENSE"]

    generators = "VirtualBuildEnv", "VirtualRunEnv"
    conandata, meta, headers, sources, license_full_text , importable_modules = [None for _ in range(6)]

    def init(self):
        """
        ps1: Get-Content "build" | Invoke-Expression
        bash: bash ./build
        """
        conandata_path = Path(self.recipe_folder) / "conandata.yml"
        metadata_path = Path(self.recipe_folder) / "metadata.json"
        license_path = Path(self.recipe_folder) / "LICENSE"

        self.conandata = yaml.safe_load(conandata_path.read_text())
        self.meta = yaml.safe_load(metadata_path.read_text())

        # Required attributes
        self.name, self.version = self.meta.get('name'), self.meta.get('version')

        # Optional attributes
        self.license_full_text = _load_file(license_path.__str__())
        self.topics = tuple(self.meta.get('topics'))
        for k in ['license', 'url', 'homepage', 'description', 'authors', 'maintainers']:
            self.__setattr__(k, self.meta.get(k))

        # Modules processing
        self.headers, self.sources, self.importable_modules = None, None, self._determine_importable_modules()
        self._modules_preprocessing()

    def _file_detector(self, folder: str, obj: list[str], retarget: Path = None) -> list[tuple[str, str]]:
        entry = Path(self.recipe_folder) / folder if retarget is None else retarget / folder
        res = []
        for _obj in obj:
            res.extend(list(entry.rglob(f"*.{_obj}")))
        _tmp = [(os.path.dirname(str(file)), os.path.basename(str(file))) for file in res]
        return _tmp

    def _modules_preprocessing(self):

        # clear generated modules
        _m_files = self._file_detector("src", ["ixx", "cppm", ])
        for (k, v) in _m_files:
            _rm_file = k + sep + v
            if os.path.exists(_rm_file):
                os.remove(_rm_file)

        # regenerated module files
        if self.meta.get("generate_modules_inplace"):

            self.headers = self._file_detector("include", ["hpp", ])
            self.sources = self._file_detector("src", ["cpp", ])
            _suffix = 'ixx' if os.name == 'nt' else 'cppm'

            for (k, v) in self.sources:
                _src = v.split('.')
                _mod_name = _src[0]

                _hpp_content = _source_file_loader(k.replace('src', 'include') + sep + _mod_name + '.hpp')
                _hpp_intro, _hpp_inc, _hpp_split, _hpp_extra, _hpp_obj = self._module_elements(_hpp_content,
                                                                                               _mod_name)

                _cpp_content = _source_file_loader(k + sep + v)
                _cpp_intro, _cpp_inc, _cpp_split, _cpp_extra, _cpp_obj = self._module_elements(_cpp_content,
                                                                                               _mod_name)

                # merge export items in hpp or cpp
                _m_intro, _m_split = _hpp_intro, _hpp_split  # follow the hpp nomenclature
                _m_inc = [_ for _ in set(_hpp_inc).union(set(_cpp_inc)) if not _.startswith('// Conan::Escape')]
                _m_inc = [_ for _ in _m_inc if not _.startswith('#pragma once')]
                _m_inc = [_ for _ in _m_inc if f'{_mod_name}.hpp' not in _]  # escape self include
                _m_extra = [_ for _ in set(_hpp_extra).union(set(_cpp_extra))]
                _m_obj = ['\n'] + '@@'.join(_hpp_obj + _cpp_obj).replace('@@', '\n\n\n').split('\n')

                _m_full = _m_intro + _m_inc + _m_split + _m_extra + _m_obj
                with open(k + sep + _mod_name + f'.{_suffix}', 'w', encoding='utf-8') as f:
                    f.write('\n'.join(_m_full))

    def _determine_importable_modules(self):
        _tmp = [f'<{_}>' for _ in self.meta.get('std_modules') if f'<{_}>' in white_list]
        return _tmp + ['"' + _ + '.hpp";' for _ in self.meta.get("user_modules")]

    def build_requirements(self):
        self.build_requires(f"cmake/{self.meta.get('cmake_version')}")

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

        supported_compilers = {"gcc", "msvc", "clang", "apple-clang", }  # no support for 'Visual Studio' in Conan1.0
        if self.settings.compiler.__str__() in supported_compilers:
            _build_std = self.meta.get("build_cppstd")
            _build_std = "17" if _build_std not in {"17", "20", "23"} else _build_std  # fallback to C++17
            self.settings.compiler.cppstd = _build_std

        self._make_c_compatible()

    def _make_c_compatible(self):
        _c_hs = self._file_detector('include', ['h', ], retarget=Path(self.recipe_folder).parent / 'es')
        for (k, v) in _c_hs:
            _f = k + sep + v
            with open(_f, 'r', encoding='utf-8') as f:
                _org_text = f.readlines()
            _has_pragma, _idx = _pragma_in_import(_org_text)
            if _has_pragma:
                _start = ['#pragma once\n', '#ifdef __cplusplus\n', 'extern "C" {\n', '#endif\n']
            else:
                _start = ['#ifdef __cplusplus\n', 'extern "C" {\n', '#endif\n']
            _inner_text = ['    ' + l for i, l in enumerate(_org_text) if i != _idx]
            _end = ['#ifdef __cplusplus\n', '}\n', '#endif\n']
            _new_text = _start + _inner_text + _end

            with open(_f, 'w', encoding='utf-8') as f:
                f.write(''.join(_new_text))

    def requirements(self):
        for req in self.conandata.get('requirements'):
            self.requires(req)

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables['C_DEPS'], tc.variables['CPP_DEPS'] = self._preparing_deps_links()
        if self.options.shared:
            tc.variables['SHARED_MSG'] = 'Conan: shared=True is not supported due to complexity in this frame;'
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def _preparing_deps_links(self):
        _common, _c, _cpp = [self.meta.get('dependencies').get(_) for _ in ['common', 'c', 'cpp']]
        _c = {k: v if k not in _common.keys() else list(set(v).union(set(_common.get(k)))) for k, v in _c.items()}
        _cpp = {k: v if k not in _common.keys() else list(set(v).union(set(_common.get(k)))) for k, v in _cpp.items()}
        _c_deps = [f"{k}@{' '.join(v)}" for k, v in {**_common, **_c}.items()]
        _cpp_deps = [f"{k}@{' '.join(v)}" for k, v in {**_common, **_cpp}.items()]
        return _c_deps, _cpp_deps

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def _remove_customized_doc_command(self, tags: list[str] = None):  # maybe no use anymore

        if tags is None:
            tags = ['@exporter', '@attacher']

        _cpp = self._file_detector('src', ['cpp', ], retarget=Path(self.recipe_folder).parent / 'es')
        _hpp = self._file_detector('include', ['hpp', ], retarget=Path(self.recipe_folder).parent / 'es')

        for (k, v) in (_cpp + _hpp):
            _f = k + sep + v
            with open(_f, 'r', encoding='utf-8') as f:
                _file = f.readlines()
            with open(_f, 'w', encoding='utf-8') as w:
                w.write(''.join([_ for _ in _file if not any([_.startswith(f' * {tag}') for tag in tags])]))


    def _module_elements(self, x: list[str], m_name: str):
        # two transformations if matches:
        # 1. #include <lib> => import <lib>;
        # 2. #include "lib.hpp" => import "lib.hpp";

        _flag, _is_import_lines, _splitter = 1, [], 0
        for i, _l in enumerate(x):
            _is_import_lines.append(_flag)
            if _l.strip() == '// Conan::ImportEnd':
                _flag = 0
                _splitter = i + 1

        _import_context = [l for i, l in zip(_is_import_lines, x) if i]
        _other_context = [l for i, l in zip(_is_import_lines, x) if not i]

        _tmp = ['// Conan::Escape ' + _ if _is_valid_import(_, self.importable_modules) else _ for _
                in _import_context[1:-1]]
        _extra = ['import ' + _.split('#include ')[-1].strip() + ';\n' for _ in _tmp if
                  _.startswith('// Conan::Escape ')]
        _intro, _split = ['module;\n', ], [f'export module {m_name};\n', ]

        # drop '\n' in import lines
        _intro, _tmp, _split, _extra = ([_.strip() for _ in _intro], [_.strip() for _ in _tmp],
                                        [_.strip() for _ in _split], [_.strip() for _ in _extra])

        return  (_intro, _tmp, _split, _extra, _get_export_objects(_other_context, '@exporter') +
                 _get_export_objects(_other_context, '@attacher'))

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = [self.name]
        _c, _cpp = self._preparing_deps_links()

        self.cpp_info.components[f"{self.name}_c"].libs = [f"{self.name}_c"]
        self.cpp_info.components[f"{self.name}_c"].requires = [[_t := _.split('@')[1],
                                                                conan_targets[_t] if _t in conan_targets.keys()
                                                                else _t][-1] for _ in _c]
        self.cpp_info.components[f"{self.name}_cpp"].libs = [f"{self.name}_cpp"]
        self.cpp_info.components[f"{self.name}_cpp"].requires = [[_t := _.split('@')[1],
                                                                  conan_targets[_t] if _t in conan_targets.keys()
                                                                  else _t][-1] for _ in _cpp]

    @staticmethod
    def _call_syntax_suggestion():
        _content = ['============================= Syntax Guide =============================',
                    '1.force 2 blank lines to distinguish global objects;',
                    '2.Use // Conan::ImportStart and // Conan::ImportEnd in beginning,',
                    '  wrapping #include lines;',
                    '3.generate_modules_inplace is true in metadata.json can automatically,',
                    '  generate modules (ixx, cppm) files;',
                    '4.std_modules and user_modules in metadata.json affect import lines,',
                    '5.std_modules make #include <stdlib> to import <stdlib>; in the right',
                    '  order, when 3. is satisfied;',
                    '6.user_modules make #include <usrlib.hpp> to import <usrlib.hpp> in',
                    '  the right order, when 3. is satisfied;',
                    '7.multi-lined doxygen /** ... */ with @exporter inside, will export',
                    '  associated global object (see 1.) into generated modules;',
                    '8.multi-lined doxygen /** ... */ with @attacher inside, will attach',
                    '  associated global object (see 1.) into generated modules;',
                    '9.suffix .h and .c for C; then .hpp and .cpp for C++;',
                    '============================= Guide Over =============================', ]
        print(*_content, sep='\n')