
set(MODULE_NAME "communication_helpers_module")
set(COMM_HELPER_BUILD_DIR "/home/pi/energy-measurement/scripts/communication_helpers")

add_subdirectory(${MODULE_DIR}/src/ ${MODULE_BINARY_DIR}/${MODULE_NAME})
link_directories(${MODULE_DIR} ${COMM_HELPER_BUILD_DIR})
list(APPEND MODULE_LIBS communication_helpers_binding communication_helper stdc++)
