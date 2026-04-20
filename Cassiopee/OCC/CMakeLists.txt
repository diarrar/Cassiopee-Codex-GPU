# ------------------------------------------------------------------------------
# General CMake settings
# ------------------------------------------------------------------------------
cmake_minimum_required(VERSION 3.18 FATAL_ERROR)
cmake_policy(SET CMP0074 NEW)

if(NOT DEFINED PROJECT_ROOT)
  if(DEFINED CASSIOPEE_ROOT)
    set(PROJECT_ROOT ${CASSIOPEE_ROOT} CACHE PATH)
  else()
    set(PROJECT_ROOT ${PROJECT_SOURCE_DIR} CACHE PATH)
  endif()
endif()

set(PROJECT_UTILS_DIR ${PROJECT_ROOT}/ThirdParty/project_utils)
set(PROJECT_UTILS_CMAKE_DIR ${PROJECT_UTILS_DIR}/cmake)
list(APPEND CMAKE_MODULE_PATH "${PROJECT_UTILS_CMAKE_DIR}/find_package")
include(${PROJECT_UTILS_CMAKE_DIR}/dependency_management.cmake)

set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")

# ------------------------------------------------------------------------------
# Project
# ------------------------------------------------------------------------------
project(
  OCC VERSION 3.3
  DESCRIPTION "Cassiopee OCC – OpenCASCADE Python bindings"
  LANGUAGES C CXX
)

set(CMAKE_CXX_STANDARD          14)
set(CMAKE_CXX_EXTENSIONS        OFF)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

# ------------------------------------------------------------------------------
# Dependencies
# ------------------------------------------------------------------------------
project_find_package(Python REQUIRED COMPONENTS Interpreter Development NumPy)

# OpenCASCADE – look for the modern CMake config or fall back to pkg-config.
# Packages names differ by distro: OpenCASCADE (Debian/Ubuntu) vs
# OpenCASCADE-Foundation etc.  We try a few known component names.
find_package(OpenCASCADE QUIET)
if(NOT OpenCASCADE_FOUND)
  find_package(OCCT QUIET)
endif()
if(NOT OpenCASCADE_FOUND AND NOT OCCT_FOUND)
  message(WARNING
    "OpenCASCADE / OCCT not found.  "
    "OCC module will not be built.  "
    "Install libocct-*-dev (Debian/Ubuntu) or equivalent and re-run CMake.")
  return()
endif()

project_add_subdirectory(KCore)
project_add_subdirectory(Generator)

# ------------------------------------------------------------------------------
# Compilation – only the Python wrapper (occ.cpp) is compiled here;
# the module links against the system OpenCASCADE libraries.
# ------------------------------------------------------------------------------
set(include_dir "${PROJECT_SOURCE_DIR}/${PROJECT_NAME}")

add_library(${PROJECT_NAME} SHARED
  "${PROJECT_SOURCE_DIR}/${PROJECT_NAME}/OCCSurface.cpp"
  "${PROJECT_SOURCE_DIR}/${PROJECT_NAME}/OCCSurface2.cpp"
  "${PROJECT_SOURCE_DIR}/${PROJECT_NAME}/CADviaOCC.cpp"
  "${PROJECT_SOURCE_DIR}/${PROJECT_NAME}/CADviaOCC2.cpp"
  "${PROJECT_SOURCE_DIR}/${PROJECT_NAME}/import_OCC_CAD_wrapper.cpp"
)

target_include_directories(${PROJECT_NAME} PUBLIC
  $<BUILD_INTERFACE:${include_dir}>
  $<INSTALL_INTERFACE:include>
)

target_link_libraries(${PROJECT_NAME}
  PUBLIC
    Python::Python
    KCore::KCore
    Generator::Generator
)

# Link against whichever OpenCASCADE target is available
if(TARGET OpenCASCADE::TKBO)
  target_link_libraries(${PROJECT_NAME} PUBLIC
    OpenCASCADE::TKernel OpenCASCADE::TKMath OpenCASCADE::TKBO
    OpenCASCADE::TKBRep  OpenCASCADE::TKTopAlgo
    OpenCASCADE::TKGeomBase OpenCASCADE::TKGeomAlgo
    OpenCASCADE::TKIGES OpenCASCADE::TKSTEP OpenCASCADE::TKSTEPBase
    OpenCASCADE::TKXSBase OpenCASCADE::TKSTL OpenCASCADE::TKMesh
    OpenCASCADE::TKShHealing OpenCASCADE::TKOffset OpenCASCADE::TKFillet
  )
elseif(OpenCASCADE_FOUND)
  target_link_libraries(${PROJECT_NAME} PUBLIC ${OpenCASCADE_LIBRARIES})
  target_include_directories(${PROJECT_NAME} PUBLIC ${OpenCASCADE_INCLUDE_DIR})
endif()

# ------------------------------------------------------------------------------
# Installation
# ------------------------------------------------------------------------------
target_install(${PROJECT_NAME})

# ------------------------------------------------------------------------------
# Python wrapper and Python files
# ------------------------------------------------------------------------------
include(${PROJECT_UTILS_CMAKE_DIR}/python_wrapping.cmake)
compile_install_cpython_module(${PROJECT_NAME} "${PROJECT_SOURCE_DIR}/${PROJECT_NAME}/occ.cpp")
install_python_modules(${PROJECT_NAME})

# ------------------------------------------------------------------------------
# Testing
# ------------------------------------------------------------------------------
if(EXISTS "${PROJECT_SOURCE_DIR}/test/CMakeLists.txt")
  include(CTest)
  add_subdirectory(test)
endif()
