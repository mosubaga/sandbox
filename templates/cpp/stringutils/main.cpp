#include <iostream>
#include <string>

bool contains_substring(const std::string& text, const std::string& needle) {
    return text.find(needle) != std::string::npos;
}

std::string trim(const std::string& text) {
    const std::string whitespace = " \t\n\r\f\v";
    const std::size_t start = text.find_first_not_of(whitespace);
    if (start == std::string::npos) {
        return "";
    }

    const std::size_t end = text.find_last_not_of(whitespace);
    return text.substr(start, end - start + 1);
}

std::string replace_all(std::string text, const std::string& from, const std::string& to) {
    if (from.empty()) {
        return text;
    }

    std::size_t position = 0;
    while ((position = text.find(from, position)) != std::string::npos) {
        text.replace(position, from.length(), to);
        position += to.length();
    }

    return text;
}

int main() {
    std::string message = "  Hello, C++ strings!  ";
    std::string trimmed = trim(message);

    std::cout << "Original: [" << message << "]\n";
    std::cout << "Trimmed: [" << trimmed << "]\n";
    std::cout << "Contains 'C++': "
              << (contains_substring(trimmed, "C++") ? "yes" : "no")
              << "\n";

    std::string replaced = replace_all(trimmed, "strings", "utilities");
    std::cout << "Replaced: [" << replaced << "]\n";

    return 0;
}
