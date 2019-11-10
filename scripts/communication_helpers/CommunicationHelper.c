#include <stdio.h>
#include <unistd.h>

#include "CommunicationHelper.h"
#include <wiringSerial.h>

void SendCommand(Command command, const char* message) {
  int fd = serialOpen ("/dev/ttyS0", 115200);

  if (fd == -1) {
    fprintf(stderr, "Unable to open serial port\n");
    return;
  }

  char* json = "{ \"command\" : %d, \"msg\": \"%s\" }\n";
  serialPrintf(fd, json, command, message);

  // 0.1 second sleep is neccessary for waiting the
  // response of the energy measurement device.
  usleep(100000);

  int hasResponse = 0;
  while (serialDataAvail (fd)) {
    hasResponse = 1;
    fprintf(stderr, "%c", serialGetchar(fd));
  }

  if (hasResponse)
    fprintf(stderr, "\n");
}
