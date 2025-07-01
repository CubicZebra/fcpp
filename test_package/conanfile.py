from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.build import can_run
from conan.tools.env import VirtualRunEnv, VirtualBuildEnv
from pathlib import Path
import yaml
import os
sep = os.path.sep


class tstTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"

    def init(self):
        conandata_path = Path(self.recipe_folder).parent / "conandata.yml"
        self.conandata = yaml.safe_load(conandata_path.read_text())

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

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def layout(self):
        cmake_layout(self)

    def test(self):
        if can_run(self):
            exe_path = os.path.join(self.cpp.build.bindirs[0], "example")
            if self.settings.os == "Windows":
                exe_path += ".exe"
            self.run(exe_path, env="conanrun")

