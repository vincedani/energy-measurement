/*
 * Compiling:
 * g++ 02_sqlite.cpp                                           \
 *   ../../scripts/communication_helpers/CommunicationHelper.h \
 *   ../../scripts/communication_helpers/CommunicationHelper.c \
 *   -lwiringPi                                                \
 *   -lsqlite3
 */

#include <sqlite3.h>
#include <string>

#include <iomanip>
#include <ctime>
#include <chrono>
#include <sstream>
#include <iostream>

#include "../../scripts/communication_helpers/CommunicationHelper.h"

using namespace std;
using namespace std::chrono;

#define DB_PATH "/home/pi/energy-measurement/src/weather_station.db"

string quoteParam(const string& s) {
    return string("'") + s + string("'");
}

string getCurrentTime() {
  auto now = system_clock::now();
  auto ms = duration_cast<milliseconds>(now.time_since_epoch()) % 1000;

  auto timer = system_clock::to_time_t(now);
  std::tm bt = *localtime(&timer);

  std::ostringstream oss;
  oss << put_time(&bt, "%H:%M:%S") << "." << ms.count();
  return oss.str();
}

static int callback(void *data, int argc, char **argv, char **azColName) {
  // Debugging information.
  // Not needed to print out the fetched data during the energy-measurement.

  // for (int i = 0; i < argc; i++) {
  //   cout << azColName[i] << ": " << (argv[i] ? argv[i] : "NULL") << endl;
  // }
  // cout << endl;

  return 0;
}

int insertRecord() {
  auto current_time = getCurrentTime();
  float temperature = 25.072;
  float humidity    = 56.19;
  float pressure    = 998.646;

  SendCommand(START, "save_record_sqlite3_cpp");

  sqlite3 *db;
  int result = sqlite3_open(DB_PATH, &db);

  if (result != 0)
    return 1;

  string command = "insert into Measurements "              \
    "(TimeStamp, Temperature, Humidity, Pressure) values (" \
    + quoteParam(current_time)           + ", "
    + quoteParam(to_string(temperature)) + ", "
    + quoteParam(to_string(humidity))    + ", "
    + quoteParam(to_string(pressure))    + ");";

  char *zErrMsg = 0;
  result = sqlite3_exec(db, command.c_str(), callback, 0, &zErrMsg);

  if (result != SQLITE_OK)
    return 1;

  sqlite3_close(db);

  SendCommand(STOP, "save_record_sqlite3_cpp");

  return 0;
}

int queryRecords() {
  SendCommand(START, "query_record_sqlite3_cpp");

  sqlite3 *db;
  int result = sqlite3_open(DB_PATH, &db);

  if (result != 0)
    return 1;

  string command = "select * from Measurements order by ID desc limit 5";

  char *zErrMsg = 0;
  result = sqlite3_exec(db, command.c_str(), callback, 0, &zErrMsg);

  if (result != SQLITE_OK)
    return 1;

  sqlite3_close(db);

  SendCommand(STOP, "query_record_sqlite3_cpp");

  return 0;
}

int main()
{
  for (int i = 0; i < 10; i++) {
    int result = insertRecord();

    if (result != 0)
      return 1;

    result = queryRecords();

    if (result != 0)
      return 1;
  }

  return 0;
}
