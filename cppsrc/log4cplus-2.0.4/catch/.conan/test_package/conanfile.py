#!/usr/bin/env python
# -*- coding: utf-8 -*-
from conans import ConanFile, CMake
import os


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        assert os.path.isfile(os.path.join(self.deps_cpp_info["Catch2"].rootpath, "licenses", "LICENSE.txt"))
        bin_path = os.path.join("bin", "test_package")
        self.run(f"{bin_path} -s", run_environment=True)
