from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout, CMakeToolchain
from conan.tools.build import can_run
from conan.tools.env import VirtualRunEnv, VirtualBuildEnv
from pathlib import Path
import shutil
import yaml
import os
sep = os.path.sep


def _clear_test_build():
    _build = sep.join(__file__.split(sep)[:-1] + ['build'])
    _presets = sep.join(__file__.split(sep)[:-1] + ['CMakeUserPresets.json'])
    if os.path.exists(_build):
        shutil.rmtree(_build)
    if os.path.exists(_presets):
        os.remove(_presets)


def _recursive_find(root: str, obj_files: list[str]):
    for f in os.listdir(root):
        _f = root + sep + f
        if not os.path.isdir(_f):
            if f in obj_files:
                yield _f
        else:
            yield from _recursive_find(_f, obj_files)


class PackageTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps"

    conandata, metadata = None, None

    def init(self):
        conandata_path = Path(self.recipe_folder).parent / "conandata.yml"
        self.conandata = yaml.safe_load(conandata_path.read_text())
        metadata_path = Path(self.recipe_folder).parent / "metadata.json"
        self.metadata = yaml.safe_load(metadata_path.read_text())

    def build_requirements(self):
        self.build_requires(f"cmake/{self.metadata.get('cmake_version')}")

    def requirements(self):
        self.requires(self.tested_reference_str)
        for req in self.conandata.get("requirements", []):
            self.requires(req)

    def generate(self):
        build_env, run_env = VirtualBuildEnv(self), VirtualRunEnv(self)
        build_env.generate()
        run_env.generate(scope="run")

        tc = CMakeToolchain(self)
        lib_name = self.tested_reference_str.split("/")[0]
        tc.variables["LIB_NAME"] = lib_name
        tc.variables["CXX_DEPS"] = self._get_targets()
        tc.variables["TRIGGER_TESTS"] = self.metadata.get('trigger_tests')
        tc.generate()

    def _preparing_deps_links(self):
        _common, _c, _cpp, _test = [self.metadata.get('dependencies').get(_) for _ in ['common', 'c', 'cpp', 'test']]
        _c = {k: v if k not in _common.keys() else list(set(v).union(set(_common.get(k)))) for k, v in _c.items()}
        _cpp = {k: v if k not in _common.keys() else list(set(v).union(set(_common.get(k)))) for k, v in _cpp.items()}
        _test_deps = [f"{k}@{' '.join(v)}" for k, v in _test.items()]
        _c_deps = [f"{k}@{' '.join(v)}" for k, v in {**_common, **_c}.items()]
        _cpp_deps = [f"{k}@{' '.join(v)}" for k, v in {**_common, **_cpp}.items()]
        return list(set(_c_deps).union(set(_cpp_deps)).union(set(_test_deps)))

    def _get_targets(self):
        _targets, _name = self.metadata.get('target'), self.metadata.get('name')
        if _targets is None or _targets == 'auto':
            _targets = [f'{_name}@{_name}::{_name}']
        else:
            _targets = [f'{_name}@{_targets}']
        _targets.extend(self._preparing_deps_links())
        return _targets

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def layout(self):
        cmake_layout(self)

    def configure(self):
        supported_compilers = {"gcc", "msvc", "clang", "apple-clang", }  # no support for 'Visual Studio' in Conan1.0
        if self.settings.compiler.__str__() in supported_compilers:
            _build_std = self.metadata.get("build_cppstd")
            _build_std = "17" if _build_std not in {"17", "20", "23"} else _build_std  # fallback
            self.settings.compiler.cppstd = _build_std

    def test(self):

        # scripting in test_package/main.cpp
        if can_run(self):
            cmd = os.path.join(self.cpp.build.bindirs[0], "main")
            self.run(cmd, env="conanrun")

        # test cases in test_pacakge/test/*.cpp
        if self.metadata.get('trigger_tests'):
            try:
                if can_run(self):
                    cmake = CMake(self)
                    cmake.test()
            except (Exception, ) as err:
                print('CTest Crashed:', err)
            finally:
                target_folder = self.recipe_folder + sep + 'test' + sep + 'export'
                if self.metadata.get('saving_tests_log'):
                    obj_folder = self.recipe_folder + sep + 'build'
                    report = [_ for _ in _recursive_find(obj_folder, ['LastTest.log'])][0]  # need robust
                    with open(report, 'r', encoding='utf-8') as f:
                        _content = f.readlines()
                    with open(target_folder + sep + 'TestResult.log', 'w', encoding='utf-8') as f:
                        f.write(''.join(_content))
                else:
                    if os.path.exists(_f := target_folder + sep + 'TestResult.log'):
                        os.remove(_f)


if __name__ == '__main__':
    _clear_test_build()
