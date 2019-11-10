var comm_helper = require('communication_helpers_module');

comm_helper.SendCommand(comm_helper.START, "scheduling_js");

var timeoutInSec = 11000;
var intervallInms = 1000;

var scheduler = setInterval(function() { ; }, intervallInms);
setTimeout(stopScheduler, timeoutInSec, scheduler);

function stopScheduler(scheduler) {
  clearInterval(scheduler);
  comm_helper.SendCommand(comm_helper.STOP, "scheduling_js");
}