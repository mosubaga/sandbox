#include <iostream>
#include <curl/curl.h>

// Callback function to handle the response received from the server
size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* response) {
    size_t totalSize = size * nmemb;
    response->append((char*)contents, totalSize);
    return totalSize;
}

int main() {
    CURL* curl;
    CURLcode res;
    std::string response;

    // Initialize cURL
    curl_global_init(CURL_GLOBAL_ALL);
    curl = curl_easy_init();
    if (curl) {
        // Set the URL to send the GET request
        curl_easy_setopt(curl, CURLOPT_URL, "[URL]");

        // Set the custom request header "Authorization: HeaderTest"
        struct curl_slist* headers = NULL;
        headers = curl_slist_append(headers, "Authorization: HeaderTest");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        // Set the callback function to handle the response
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);

        // Perform the request
        res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            std::cerr << "Failed to perform request: " << curl_easy_strerror(res) << std::endl;
        } else {
            // Print the response received from the server
            std::cout << "Response received:\n" << response << std::endl;
        }

        // Clean up
        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
    } else {
        std::cerr << "Failed to initialize cURL" << std::endl;
    }

    // Cleanup cURL resources
    curl_global_cleanup();

    return 0;
}