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
  Modeler VERSION 3.3
  DESCRIPTION "Cassiopee Modeler – geometry modelling module"
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
project_add_subdirectory(KCore)

# Optional OpenCASCADE for TIGL support
option(MODELER_ENABLE_OCC "Enable OpenCASCADE (TIGL) support" OFF)
if(MODELER_ENABLE_OCC)
  find_package(OpenCASCADE QUIET)
  if(NOT OpenCASCADE_FOUND)
    find_package(OCCT QUIET)
  endif()
endif()

# ------------------------------------------------------------------------------
# Compilation
# ------------------------------------------------------------------------------
set(include_dir "${PROJECT_SOURCE_DIR}/${PROJECT_NAME}")

execute_process(
  COMMAND python print_source_filenames.py
  WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
  OUTPUT_VARIABLE src_files
)
string(STRIP "${src_files}" src_files)

add_library(${PROJECT_NAME} SHARED "${src_files}")

target_include_directories(${PROJECT_NAME} PUBLIC
  $<BUILD_INTERFACE:${include_dir}>
  $<INSTALL_INTERFACE:include>
)
target_link_libraries(${PROJECT_NAME}
  PUBLIC
    Python::Python
    KCore::KCore
)

if(MODELER_ENABLE_OCC AND (OpenCASCADE_FOUND OR OCCT_FOUND))
  if(TARGET OpenCASCADE::TKernel)
    target_link_libraries(${PROJECT_NAME} PUBLIC
      OpenCASCADE::TKernel OpenCASCADE::TKMath OpenCASCADE::TKBO
      OpenCASCADE::TKBRep  OpenCASCADE::TKTopAlgo
      OpenCASCADE::TKGeomBase OpenCASCADE::TKGeomAlgo
    )
  elseif(OpenCASCADE_FOUND)
    target_link_libraries(${PROJECT_NAME} PUBLIC ${OpenCASCADE_LIBRARIES})
    target_include_directories(${PROJECT_NAME} PUBLIC ${OpenCASCADE_INCLUDE_DIR})
  endif()
endif()

# ------------------------------------------------------------------------------
# Installation
# ------------------------------------------------------------------------------
target_install(${PROJECT_NAME})

# ------------------------------------------------------------------------------
# Python wrapper and Python files
# ------------------------------------------------------------------------------
include(${PROJECT_UTILS_CMAKE_DIR}/python_wrapping.cmake)
compile_install_cpython_module(${PROJECT_NAME} "${PROJECT_SOURCE_DIR}/${PROJECT_NAME}/modeler.cpp")
install_python_modules(${PROJECT_NAME})

# ------------------------------------------------------------------------------
# Testing
# ------------------------------------------------------------------------------
if(EXISTS "${PROJECT_SOURCE_DIR}/test/CMakeLists.txt")
  include(CTest)
  add_subdirectory(test)
endif()
