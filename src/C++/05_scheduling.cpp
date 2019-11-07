/*
 * Compiling:
 * g++ 05_scheduling.cpp                                       \
 *   ../../scripts/communication_helpers/CommunicationHelper.h \
 *   ../../scripts/communication_helpers/CommunicationHelper.c \
 *   -lwiringPi
 */

#include <ctime>
#include <chrono>
#include <iostream>
#include <thread>

#include "../../scripts/communication_helpers/CommunicationHelper.h"

using namespace std;
using namespace std::chrono;

void func() {
  ;
}

void start(int interval, function<void(void)> func) {
  std::thread([interval, func]() {
    while (true) {
      func();
      this_thread::sleep_for(milliseconds(interval));
    }
  }).detach();
}

int main () {

  SendCommand(START, "scheduling_cpp");

  int timeout = 10;
  auto startTime = system_clock::now();

  start(1000, &func);

  duration<double> ellapsedTime;
  do {
    ellapsedTime = system_clock::now() - startTime;
  } while (ellapsedTime.count() < timeout);

  SendCommand(STOP, "scheduling_cpp");

  return 0;
}