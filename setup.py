import inspect
import os
import sys
from pathlib import Path

import cmake_build_extension
import setuptools

# This example is compliant with PEP517 and PEP518. It uses the pyproject.toml file to store
# most of the package metadata. However, build extensions are not supported and must be
# configured in the setup.py.
setuptools.setup(
    # Custom setuptools extension that configures a CMake project.

    # Args:
    #     name: The name of the extension.
    #     install_prefix: The path relative to the site-package directory where the CMake
    #         project is installed (typically the name of the Python package).
    #     disable_editable: Skip this extension in editable mode.
    #     write_top_level_init: Create a new top-level ``__init__.py`` file in the install
    #         prefix and write content.
    #     cmake_configure_options: List of additional CMake configure options (-DBAR=FOO).
    #     source_dir: The location of the main CMakeLists.txt.
    #     cmake_build_type: The default build type of the CMake project.
    #     cmake_component: The name of component to install. Defaults to all components.
    #     cmake_depends_on: List of dependency packages containing required CMake projects.
    #     expose_binaries: List of binary paths to expose, relative to top-level directory.
    ext_modules=[
        cmake_build_extension.CMakeExtension(
            name="Pybind11Bindings",
            # Name of the resulting package name (import my_project)
            install_prefix="my_project",
            # Note: pybind11 is a build-system requirement specified in pyproject.toml,
            #       therefore pypa/pip or pypa/build will install it in the virtual
            #       environment created in /tmp during packaging.
            #       This cmake_depends_on option adds the pybind11 installation path
            #       to CMAKE_PREFIX_PATH so that the example finds the pybind11 targets
            #       even if it is not installed in the system.
            cmake_depends_on=["pybind11", 'numpy'],
            # Exposes the binary print_answer to the environment.
            # It requires also adding a new entry point in setup.cfg.
            # expose_binaries=["bin/print_answer"],
            # Writes the content to the top-level __init__.py
            # write_top_level_init=init_py,
            # Selects the folder where the main CMakeLists.txt is stored
            # (it could be a subfolder)
            source_dir=str(Path(__file__).parent.absolute()),
            cmake_configure_options=[
                # This option points CMake to the right Python interpreter, and helps
                # the logic of FindPython3.cmake to find the active version
                f"-DPython3_ROOT_DIR={Path(sys.prefix)}",
                "-DCALL_FROM_SETUP_PY:BOOL=ON",
                "-DBUILD_SHARED_LIBS:BOOL=OFF",
            ]
        ),
    ],
    cmdclass=dict(
        # Enable the CMakeExtension entries defined above
        build_ext=cmake_build_extension.BuildExtension,
        # If the setup.py or setup.cfg are in a subfolder wrt the main CMakeLists.txt,
        # you can use the following custom command to create the source distribution.
        # sdist=cmake_build_extension.GitSdistFolder
    ),
)