/*
 * Compiling:
 * g++ -L../../SenseHat/build -lsense-hat 01_sensors.cpp       \
 *   ../../scripts/communication_helpers/CommunicationHelper.h \
 *   ../../scripts/communication_helpers/CommunicationHelper.c \
 *   -lwiringPi
 */

#include "../../SenseHat/src/sense-hat.h"
#include "../../scripts/communication_helpers/CommunicationHelper.h"

int main()
{
  SenseHAT senseHat;

  for(int i = 0; i < 10; i++) {
    SendCommand(START, "temperature_from_pressure_cpp");
    double temperatureFromPressure = senseHat.get_temperature_from_pressure();
    SendCommand(STOP, "temperature_from_pressure_cpp");

    SendCommand(START, "temperature_from_humidity_cpp");
    double temperatureFromHumidity = senseHat.get_temperature_from_humidity();
    SendCommand(STOP, "temperature_from_humidity_cpp");

    SendCommand(START, "pressure_cpp");
    double pressure = senseHat.get_pressure();
    SendCommand(STOP, "pressure_cpp");

    SendCommand(START, "humidity_cpp");
    double humidity = senseHat.get_humidity();
    SendCommand(STOP, "humidity_cpp");
  }

  return 0;
}
