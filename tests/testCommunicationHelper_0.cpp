/*
 * Compiling:
 * g++ tests/testCommunicationHelper_0.cpp               \
 *   scripts/communication_helpers/CommunicationHelper.h \
 *   scripts/communication_helpers/CommunicationHelper.c \
 *   -lwiringPi
 */

#include <unistd.h>

#include "../scripts/communication_helpers/CommunicationHelper.h"

int main() {
  SendCommand(START, "CppTest");

  usleep(2000000);

  SendCommand(STOP, "CppTest");
}
