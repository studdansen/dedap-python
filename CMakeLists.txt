#: @file
#: @brief CMake build configuration for the `dedap-python` project.

cmake_minimum_required(VERSION 3.28)
project(dedap_python_project
	DESCRIPTION "Mapping with directed acyclic graphs"
)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
#~ include_directories(${Python3_INCLUDE_DIRS}) # permits `#include <pyconfig.h>`


# find Sphinx


#~ # ===== documentation =====

set(BUILD_DOCS NO CACHE BOOL "Build documentation")
if(BUILD_DOCS)
	
	set(CONF_PY_IN "${CMAKE_CURRENT_SOURCE_DIR}/doc/conf.py.in")
	set(CONF_PY    "${CMAKE_CURRENT_BINARY_DIR}/doc/conf.py")
	configure_file(${CONF_PY_IN} ${CONF_PY})
	
	add_custom_target(dedap_python_html_docs ALL
		${Python3_EXECUTABLE} -m 'sphinx.cmd.build'
		-M html			# builder
		"${CMAKE_CURRENT_SOURCE_DIR}/doc"		# source directory
		"${CMAKE_CURRENT_BINARY_DIR}/doc"		# build directory
		-c "${CMAKE_CURRENT_BINARY_DIR}/doc"	# conf.py directory
	)
	
endif()
