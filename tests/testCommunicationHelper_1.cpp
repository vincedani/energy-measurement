/*
 * Compiling:
 * g++ tests/testCommunicationHelper_1.cpp \
 *   scripts/CommunicationHelper.h         \
 *   scripts/CommunicationHelper.c         \
 *   -lwiringPi
 */

#include <unistd.h>

#include "../scripts/CommunicationHelper.h"

int main() {
  SendCommand(START, "CppTest");
  SendCommand(START, "CppTest_Ignored");

  usleep(2000000);

  SendCommand(STOP, "CppTest");
}
