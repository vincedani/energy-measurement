var sense_module = require('sense_hat_module');
// var comm_helper = require('communication_helpers_module');

var senseHat = new sense_module.SenseHAT();

for (i = 0; i < 10; i++) {
  // comm_helper.SendCommand(comm_helper.START, "temperature_from_pressure_js");
  var temp_fromhumidity = senseHat.get_temperature_from_humidity();
  // comm_helper.SendCommand(comm_helper.STOP, "temperature_from_pressure_js");

  // comm_helper.SendCommand(comm_helper.START, "temperature_from_humidity_js");
  var temp_from_pressure = senseHat.get_temperature_from_pressure();
  // comm_helper.SendCommand(comm_helper.STOP, "temperature_from_humidity_js");

  // comm_helper.SendCommand(comm_helper.START, "pressure_js");
  var pressure = senseHat.get_pressure();
  // comm_helper.SendCommand(comm_helper.STOP, "pressure_js");

  // comm_helper.SendCommand(comm_helper.START, "humidity_js");
  var humidity = senseHat.get_humidity();
  // comm_helper.SendCommand(comm_helper.STOP, "humidity_js");
}
