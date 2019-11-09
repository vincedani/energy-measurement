
project(communication_helpers CXX)

add_library(communication_helpers_binding STATIC
    communication_helpers_js_binding.cpp
)
target_include_directories(communication_helpers_binding PRIVATE ${JERRY_INCLUDE_DIR})
target_link_libraries(communication_helpers_binding PUBLIC stdc++)
