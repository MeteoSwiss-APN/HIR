# HIR

The high-level intermediate representation (HIR) is a specification of concepts used by domain-specific languages (DSL) and tools to capture computational patterns present in weather and climate applications. 
The typical computational patterns are derived from discretization of different methods (finite differences, finite volumes, Galerkin methods, etc) on different grids, like compact stencil operations and vertical implicit solvers (like tridiagonal solve)
The HIR aims a prividing a complete set of concepts (as nodes) that are necessary to represent any computation present in dynamical cores or the physical parameterizations of models, as if they were implemented in a sequential manner. 
An example implementation using HIR should contain contain only the grid operations derived from the discretized equations and should not contain details related to specific implementation for a computing architecture (like memory layouts, loop ordering, etc) or programming language

## Introduction

The HIR package contains:

* current state of the art of the proposal specification for HIR
https://github.com/MeteoSwiss-APN/HIR/tree/master/doc

* A concrete implementation of the specification (using [protocol buffers](https://developers.google.com/protocol-buffers/))

https://github.com/MeteoSwiss-APN/HIR/blob/master/src/proto/HIR.proto

Notice that the implementation is behind the latest version proposed in the doc folder

* A python tool to traverse and operate on the .proto specification

https://github.com/MeteoSwiss-APN/HIR/tree/master/src/python


## How to build

```
mkdir build
cd build
cmake ..
make protobuf
make 
```

The HIR package build will 
* compile a pdf documentation with the latest specification of the HIR
(under doc)
* download a build google protobuffers software
* compile the HIR.proto specification
that will generate a python module to handle the HIR nodes and traverse the AST of any HIR that follows the specification of HIR.proto

The python module is generated under ``<HIR>/gen/src/proto/HIR_pb2.py``
  
## Python deserialization of an HIR file

An example of how to deserialize the HIR and traverse the AST can be found in
https://github.com/MeteoSwiss-APN/HIR/blob/master/src/python/deserialize.py

In order to run it

```
export PYTHONPATH=<HIR>/gen/src/proto:<HIR>/build/prefix/protobuf/python
python deserialize <hirexample.hir>
```

