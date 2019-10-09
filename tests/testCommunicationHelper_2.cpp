/*
 * Compiling:
 * g++ tests/testCommunicationHelper_2.cpp \
 *   scripts/CommunicationHelper.h         \
 *   scripts/CommunicationHelper.c         \
 *   -lwiringPi
 */

#include <unistd.h>

#include "../scripts/CommunicationHelper.h"

int main() {
  SendCommand(START, "CppTest");

  usleep(2000000);

  SendCommand(STOP, "CppTest_NonExisting");
}
