if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "RelWithDebInfo" CACHE STRING 
      "Choose the type of build, options are: Debug Release RelWithDebInfo." FORCE)
endif()

if(NOT CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "${CMAKE_SOURCE_DIR}/install" CACHE STRING
      "Install path prefix, prepended onto install directories." FORCE)
endif()

project(HIR NONE)
cmake_minimum_required(VERSION 3.3)
list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

add_subdirectory(doc)

set(protobuf_version "3.4.0")
set(protobuf_version_short "3.4")

include(External_Protobuf)

install_protobuf(
    DOWNLOAD_DIR ${CMAKE_BINARY_DIR}/download
    URL "https://github.com/google/protobuf/archive/v${protobuf_version}.tar.gz"
    URL_MD5 "1d077a7d4db3d75681f5c333f2de9b1a"
)

message("${Protobuf_DIR} KL ${ProtocBinary}")
add_custom_command(OUTPUT "HIR_pb2.py" COMMAND ${CMAKE_SOURCE_DIR}/cmake/scripts/compileProto.sh "${ProtocBinary}" "${CMAKE_SOURCE_DIR}" "${CMAKE_BINARY_DIR}")
add_custom_command(OUTPUT "dummy.d" COMMAND /bin/bash ${CMAKE_BINARY_DIR}/protobuf_python_install_script.sh)
add_custom_target(proto_python ALL DEPENDS "HIR_pb2.py" "dummy.d")

