# @file

# Python bindings using `ctypes`

find_package(Python3 REQUIRED COMPONENTS Development)
include_directories(${Python3_INCLUDE_DIRS}) # permits `#include <pyconfig.h>`
