
project(C++ CXX)

add_library(sqlite_binding STATIC
    sqlite_js_binding.cpp
)
target_include_directories(sqlite_binding PRIVATE ${JERRY_INCLUDE_DIR})
target_link_libraries(sqlite_binding PUBLIC stdc++)
