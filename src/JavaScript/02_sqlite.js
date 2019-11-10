var comm_helper = require('communication_helpers_module');
var sqlite_module = require('sqlite_module');

for (i = 0; i < 10; i++) {
  comm_helper.SendCommand(comm_helper.START, "save_record_sqlite3_js");
  sqlite_module.insertRecord();
  comm_helper.SendCommand(comm_helper.STOP, "save_record_sqlite3_js");

  comm_helper.SendCommand(comm_helper.START, "query_record_sqlite3_js");
  sqlite_module.queryRecords();
  comm_helper.SendCommand(comm_helper.STOP, "query_record_sqlite3_js");
}
