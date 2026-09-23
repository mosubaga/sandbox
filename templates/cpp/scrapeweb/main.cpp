#include <iostream>
#include <string>
#include <curl/curl.h>
#include <gumbo.h>

// libcurl callback function to handle incoming data stream
// Appends incoming text data chunks directly into a standard C++ string
static size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    size_t realsize = size * nmemb;
    std::string* mem = static_cast<std::string*>(userp);

    // Append the character chunk to our C++ string buffer
    mem->append(static_cast<const char*>(contents), realsize);

    return realsize;
}

// Recursively walks the DOM tree to extract <a> link attributes
void extract_links(GumboNode* node) {
    if (node->type != GUMBO_NODE_ELEMENT) {
        return;
    }

    if (node->v.element.tag == GUMBO_TAG_A) {
        GumboAttribute* href = gumbo_get_attribute(&node->v.element.attributes, "href");

        if (href) {
            std::string link_text = "[No Text]";

            // Check if the link element has an inner text child node
            if (node->v.element.children.length > 0) {
                // Access the 0-th element of the data array first, then cast it
                GumboNode* child = static_cast<GumboNode*>(node->v.element.children.data[0]);
                if (child->type == GUMBO_NODE_TEXT || child->type == GUMBO_NODE_WHITESPACE) {
                    link_text = child->v.text.text;
                }
            }

            std::cout << "Link Text: " << link_text << "\n";
            std::cout << "URL:       " << href->value << "\n";
            std::cout << "-----------------------------------\n";
        }
    }

    // Traverse every child element using modern casting
    GumboVector* children = &node->v.element.children;
    for (unsigned int i = 0; i < children->length; ++i) {
        extract_links(static_cast<GumboNode*>(children->data[i]));
    }
}

int main() {
    CURL* curl_handle;
    CURLcode res;

    // Use a clean C++ std::string buffer instead of raw char * and realloc
    std::string html_buffer;

    // Define the URL to scrape
    const char* target_url = "https://mosubaga.github.io";

    // Initialize global libcurl state
    curl_global_init(CURL_GLOBAL_ALL);
    curl_handle = curl_easy_init();

    if (curl_handle) {
        // Specify target URL
        curl_easy_setopt(curl_handle, CURLOPT_URL, target_url);

        // Pass our WriteCallback function to handle downloading chunks
        curl_easy_setopt(curl_handle, CURLOPT_WRITEFUNCTION, WriteCallback);

        // Pass our custom string pointer to the callback function
        curl_easy_setopt(curl_handle, CURLOPT_WRITEDATA, &html_buffer);

        // Emulate a web browser User-Agent to avoid generic automated access blocks
        curl_easy_setopt(curl_handle, CURLOPT_USERAGENT, "libcurl-agent/1.0");

        std::cout << "Downloading content from: " << target_url << "...\n";
        res = curl_easy_perform(curl_handle);

        if (res != CURLE_OK) {
            std::cerr << "libcurl failed: " << curl_easy_strerror(res) << "\n";
        }
        else {
            std::cout << "Downloaded " << html_buffer.size() << " bytes successfully. Parsing HTML...\n\n";

            // Parse downloaded HTML layout tree using Gumbo (.c_str() provides the const char*)
            GumboOutput* output = gumbo_parse(html_buffer.c_str());

            // Begin extracting hyperlinks from root level node
            extract_links(output->root);

            // Clean up Gumbo parse tree allocations
            gumbo_destroy_output(&kGumboDefaultOptions, output);
        }

        // Cleanup local curl handle resources
        curl_easy_cleanup(curl_handle);
    }

    // Global libcurl environment shutdown
    curl_global_cleanup();

    return 0;
}
