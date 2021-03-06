var sense_module = require('sense_hat_module');
var comm_helper = require('communication_helpers_module');
var sleep = require('sleep');

var senseHat = new sense_module.SenseHAT();

var ASCII_CHARACTERS = {
  '-': [ 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
  '>': [ 0x21, 0x18, 0x3c, 0x3c, 0x18, 0x18, 0x00, 0x18, 0x00 ],
  '"': [ 0x22, 0x6c, 0x6c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
  '#': [ 0x23, 0x6c, 0x6c, 0xfe, 0x6c, 0xfe, 0x6c, 0x6c, 0x00 ],
  '$': [ 0x24, 0x30, 0x7c, 0xc0, 0x78, 0x0c, 0xf8, 0x30, 0x00 ],
  '%': [ 0x25, 0x00, 0xc6, 0xcc, 0x18, 0x30, 0x66, 0xc6, 0x00 ],
  '&': [ 0x26, 0x38, 0x6c, 0x38, 0x76, 0xdc, 0xcc, 0x76, 0x00 ],
  '' : [ 0x27, 0x60, 0x60, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00 ],
  '(': [ 0x28, 0x18, 0x30, 0x60, 0x60, 0x60, 0x30, 0x18, 0x00 ],
  ')': [ 0x29, 0x60, 0x30, 0x18, 0x18, 0x18, 0x30, 0x60, 0x00 ],
  '*': [ 0x2a, 0x00, 0x66, 0x3c, 0xff, 0x3c, 0x66, 0x00, 0x00 ],
  '+': [ 0x2b, 0x00, 0x30, 0x30, 0xfc, 0x30, 0x30, 0x00, 0x00 ],
  ',': [ 0x2c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x30, 0x60 ],
  '-': [ 0x2d, 0x00, 0x00, 0x00, 0xfc, 0x00, 0x00, 0x00, 0x00 ],
  '.': [ 0x2e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x30, 0x30, 0x00 ],
  '>': [ 0x2f, 0x06, 0x0c, 0x18, 0x30, 0x60, 0xc0, 0x80, 0x00 ],
  '0': [ 0x30, 0x7c, 0xc6, 0xce, 0xde, 0xf6, 0xe6, 0x7c, 0x00 ],
  '1': [ 0x31, 0x30, 0x70, 0x30, 0x30, 0x30, 0x30, 0xfc, 0x00 ],
  '2': [ 0x32, 0x78, 0xcc, 0x0c, 0x38, 0x60, 0xcc, 0xfc, 0x00 ],
  '3': [ 0x33, 0x78, 0xcc, 0x0c, 0x38, 0x0c, 0xcc, 0x78, 0x00 ],
  '4': [ 0x34, 0x1c, 0x3c, 0x6c, 0xcc, 0xfe, 0x0c, 0x1e, 0x00 ],
  '5': [ 0x35, 0xfc, 0xc0, 0xf8, 0x0c, 0x0c, 0xcc, 0x78, 0x00 ],
  '6': [ 0x36, 0x38, 0x60, 0xc0, 0xf8, 0xcc, 0xcc, 0x78, 0x00 ],
  '7': [ 0x37, 0xfc, 0xcc, 0x0c, 0x18, 0x30, 0x30, 0x30, 0x00 ],
  '8': [ 0x38, 0x78, 0xcc, 0xcc, 0x78, 0xcc, 0xcc, 0x78, 0x00 ],
  '9': [ 0x39, 0x78, 0xcc, 0xcc, 0x7c, 0x0c, 0x18, 0x70, 0x00 ],
  ':': [ 0x3a, 0x00, 0x30, 0x30, 0x00, 0x00, 0x30, 0x30, 0x00 ],
  ';': [ 0x3b, 0x00, 0x30, 0x30, 0x00, 0x00, 0x30, 0x30, 0x60 ],
  '<': [ 0x3c, 0x18, 0x30, 0x60, 0xc0, 0x60, 0x30, 0x18, 0x00 ],
  '=': [ 0x3d, 0x00, 0x00, 0xfc, 0x00, 0x00, 0xfc, 0x00, 0x00 ],
  '>': [ 0x3e, 0x60, 0x30, 0x18, 0x0c, 0x18, 0x30, 0x60, 0x00 ],
  '?': [ 0x3f, 0x78, 0xcc, 0x0c, 0x18, 0x30, 0x00, 0x30, 0x00 ],
  '@': [ 0x40, 0x7c, 0xc6, 0xde, 0xde, 0xde, 0xc0, 0x78, 0x00 ],
  'A': [ 0x41, 0x30, 0x78, 0xcc, 0xcc, 0xfc, 0xcc, 0xcc, 0x00 ],
  'B': [ 0x42, 0xfc, 0x66, 0x66, 0x7c, 0x66, 0x66, 0xfc, 0x00 ],
  'C': [ 0x43, 0x3c, 0x66, 0xc0, 0xc0, 0xc0, 0x66, 0x3c, 0x00 ],
  'D': [ 0x44, 0xf8, 0x6c, 0x66, 0x66, 0x66, 0x6c, 0xf8, 0x00 ],
  'E': [ 0x45, 0xfe, 0x62, 0x68, 0x78, 0x68, 0x62, 0xfe, 0x00 ],
  'F': [ 0x46, 0xfe, 0x62, 0x68, 0x78, 0x68, 0x60, 0xf0, 0x00 ],
  'G': [ 0x47, 0x3c, 0x66, 0xc0, 0xc0, 0xce, 0x66, 0x3e, 0x00 ],
  'H': [ 0x48, 0xcc, 0xcc, 0xcc, 0xfc, 0xcc, 0xcc, 0xcc, 0x00 ],
  'I': [ 0x49, 0x78, 0x30, 0x30, 0x30, 0x30, 0x30, 0x78, 0x00 ],
  'J': [ 0x4a, 0x1e, 0x0c, 0x0c, 0x0c, 0xcc, 0xcc, 0x78, 0x00 ],
  'K': [ 0x4b, 0xe6, 0x66, 0x6c, 0x78, 0x6c, 0x66, 0xe6, 0x00 ],
  'L': [ 0x4c, 0xf0, 0x60, 0x60, 0x60, 0x62, 0x66, 0xfe, 0x00 ],
  'M': [ 0x4d, 0xc6, 0xee, 0xfe, 0xfe, 0xd6, 0xc6, 0xc6, 0x00 ],
  'N': [ 0x4e, 0xc6, 0xe6, 0xf6, 0xde, 0xce, 0xc6, 0xc6, 0x00 ],
  'O': [ 0x4f, 0x38, 0x6c, 0xc6, 0xc6, 0xc6, 0x6c, 0x38, 0x00 ],
  'P': [ 0x50, 0xfc, 0x66, 0x66, 0x7c, 0x60, 0x60, 0xf0, 0x00 ],
  'Q': [ 0x51, 0x78, 0xcc, 0xcc, 0xcc, 0xdc, 0x78, 0x1c, 0x00 ],
  'R': [ 0x52, 0xfc, 0x66, 0x66, 0x7c, 0x6c, 0x66, 0xe6, 0x00 ],
  'S': [ 0x53, 0x78, 0xcc, 0xe0, 0x70, 0x1c, 0xcc, 0x78, 0x00 ],
  'T': [ 0x54, 0xfc, 0xb4, 0x30, 0x30, 0x30, 0x30, 0x78, 0x00 ],
  'U': [ 0x55, 0xcc, 0xcc, 0xcc, 0xcc, 0xcc, 0xcc, 0xfc, 0x00 ],
  'V': [ 0x56, 0xcc, 0xcc, 0xcc, 0xcc, 0xcc, 0x78, 0x30, 0x00 ],
  'W': [ 0x57, 0xc6, 0xc6, 0xc6, 0xd6, 0xfe, 0xee, 0xc6, 0x00 ],
  'X': [ 0x58, 0xc6, 0xc6, 0x6c, 0x38, 0x38, 0x6c, 0xc6, 0x00 ],
  'Y': [ 0x59, 0xcc, 0xcc, 0xcc, 0x78, 0x30, 0x30, 0x78, 0x00 ],
  'Z': [ 0x5a, 0xfe, 0xc6, 0x8c, 0x18, 0x32, 0x66, 0xfe, 0x00 ],
  '[': [ 0x5b, 0x78, 0x60, 0x60, 0x60, 0x60, 0x60, 0x78, 0x00 ],
  '<': [ 0x5c, 0xc0, 0x60, 0x30, 0x18, 0x0c, 0x06, 0x02, 0x00 ],
  ']': [ 0x5d, 0x78, 0x18, 0x18, 0x18, 0x18, 0x18, 0x78, 0x00 ],
  '^': [ 0x5e, 0x10, 0x38, 0x6c, 0xc6, 0x00, 0x00, 0x00, 0x00 ],
  '_': [ 0x5f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff ],
  '`': [ 0x60, 0x30, 0x30, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00 ],
  'a': [ 0x61, 0x00, 0x00, 0x78, 0x0c, 0x7c, 0xcc, 0x76, 0x00 ],
  'b': [ 0x62, 0xe0, 0x60, 0x60, 0x7c, 0x66, 0x66, 0xdc, 0x00 ],
  'c': [ 0x63, 0x00, 0x00, 0x78, 0xcc, 0xc0, 0xcc, 0x78, 0x00 ],
  'd': [ 0x64, 0x1c, 0x0c, 0x0c, 0x7c, 0xcc, 0xcc, 0x76, 0x00 ],
  'e': [ 0x65, 0x00, 0x00, 0x78, 0xcc, 0xfc, 0xc0, 0x78, 0x00 ],
  'f': [ 0x66, 0x38, 0x6c, 0x60, 0xf0, 0x60, 0x60, 0xf0, 0x00 ],
  'g': [ 0x67, 0x00, 0x00, 0x76, 0xcc, 0xcc, 0x7c, 0x0c, 0xf8 ],
  'h': [ 0x68, 0xe0, 0x60, 0x6c, 0x76, 0x66, 0x66, 0xe6, 0x00 ],
  'i': [ 0x69, 0x30, 0x00, 0x70, 0x30, 0x30, 0x30, 0x78, 0x00 ],
  'j': [ 0x6a, 0x0c, 0x00, 0x0c, 0x0c, 0x0c, 0xcc, 0xcc, 0x78 ],
  'k': [ 0x6b, 0xe0, 0x60, 0x66, 0x6c, 0x78, 0x6c, 0xe6, 0x00 ],
  'l': [ 0x6c, 0x70, 0x30, 0x30, 0x30, 0x30, 0x30, 0x78, 0x00 ],
  'm': [ 0x6d, 0x00, 0x00, 0xcc, 0xfe, 0xfe, 0xd6, 0xc6, 0x00 ],
  'n': [ 0x6e, 0x00, 0x00, 0xf8, 0xcc, 0xcc, 0xcc, 0xcc, 0x00 ],
  'o': [ 0x6f, 0x00, 0x00, 0x78, 0xcc, 0xcc, 0xcc, 0x78, 0x00 ],
  'p': [ 0x70, 0x00, 0x00, 0xdc, 0x66, 0x66, 0x7c, 0x60, 0xf0 ],
  'q': [ 0x71, 0x00, 0x00, 0x76, 0xcc, 0xcc, 0x7c, 0x0c, 0x1e ],
  'r': [ 0x72, 0x00, 0x00, 0xdc, 0x76, 0x66, 0x60, 0xf0, 0x00 ],
  's': [ 0x73, 0x00, 0x00, 0x7c, 0xc0, 0x78, 0x0c, 0xf8, 0x00 ],
  't': [ 0x74, 0x10, 0x30, 0x7c, 0x30, 0x30, 0x34, 0x18, 0x00 ],
  'u': [ 0x75, 0x00, 0x00, 0xcc, 0xcc, 0xcc, 0xcc, 0x76, 0x00 ],
  'v': [ 0x76, 0x00, 0x00, 0xcc, 0xcc, 0xcc, 0x78, 0x30, 0x00 ],
  'w': [ 0x77, 0x00, 0x00, 0xc6, 0xd6, 0xfe, 0xfe, 0x6c, 0x00 ],
  'x': [ 0x78, 0x00, 0x00, 0xc6, 0x6c, 0x38, 0x6c, 0xc6, 0x00 ],
  'y': [ 0x79, 0x00, 0x00, 0xcc, 0xcc, 0xcc, 0x7c, 0x0c, 0xf8 ],
  'z': [ 0x7a, 0x00, 0x00, 0xfc, 0x98, 0x30, 0x64, 0xfc, 0x00 ],
  '{': [ 0x7b, 0x1c, 0x30, 0x30, 0xe0, 0x30, 0x30, 0x1c, 0x00 ],
  '|': [ 0x7c, 0x18, 0x18, 0x18, 0x00, 0x18, 0x18, 0x18, 0x00 ],
  '}': [ 0x7d, 0xe0, 0x30, 0x30, 0x1c, 0x30, 0x30, 0xe0, 0x00 ],
  '~': [ 0x7e, 0x76, 0xdc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
};

function hexToBin(num) {
  var bin = num.toString(2);
  var result = '';

  if (bin.length < 8) {
    for (var i = 0; i < (8 - bin.length); i++)
      result += '0';

    result += bin;
  } else {
    result = bin;
  }

  return result;
}

function showCharacter(character) {
  var byteReprezentation = ASCII_CHARACTERS[character];

  for (var i = 1; i < 8; i++) {
    var binaryRep = hexToBin(byteReprezentation[i])
      .split("").reverse("").join("")

    for (var j = 0; j < binaryRep.length; j++) {
      if (binaryRep[j] == "1")
        senseHat.set_pixel(i, j, 255, 255, 255);
    }
  }
}

for (var measurement_count = 0; measurement_count < 10; measurement_count++) {
  // Show string message
  comm_helper.SendCommand(comm_helper.START, "LED_show_message_js");
  var message = "TEST";
  for (var i = 0; i < message.length; i++) {
    showCharacter(message[i])
    sleep.usleepSync(1000000);
    senseHat.blank();
  }
  comm_helper.SendCommand(comm_helper.STOP, "LED_show_message_js");

  // Show an 'A' letter
  comm_helper.SendCommand(comm_helper.START, "LED_show_letter_js");
  showCharacter('A')
  sleep.usleepSync(3000000);
  senseHat.blank();
  comm_helper.SendCommand(comm_helper.STOP, "LED_show_letter_js");

  // Light up pixels for more accurate measurement.
  for (var constraint = 0; constraint <= 8; constraint++) {
    var measurement_msg = "LED_set_pixels_js_" + constraint;
    comm_helper.SendCommand(comm_helper.START, measurement_msg);
    for (var i = 0; i < constraint; i++) {
      for (var j = 0; j < constraint; j++) {
        senseHat.set_pixel(i, j, 255, 255, 255);
      }
    }
    sleep.usleepSync(3000000);
    comm_helper.SendCommand(comm_helper.STOP, measurement_msg);
    senseHat.blank();
  }
}
