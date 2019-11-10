
set(MODULE_NAME "sqlite_module")
add_subdirectory(${MODULE_DIR}/src/ ${MODULE_BINARY_DIR}/${MODULE_NAME})
link_directories(${MODULE_DIR})
list(APPEND MODULE_LIBS sqlite_binding sqlite stdc++)
