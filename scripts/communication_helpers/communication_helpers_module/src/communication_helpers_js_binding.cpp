
#include <cstdlib>
#include <cstring>
#include "jerryscript.h"
#include "communication_helpers_js_binding.h"



// external function for API functions
jerry_value_t SendCommand_handler (const jerry_value_t function_obj,
                                    const jerry_value_t this_val,
                                    const jerry_value_t args_p[],
                                    const jerry_length_t args_cnt)
{
  
  switch (args_cnt) {

    case 2: {

      if (jerry_value_is_number (args_p[0]) && (jerry_value_is_string (args_p[1]) || jerry_value_is_null (args_p[1])))
      {
        
  // create an integer / floating point number from a jerry_value_t
  Command arg_0 = (Command)jerry_get_number_value (args_p[0]);

  // create an array of characters from a jerry_value_t
  char * arg_1 = NULL;
  if (jerry_value_is_string (args_p[1]))
  {
    jerry_size_t arg_1_size = jerry_get_string_size (args_p[1]);
    arg_1 = new char[arg_1_size + 1];
    jerry_string_to_char_buffer (args_p[1], (jerry_char_t*)arg_1, arg_1_size);
    arg_1[arg_1_size] = '\0';
  }

        SendCommand(arg_0, arg_1);
        
  // TODO: if you won't use arg_1 pointer, uncomment the line below
  //if (jerry_value_is_string (args_p[1]))
  //  delete[] arg_1;

        break;
      }

    char const *msg = "Wrong argument type for SendCommand().";
    return jerry_create_error (JERRY_ERROR_TYPE, (const jerry_char_t*)msg);
    }

    default: {
      char const *msg = "Wrong argument count for SendCommand().";
      return jerry_create_error (JERRY_ERROR_TYPE, (const jerry_char_t*)msg);
    }
  }

  
  jerry_value_t ret_val = jerry_create_undefined ();

  return ret_val;
}


// init function for the module
extern "C" jerry_value_t Init_communication_helpers()
{

  jerry_value_t object = jerry_create_object();


  // set an external function as a property to the module object
  jerry_value_t SendCommand_name = jerry_create_string ((const jerry_char_t*)"SendCommand");
  jerry_value_t SendCommand_func = jerry_create_external_function (SendCommand_handler);
  jerry_value_t SendCommand_ret = jerry_set_property (object, SendCommand_name, SendCommand_func);
  jerry_release_value (SendCommand_name);
  jerry_release_value (SendCommand_func);
  jerry_release_value (SendCommand_ret);


  // set an enum constant as a property to the module object
  jerry_property_descriptor_t START_prop_desc;
  jerry_init_property_descriptor_fields (&START_prop_desc);
  START_prop_desc.is_value_defined = true;
  START_prop_desc.value = jerry_create_number (START);
  jerry_value_t START_name = jerry_create_string ((const jerry_char_t *)"START");
  jerry_value_t START_ret = jerry_define_own_property (object, START_name, &START_prop_desc);
  jerry_release_value (START_ret);
  jerry_release_value (START_name);
  jerry_free_property_descriptor_fields (&START_prop_desc);


  // set an enum constant as a property to the module object
  jerry_property_descriptor_t STOP_prop_desc;
  jerry_init_property_descriptor_fields (&STOP_prop_desc);
  STOP_prop_desc.is_value_defined = true;
  STOP_prop_desc.value = jerry_create_number (STOP);
  jerry_value_t STOP_name = jerry_create_string ((const jerry_char_t *)"STOP");
  jerry_value_t STOP_ret = jerry_define_own_property (object, STOP_name, &STOP_prop_desc);
  jerry_release_value (STOP_ret);
  jerry_release_value (STOP_name);
  jerry_free_property_descriptor_fields (&STOP_prop_desc);

  return object;
}
