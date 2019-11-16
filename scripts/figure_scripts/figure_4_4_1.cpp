/*
 * Compiling:
 * g++ figure_4_4_1.cpp                             \
 *   ../communication_helpers/CommunicationHelper.h \
 *   ../communication_helpers/CommunicationHelper.c \
 *   -lwiringPi
 */

#include <iostream>
#include <vector>
#include <fstream>
#include <cstdlib>
#include "../communication_helpers/CommunicationHelper.h"

using namespace std;

int main(int argc, char const *argv[]) {
  unsigned long long int nterms = std::atoi(argv[1]);

  unsigned long long int n1 = 0;
  unsigned long long int n2 = 1;
  unsigned long long int nth = 0;
  unsigned long long int count = 0;

  SendCommand(START, "fibonacci_cpp_0S");
  std::vector<unsigned long long int> sequence { n2 };

  while(count <= nterms) {
    nth = n1 + n2;
    sequence.push_back(nth);

    n1 = n2;
    n2 = nth;
    count++;
  }

  std::ofstream outFile;
  outFile.open("fibonacci_sequence_cpp.txt");

  unsigned long long int maxIndex = sequence.size() < 15000 ? sequence.size() : 15000;
  for (unsigned long long int i = 0; i < maxIndex; i++) {
    outFile << sequence.at(i) << ",";
  }
  SendCommand(STOP, "fibonacci_cpp_0S");

  return 0;
}
