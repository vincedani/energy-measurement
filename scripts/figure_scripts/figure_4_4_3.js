var comm_helper = require('communication_helpers_module');
var fs = require('fs');

Number.prototype.toFixedSpecial = function(n) {
  var str = this.toFixed(n);
  if (str.indexOf('e+') === -1)
    return str;

  // if number is in scientific notation, pick (b)ase and (p)ower
  str = str.replace('.', '').split('e+').reduce(function(p, b) {
    return p + Array(b - p.length + 2).join(0);
  });

  if (n > 0)
    str += '.' + Array(n + 1).join(0);

  return str;
};


var nterms = process.argv[2];

// first two terms
var n1 = 0;
var n2 = 1;
var count = 0;

function insertionSort(nums) {
  for (var i = 1; i < nums.length; i++) {
    var j = i - 1
    var tmp = nums[i]
    while (j >= 0 && nums[j] > tmp) {
      nums[j + 1] = nums[j]
      j--
    }
    nums[j+1] = tmp
  }
  return nums
}

comm_helper.SendCommand(comm_helper.START, "fibonacci_alg_js");

var fibonacci_sequence = [ n2 ];

while (count < nterms) {
  nth = n1 + n2
  fibonacci_sequence.push(nth);

  n1 = n2
  n2 = nth
  count += 1
}

var sortedList = insertionSort(fibonacci_sequence.reverse())

var wStream = fs.createWriteStream("fibonacci_sequence_js.txt");

wStream.on('ready', function() {
  for (var i = 0; i < sortedList.length; i++) {
    var printedNumber = sortedList[i].toFixedSpecial(0);
    wStream.write(printedNumber + ",");
  }
});

comm_helper.SendCommand(comm_helper.STOP, "fibonacci_alg_js");