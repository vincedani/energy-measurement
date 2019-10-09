#pragma once

#include <string>


typedef enum {
  START = 1,
  STOP  = 2
} Command;

void SendCommand(Command command, string message);
