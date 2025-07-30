from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout, CMakeToolchain
from conan.tools.build import can_run
from conan.tools.env import VirtualRunEnv, VirtualBuildEnv
from pathlib import Path
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
        self.build_requires("cmake/4.0.1")

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
        tc.variables["DEP_TARGETS"] = self._get_targets()
        tc.generate()

    def _calculate_targets(self):
        _common, _c, _cpp = [self.metadata.get('dependencies').get(_) for _ in ['common', 'c', 'cpp']]
        _lib_name = self.metadata.get('name')
        res = {f'{_lib_name}_c', f'{_lib_name}_cpp'}
        for k, v in _common.items():
            res = res.union(set(v))
        for k, v in _c.items():
            res = res.union(set(v))
        for k, v in _cpp.items():
            res = res.union(set(v))
        return ';'.join(res)

    def _get_targets(self):
        _targets = self.metadata.get('targets')
        if _targets is None or _targets == 'auto':
            _targets = self._calculate_targets()
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
