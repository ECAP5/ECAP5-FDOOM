#           __        _
#  ________/ /  ___ _(_)__  ___
# / __/ __/ _ \/ _ `/ / _ \/ -_)
# \__/\__/_//_/\_,_/_/_//_/\__/
# 
# Copyright (C) Clément Chaine
# This file is part of ECAP5-FDOOM <https://github.com/ecap5/ECAP5-FDOOM>
# 
# ECAP5-FDOOM is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# ECAP5-FDOOM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with ECAP5-FDOOM.  If not, see <http://www.gnu.crg/licenses/>.

cmake_minimum_required(VERSION 3.21)
include(FetchContent)

project(ECAP5_FDOOM)

set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/cmake")
set(CMAKE_PREFIX_PATH "${CMAKE_CURRENT_LIST_DIR}/cmake")

# Create python virtual env
set(VENV_DIR ${CMAKE_BINARY_DIR}/venv)
if(NOT EXISTS "${VENV_DIR}")
  find_package(Python3 COMPONENTS Interpreter)
  execute_process(COMMAND "${Python3_EXECUTABLE}" -m venv ${VENV_DIR})
  set(Python3_FIND_VIRTUALENV ONLY)
  unset(Python3_EXECUTABLE)
endif()
set(ENV{VIRTUAL_ENV} "${VENV_DIR}")
find_package(Python3 COMPONENTS Interpreter Development)

# Dependencies

include(${CMAKE_CURRENT_LIST_DIR}/cmake/dependency.cmake)

add_dependency(
  GIT ecap5/squashware
  TAG newresolution)

# Generate the WAD file

set(WAD_FILE ${ecap5_squashware_SOURCE_DIR}/build/kernel/doom.wad)
add_custom_command(
  OUTPUT ${WAD_FILE}
  COMMAND ${CMAKE_MAKE_PROGRAM} -C ${ecap5_squashware_SOURCE_DIR}
  DEPENDS ${ecap5_squashware_SOURCE_DIR}/Makefile
  COMMENT "Generating WAD file"
  VERBATIM
)

# Generate WAD object file
set(WAD_OBJECT ${CMAKE_CURRENT_BINARY_DIR}/wad.o)
add_custom_command(
  OUTPUT  ${WAD_OBJECT}
  COMMAND riscv64-unknown-elf-objcopy -I binary -O elf32-littleriscv -B riscv --rename-section .data=.wad ${WAD_FILE} ${WAD_OBJECT}
  DEPENDS ${WAD_FILE}
)

# Compile the doom elf

set(CROSS_COMPILE riscv64-unknown-elf-)
set(CMAKE_ASM_COMPILER  ${CROSS_COMPILE}gcc)
set(CMAKE_AR            ${CROSS_COMPILE}ar)
set(CMAKE_ASM_COMPILER  ${CROSS_COMPILE}gcc)
set(CMAKE_C_COMPILER    ${CROSS_COMPILE}gcc)
set(CMAKE_CXX_COMPILER  ${CROSS_COMPILE}g++)

enable_language(ASM)

set(ARCH_FLAGS -march=rv32i -mabi=ilp32 -mcmodel=medany)
set(COMMON_OPTS -fstack-usage -Os -static -fvisibility=hidden -fno-ident -fno-asynchronous-unwind-tables -fno-unwind-tables -ffunction-sections -fdata-sections)
add_compile_options(${ARCH_FLAGS} ${COMMON_OPTS})

set(LD_SCRIPT ${CMAKE_CURRENT_LIST_DIR}/link.ld)

set(INC_DIRS include/)
list(TRANSFORM INC_DIRS PREPEND "${CMAKE_CURRENT_LIST_DIR}/")
file(GLOB_RECURSE SOURCES "src/*.c")

add_executable(doom.elf ${SOURCES} ${WAD_OBJECT})
target_include_directories(doom.elf PRIVATE ${INC_DIRS})
target_link_options(doom.elf PRIVATE
  ${ARCH_FLAGS}
  "-T${LD_SCRIPT}"
  "-nostartfiles"
  "--specs=nano.specs"
  "-nodefaultlibs"
  "-Wl,--gc-sections"
  "-Wl,-Map=${CMAKE_CURRENT_BINARY_DIR}/doom.map"
)
target_link_libraries(doom.elf c m gcc)
