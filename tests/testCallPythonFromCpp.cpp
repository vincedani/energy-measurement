#include<iostream>
#include <cstdlib>

using namespace std;

int main ()
{
  int result = system("/home/pi/work/test_sender.py");
  cout << "Success?" << endl;
}
