# HIR

## Introduction

The HIR package contains:

* current state of the art of the proposal specification for HIR
https://github.com/MeteoSwiss-APN/HIR/tree/master/doc

* A concrete implementation of the specification (using google protobuffers)
https://github.com/MeteoSwiss-APN/HIR/blob/master/src/proto/HIR.proto
Notice that the implementation is behind the latest version proposed in the doc folder

* A python tool to traverse and operate on the .proto specification
https://github.com/MeteoSwiss-APN/HIR/tree/master/src/python


## How to build

```
mkdir build
cd build
cmake ..
make 
```

The HIR package build will 
* compile a pdf documentation with the latest specification of the HIR
(under doc)
* download a build google protobuffers software
* compile the HIR.proto specification
that will generate a python module to handle the protobuffer nodes and travers the AST of any HIR that follows the specification of HIR.proto

The python module is generated under ``<HIR>/gen/src/proto/HIR_pb2.py``
  
## Python deserialization of an HIR file

An example of how to deserialize the HIR and traverse the AST can be found in
https://github.com/MeteoSwiss-APN/HIR/blob/master/src/python/deserialize.py

In order to run it

```
export PYTHONPATH=<HIR>/gen/src/proto:<HIR>/build/prefix/protobuf/python
python deserialize <hirexample.hir>
```

