#pragma once

typedef enum {
  START = 1,
  STOP  = 2
} Command;

void SendCommand(Command command, const char* message);
