from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout, CMakeToolchain
from conan.tools.build import can_run
from conan.tools.env import VirtualRunEnv, VirtualBuildEnv
from pathlib import Path
import shutil
import yaml
import os
sep = os.path.sep


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
        if can_run(self):
            cmd = os.path.join(self.cpp.build.bindirs[0], "example")
            self.run(cmd, env="conanrun")


def _clear_test_build():
    _build = sep.join(__file__.split(sep)[:-1] + ['build'])
    _presets = sep.join(__file__.split(sep)[:-1] + ['CMakeUserPresets.json'])
    if os.path.exists(_build):
        shutil.rmtree(_build)
    if os.path.exists(_presets):
        os.remove(_presets)


if __name__ == '__main__':
    _clear_test_build()
