# ------------------------------------------------------------------------------
# General CMake settings
# ------------------------------------------------------------------------------
cmake_minimum_required(VERSION 3.18 FATAL_ERROR)
cmake_policy(SET CMP0074 NEW)

if(NOT DEFINED PROJECT_ROOT)
  if(DEFINED CASSIOPEE_ROOT)
    set(PROJECT_ROOT ${CASSIOPEE_ROOT} CACHE PATH)
  else()
    set(PROJECT_ROOT ${PROJECT_SOURCE_DIR}/.. CACHE PATH "Cassiopee root (parent of the module directory)")
  endif()
endif()

set(PROJECT_UTILS_DIR ${PROJECT_ROOT}/ThirdParty/project_utils)
set(PROJECT_UTILS_CMAKE_DIR ${PROJECT_UTILS_DIR}/cmake)
list(APPEND CMAKE_MODULE_PATH "${PROJECT_UTILS_CMAKE_DIR}/find_package")
include(${PROJECT_UTILS_CMAKE_DIR}/dependency_management.cmake)

set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")

# ------------------------------------------------------------------------------
# Project – pure-Python, no compiled extensions
# ------------------------------------------------------------------------------
project(
  Apps VERSION 3.3
  DESCRIPTION "Cassiopee Apps – high-level application modules"
)

# ------------------------------------------------------------------------------
# Dependencies
# ------------------------------------------------------------------------------
project_find_package(Python REQUIRED COMPONENTS Interpreter)

# ------------------------------------------------------------------------------
# Installation – install Python files only
# ------------------------------------------------------------------------------
set(PROJECT_UTILS_CMAKE_DIR_INSTALLED ${PROJECT_UTILS_CMAKE_DIR})
include(${PROJECT_UTILS_CMAKE_DIR}/python_wrapping.cmake)
install_python_modules(${PROJECT_NAME})

# ------------------------------------------------------------------------------
# Testing
# ------------------------------------------------------------------------------
if(EXISTS "${PROJECT_SOURCE_DIR}/test/CMakeLists.txt")
  include(CTest)
  add_subdirectory(test)
endif()
