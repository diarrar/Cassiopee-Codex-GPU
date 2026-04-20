# ==============================================================================
# Top-level CMakeLists.txt for Cassiopee
#
# Configures all Cassiopee modules in dependency order so that the entire
# project can be built and installed with a single CMake invocation:
#
#   cmake -B build -DCMAKE_INSTALL_PREFIX=<prefix> .
#   cmake --build build -j$(nproc)
#   cmake --install build
#
# Individual modules can still be built in isolation by running CMake from
# their own sub-directory (the per-module CMakeLists.txt files are
# self-contained).
# ==============================================================================
cmake_minimum_required(VERSION 3.18 FATAL_ERROR)
cmake_policy(SET CMP0074 NEW)

# ------------------------------------------------------------------------------
# Project root detection
# ------------------------------------------------------------------------------
set(CASSIOPEE_ROOT "${CMAKE_CURRENT_SOURCE_DIR}" CACHE PATH
    "Root directory of the Cassiopee source tree (contains this CMakeLists.txt)")

set(PROJECT_ROOT "${CASSIOPEE_ROOT}")
set(PROJECT_UTILS_DIR  "${PROJECT_ROOT}/ThirdParty/project_utils")
set(PROJECT_UTILS_CMAKE_DIR "${PROJECT_UTILS_DIR}/cmake")
list(APPEND CMAKE_MODULE_PATH "${PROJECT_UTILS_CMAKE_DIR}/find_package")
include(${PROJECT_UTILS_CMAKE_DIR}/dependency_management.cmake)

# ------------------------------------------------------------------------------
# Top-level project declaration
# ------------------------------------------------------------------------------
project(Cassiopee
  VERSION 4.2
  DESCRIPTION "Cassiopee CFD pre/post-processing Python modules"
  LANGUAGES C CXX Fortran
)

# ------------------------------------------------------------------------------
# Global compiler settings (inherited by all sub-projects)
# ------------------------------------------------------------------------------
set(CMAKE_CXX_STANDARD           14)
set(CMAKE_CXX_EXTENSIONS        OFF)
set(CMAKE_CXX_STANDARD_REQUIRED  ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_Fortran_PREPROCESS ON)
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

# ------------------------------------------------------------------------------
# Common third-party dependencies (found once for the whole tree)
# ------------------------------------------------------------------------------
find_package(Python REQUIRED COMPONENTS Interpreter Development NumPy)
find_package(OpenMP REQUIRED)
find_package(ZLIB   REQUIRED)

option(CASSIOPEE_ENABLE_MPI "Build with MPI support" ON)
if(CASSIOPEE_ENABLE_MPI)
  find_package(MPI   REQUIRED)
  find_package(HDF5  REQUIRED)   # parallel HDF5 requires MPI
  find_package(Mpi4Py REQUIRED)
endif()

# ------------------------------------------------------------------------------
# Module build order (each module forwards CASSIOPEE_ROOT so that
# project_add_subdirectory / project_find_package resolve siblings)
# ------------------------------------------------------------------------------

# Helper macro: adds a module subdirectory while propagating the root path
macro(cassiopee_add_module mod_name)
  add_subdirectory(
    "${CASSIOPEE_ROOT}/${mod_name}"
    "${CMAKE_BINARY_DIR}/${mod_name}"
  )
endmacro()

# -- Tier 0: core library (no Cassiopee module dependencies) --
cassiopee_add_module(KCore)

# -- Tier 1: modules that depend only on KCore --
cassiopee_add_module(Converter)
cassiopee_add_module(Geom)
cassiopee_add_module(Transform)
cassiopee_add_module(Generator)
cassiopee_add_module(Post)
cassiopee_add_module(Initiator)
cassiopee_add_module(Connector)
cassiopee_add_module(Distributor2)
cassiopee_add_module(Dist2Walls)
cassiopee_add_module(RigidMotion)
cassiopee_add_module(Compressor)
cassiopee_add_module(Intersector)
cassiopee_add_module(XCore)

# -- Tier 2: modules with additional dependencies --
cassiopee_add_module(OCC)
cassiopee_add_module(CPlot)

# -- Tier 3: pure-Python or optional modules --
cassiopee_add_module(Modeler)
cassiopee_add_module(Roms)
cassiopee_add_module(Apps)
cassiopee_add_module(Template)

# ------------------------------------------------------------------------------
# Install environment activation scripts
# ------------------------------------------------------------------------------
install(
  DIRECTORY "${CASSIOPEE_ROOT}/Envs/"
  DESTINATION "."
  FILES_MATCHING
    PATTERN "env_Cassiopee*"
    PATTERN "sh_Cassiopee*"
)
