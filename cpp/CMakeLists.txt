find_package(xtl REQUIRED)
find_package(xtensor REQUIRED)
if (NOT xtensor_FOUND)
    # xtensor not found, try to find it as a submodule
    # else add it as a submodule at enternal/pybind11
    if (EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/external/xtensor/CMakeLists.txt")
        message(STATUS "xtensor submodule found")
        add_subdirectory(xtensor)
    else()
        message(STATUS "xtensor submodule not found, downloading from github")
        include(FetchContent)
        FetchContent_Declare(
            xtensor
            GIT_REPOSITORY 
        )
        FetchContent_MakeAvailable(xtensor)
    endif()
else()
    message(STATUS "xtensor found")
endif()

# --- compile cpp code as a shared lib and (optional)test it ---

# Use -fPIC even if statically compiled
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# If rely on external cpp submodule, 
# add_subdirectory()
# ... or compile it manually
add_library(
    cpp_core
    src/example.cpp
)

# Optional: set_target_properties

# Include directory of headers
target_include_directories(
    cpp_core
    PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(
    cpp_core
    PUBLIC
    xtensor
)

# --- add deps ---
## find python then pybind11
find_package(Python REQUIRED COMPONENTS Interpreter Development NumPy)
find_package(pybind11 REQUIRED CONFIG QUIET)
find_package(xtensor-python REQUIRED)

if (NOT pybind11_FOUND)
    # pybind11 not found, try to find it as a submodule
    # else add it as a submodule at enternal/pybind11
    if (EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/external/pybind11/CMakeLists.txt")
        message(STATUS "pybind11 submodule found")
        add_subdirectory(pybind11)
    else()
        message(STATUS "pybind11 submodule not found, downloading from github")
        include(FetchContent)
        FetchContent_Declare(
            pybind11
            GIT_REPOSITORY 
        )
        FetchContent_MakeAvailable(pybind11)
    endif()
else()
    message(STATUS "pybind11 found")
endif()

if (NOT xtensor-python_FOUND)
    # xtensor-python not found, try to find it as a submodule
    # else add it as a submodule at enternal/pybind11
    if (EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/external/xtensor-python/CMakeLists.txt")
        message(STATUS "xtensor-python submodule found")
        add_subdirectory(xtensor-python)
    else()
        message(STATUS "xtensor-python submodule not found, downloading from github")
        include(FetchContent)
        FetchContent_Declare(
            xtensor-python
            GIT_REPOSITORY 
        )
        FetchContent_MakeAvailable(xtensor-python)
    endif()
else()
    message(STATUS "xtensor-python found")
endif()


# --- compile python module ---
pybind11_add_module(cpp_kernel bind_example.cpp)
# target_include_directories(
#     cpppkg 
#     PUBLIC
#     ${CMAKE_CURRENT_SOURCE_DIR}/include 
# )
target_link_libraries(cpp_kernel PUBLIC cpp_core pybind11::module xtensor-python Python::NumPy)

# --- Install libs so python module can import it ---

# Handle where to install the resulting Python package
if(CALL_FROM_SETUP_PY)
    # The CMakeExtension will set CMAKE_INSTALL_PREFIX to the root
    # of the resulting wheel archive
    set(KERNEL_INSTALL_PREFIX ${CMAKE_INSTALL_PREFIX})
else()
    # The Python package is installed directly in the folder of the
    # detected interpreter (system, user, or virtualenv)
    set(KERNEL_INSTALL_PREFIX ${Python3_SITELIB})
endif()

# Install the pybind11 library
install(
    TARGETS cpp_kernel
    # COMPONENT bindings
    LIBRARY DESTINATION ${KERNEL_INSTALL_PREFIX}
    ARCHIVE DESTINATION ${KERNEL_INSTALL_PREFIX}
    RUNTIME DESTINATION ${KERNEL_INSTALL_PREFIX}
)