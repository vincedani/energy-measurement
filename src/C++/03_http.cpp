/*
 * Compiling:
 * g++ 03_http.cpp                                             \
 *   ../../scripts/communication_helpers/CommunicationHelper.h \
 *   ../../scripts/communication_helpers/CommunicationHelper.c \
 *   -lwiringPi                                                \
 *   -lcurl
 */

#include <iostream>
#include <sstream>
#include <string>
#include <curl/curl.h>

#include "../../scripts/communication_helpers/CommunicationHelper.h"

#define API_ENDPOINT "http://192.168.2.58/MockServer/api/weather/"

using namespace std;

size_t writeFunction(void *ptr, size_t size, size_t nmemb, std::string* data) {
  data->append((char*) ptr, size * nmemb);
  return size * nmemb;
}

int httpGet() {
  std::stringstream ss;
  ss << API_ENDPOINT << 12;
  string url = ss.str();

  SendCommand(START, "http_get_cpp");

  curl_global_init(CURL_GLOBAL_ALL);
  CURL *curl = curl_easy_init();

  if (curl) {
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_HTTPGET, 1L);

    string response_string;
    string header_string;
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, writeFunction);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response_string);
    curl_easy_setopt(curl, CURLOPT_HEADERDATA, &header_string);;

    CURLcode res = curl_easy_perform(curl);
    if(res != CURLE_OK) {
       /* ignore */
       cerr << "[ERROR]: " << curl_easy_strerror(res) << endl;
    }

    curl_easy_cleanup(curl);
  }

  curl_global_cleanup();

  SendCommand(STOP, "http_get_cpp");
}

int httpPost() {
  string data = " [                                                                                                     \
      { \"TimeStamp\" : \"23:33:14.695226\", \"Temperature\" : 24.893, \"Humidity\" : 56.576, \"Pressure\" : 998.634 }, \
      { \"TimeStamp\" : \"23:33:33.805037\", \"Temperature\" : 24.963, \"Humidity\" : 56.488, \"Pressure\" : 998.640 }, \
      { \"TimeStamp\" : \"23:34:02.239622\", \"Temperature\" : 25.177, \"Humidity\" : 55.715, \"Pressure\" : 998.687 }, \
      { \"TimeStamp\" : \"23:34:54.227033\", \"Temperature\" : 24.939, \"Humidity\" : 55.843, \"Pressure\" : 998.686 }, \
      { \"TimeStamp\" : \"23:39:44.063628\", \"Temperature\" : 24.980, \"Humidity\" : 55.676, \"Pressure\" : 998.705 }  \
    ]";

  SendCommand(START, "http_post_cpp");

  curl_global_init(CURL_GLOBAL_ALL);
  CURL *curl = curl_easy_init();

  if (curl) {
    curl_easy_setopt(curl, CURLOPT_URL, API_ENDPOINT);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);

    CURLcode res = curl_easy_perform(curl);
    if(res != CURLE_OK) {
       /* ignore */
       cerr << "[ERROR]: " << curl_easy_strerror(res) << endl;
    }

    curl_easy_cleanup(curl);
  }

  curl_global_cleanup();

  SendCommand(STOP, "http_post_cpp");
  return 0;
}

int main() {
  for (int i = 0; i < 10; i++) {
    httpPost();
    httpGet();
  }

  return 0;
}
