##===-------------------------------------------------------------------------------------------===##
##
##  This file is distributed under the MIT License (MIT). 
##  See LICENSE.txt for details.
##
##===------------------------------------------------------------------------------------------===##

include(ExternalProject)

set(DIR_OF_PROTO_EXTERNAL ${CMAKE_CURRENT_LIST_DIR})  

function(install_protobuf)
  set(options)
  set(one_value_args GIT_REPOSITORY GIT_TAG DOWNLOAD_DIR)
  set(multi_value_args REQUIRED_VARS CMAKE_ARGS)
  cmake_parse_arguments(ARG "${options}" "${one_value_args}" "${multi_value_args}" ${ARGN})

  if(NOT("${ARG_UNPARSED_ARGUMENTS}" STREQUAL ""))
    message(FATAL_ERROR "invalid argument ${ARG_UNPARSED_ARGUMENTS}")
  endif()

  set(cmake_args
    ${ARG_CMAKE_ARGS}
    -DCMAKE_INSTALL_PREFIX:PATH=<INSTALL_DIR>
    -DBUILD_SHARED_LIBS=ON                                                         
    -Dprotobuf_BUILD_EXAMPLES=OFF
    -Dprotobuf_BUILD_SHARED_LIBS=ON
    -Dprotobuf_BUILD_TESTS=OFF
    -Dprotobuf_INSTALL_EXAMPLES=OFF
  )

  set(install_dir ${CMAKE_BINARY_DIR}/prefix/protobuf)
  set(source_dir ${CMAKE_BINARY_DIR}/protobuf-prefix/src/protobuf)

  # Python protobuf
  if(NOT DEFINED PYTHON_EXECUTABLE)
    find_package(PythonInterp 3.4 REQUIRED)
  endif()
  find_package(bash REQUIRED)

  set(PROTOBUF_PROTOC "${install_dir}/bin/protoc")
  set(PROTOBUF_LIBPROTOBUF_PATH "${install_dir}/lib")
  set(PROTOBUF_PYTHON_SOURCE "${source_dir}/python")
  set(PROTOBUF_PYTHON_INSTALL "${install_dir}")
  set(PROTOBUF_CMAKE_EXECUTABLE "${CMAKE_COMMAND}")
  set(PROTOBUF_PYTHON_EXECUTABLE "${PYTHON_EXECUTABLE}")

  set(install_script_in "${DIR_OF_PROTO_EXTERNAL}/templates/protobuf_python_install_script.sh.in")
  set(install_script "${CMAKE_CURRENT_BINARY_DIR}/protobuf_python_install_script.sh")
  configure_file(${install_script_in} ${install_script} @ONLY)

 
  set(_PROTOBUF_INSTALL_DIR_ ${install_dir})

  set(post_build_input_script ${CMAKE_SOURCE_DIR}/cmake/scripts/protobuf-postbuild.cmake.in)
  set(post_build_output_script ${CMAKE_BINARY_DIR}/yoda-cmake/cmake/protobuf-postbuild.cmake)

  # Configure the script
  configure_file(${post_build_input_script} ${post_build_output_script} @ONLY)
 

  # C++ protobuf
  ExternalProject_Add(protobuf
    DOWNLOAD_DIR ${ARG_DOWNLOAD_DIR}
    GIT_REPOSITORY ${ARG_GIT_REPOSITORY}
    GIT_TAG ${ARG_GIT_TAG}
    SOURCE_DIR "${source_dir}"
    INSTALL_DIR "${install_dir}"
    CONFIGURE_COMMAND ${CMAKE_COMMAND} -G ${CMAKE_GENERATOR} <SOURCE_DIR>/cmake ${cmake_args}
    STEP_TARGETS python-build post-build
  )
#  ExternalProject_Add_Step(
#    protobuf python-build
#    COMMAND ${BASH_EXECUTABLE} ${install_script}
 #   DEPENDEES build
 # )
  ExternalProject_Add_Step(
    protobuf post-build
    COMMAND ${CMAKE_COMMAND} -P ${post_build_output_script}
    DEPENDEES install
  )

  ExternalProject_Get_Property(protobuf install_dir)
  set(Protobuf_DIR "${install_dir}/lib/cmake/protobuf" CACHE INTERNAL "")
  set(ProtocBinary "${install_dir}/bin/protoc" CACHE INTERNAL "")

endfunction()
