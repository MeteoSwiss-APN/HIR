#!/bin/bash

proto_binary=$1
source_dir=$2
binary_dir=$3 

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${binary_dir}/prefix/protobuf/lib/
echo "${proto_binary} --python_out=${source_dir}/src/proto/gen ${source_dir}/src/proto/HIR.proto -I=${source_dir}"
mkdir -p ${source_dir}/gen
${proto_binary} --python_out=${source_dir}/gen ${source_dir}/src/proto/HIR/HIR.proto -I=${source_dir} > /tmp/log
${proto_binary} --python_out=${source_dir}/gen ${source_dir}/src/proto/IIR/IIR.proto -I=${source_dir} -I=${source_dir}/src/proto/IIR/ > /tmp/log
${proto_binary} --python_out=${source_dir}/gen ${source_dir}/src/proto/IIR/statements.proto -I=${source_dir} > /tmp/log

