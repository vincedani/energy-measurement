
#include <cstdlib>
#include <cstring>
#include "jerryscript.h"
#include "sqlite_js_binding.h"


// external function for API functions
jerry_value_t insertRecord_handler (const jerry_value_t function_obj,
                                    const jerry_value_t this_val,
                                    const jerry_value_t args_p[],
                                    const jerry_length_t args_cnt)
{
  int result;
  switch (args_cnt) {

    case 0: {
      result = insertRecord();
      break;
    }

    default: {
      char const *msg = "Wrong argument count for insertRecord().";
      return jerry_create_error (JERRY_ERROR_TYPE, (const jerry_char_t*)msg);
    }
  }


  jerry_value_t ret_val = jerry_create_number (result);

  return ret_val;
}


// external function for API functions
jerry_value_t queryRecords_handler (const jerry_value_t function_obj,
                                    const jerry_value_t this_val,
                                    const jerry_value_t args_p[],
                                    const jerry_length_t args_cnt)
{
  int result;
  switch (args_cnt) {

    case 0: {
      result = queryRecords();
      break;
    }

    default: {
      char const *msg = "Wrong argument count for queryRecords().";
      return jerry_create_error (JERRY_ERROR_TYPE, (const jerry_char_t*)msg);
    }
  }


  jerry_value_t ret_val = jerry_create_number (result);

  return ret_val;
}


// init function for the module
extern "C" jerry_value_t Init_SQLite()
{

  jerry_value_t object = jerry_create_object();


  // set an external function as a property to the module object
  jerry_value_t insertRecord_name = jerry_create_string ((const jerry_char_t*)"insertRecord");
  jerry_value_t insertRecord_func = jerry_create_external_function (insertRecord_handler);
  jerry_value_t insertRecord_ret = jerry_set_property (object, insertRecord_name, insertRecord_func);
  jerry_release_value (insertRecord_name);
  jerry_release_value (insertRecord_func);
  jerry_release_value (insertRecord_ret);


  // set an external function as a property to the module object
  jerry_value_t queryRecords_name = jerry_create_string ((const jerry_char_t*)"queryRecords");
  jerry_value_t queryRecords_func = jerry_create_external_function (queryRecords_handler);
  jerry_value_t queryRecords_ret = jerry_set_property (object, queryRecords_name, queryRecords_func);
  jerry_release_value (queryRecords_name);
  jerry_release_value (queryRecords_func);
  jerry_release_value (queryRecords_ret);

  return object;
}
