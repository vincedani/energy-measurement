var http = require('http');
var comm_helper = require('communication_helpers_module');

var apiEndpoint = '192.168.2.58';
var apiPath = '/MockServer/api/weather/'

function httpGet() {
  comm_helper.SendCommand(comm_helper.START, "http_get_js");

  http.get({
    host: apiEndpoint,
    path: apiPath + '12'
  }, function(response) {
    response.on('data', function(chunk) {
      var responseData = chunk.toString();
    });
  });

  comm_helper.SendCommand(comm_helper.STOP, "http_get_js");
}

function httpPost() {
  data = [
    { 'TimeStamp' : '23:33:14.695226', 'Temperature' : 24.893, 'Humidity' : 56.576, 'Pressure' : 998.634 },
    { 'TimeStamp' : '23:33:33.805037', 'Temperature' : 24.963, 'Humidity' : 56.488, 'Pressure' : 998.640 },
    { 'TimeStamp' : '23:34:02.239622', 'Temperature' : 25.177, 'Humidity' : 55.715, 'Pressure' : 998.687 },
    { 'TimeStamp' : '23:34:54.227033', 'Temperature' : 24.939, 'Humidity' : 55.843, 'Pressure' : 998.686 },
    { 'TimeStamp' : '23:39:44.063628', 'Temperature' : 24.980, 'Humidity' : 55.676, 'Pressure' : 998.705 }
  ].toString()

  comm_helper.SendCommand(comm_helper.START, "http_post_js");

  var request = http.request({
    host: apiEndpoint,
    path: apiPath,
    method: 'POST',
    headers: {'Content-Type': 'application/json', 'Accept':'application/json', 'Content-Length': data.length}
  }, function(response) {
    if (response.statusCode != 200)
      console.log('Response: ' + response);
  });

  request.write(data);
  request.end();

  comm_helper.SendCommand(comm_helper.STOP, "http_post_js");
}

for (i = 0; i < 10; i++) {
  httpGet();
  httpPost();
}
