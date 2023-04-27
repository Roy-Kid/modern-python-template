# --- add deps ---
## find python then pybind11
find_package(Python REQUIRED COMPONENTS Interpreter Development)
find_package(pybind11 REQUIRED CONFIG QUIET)
if (NOT pybind11_FOUND)
    # pybind11 not found, try to find it as a submodule
    # else add it as a submodule at enternal/pybind11
    if (EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/pybind11/CMakeLists.txt")
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
endif()

# --- compile cpp code as a shared lib and (optional)test it ---

# Use -fPIC even if statically compiled
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# If rely on external cpp submodule, 
# add_subdirectory()

# or compile it manually
if (NOT BUILD_SHARED_LIBS)
    add_library(
        cpp_core
        src/example.cpp
    )
else()

# Install shared library
# install(
#     TARGETS cpp_core
#     COMPONENT runtime
#     LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
#     ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
#     RUNTIME DESTINATION ${CMAKE_INSTALL_LIBDIR}
#     PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
# )

endif()


# Optional: set_target_properties

# Include directory of headers
target_include_directories(
    cpp_core
    PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# --- compile python module ---

pybind11_add_module(cpp_kernel bind_example.cpp)
# target_include_directories(
#     cpppkg 
#     PUBLIC
#     ${CMAKE_CURRENT_SOURCE_DIR}/include 
# )
target_link_libraries(cpp_kernel PRIVATE cpp_core)

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