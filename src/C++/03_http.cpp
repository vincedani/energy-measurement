/*
 * Compiling:
 * g++ 03_http.cpp                                             \
 *   ../../scripts/communication_helpers/CommunicationHelper.h \
 *   ../../scripts/communication_helpers/CommunicationHelper.c \
 *   -lwiringPi                                                \
 *   -lcurl
 */

#include <iostream>
#include <curl/curl.h>

#include "../../scripts/communication_helpers/CommunicationHelper.h"

#define API_ENDPOINT "http://192.168.2.178/weather/add"

using namespace std;

int httpGet() {
  // SendCommand(START, "http_get_cpp");

  // SendCommand(STOP, "http_get_cpp");
}

int httpPost() {
  // SendCommand(START, "http_post_cpp");

  curl_global_init(CURL_GLOBAL_ALL);
  CURL *curl = curl_easy_init();

  if (curl) {
    curl_easy_setopt(curl, CURLOPT_URL, API_ENDPOINT);
    // TODO: data
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, "name=daniel&project=curl");

    CURLcode res = curl_easy_perform(curl);
    if(res != CURLE_OK) {
       /* ignore */
       cerr << "[ERROR]: " << curl_easy_strerror(res) << endl;
    }

    curl_easy_cleanup(curl);
  }

  curl_global_cleanup();

  // SendCommand(STOP, "http_post_cpp");
  return 0;
}

int main() {
  for (int i = 0; i < 1; i++) {
    httpPost();
    httpGet();
  }

  return 0;
}