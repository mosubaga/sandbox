#include <iostream>
#include <regex>
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

std::string regex_group(const std::string& text, const std::string& pattern, std::size_t group_index) {
    const std::regex compiled(pattern);
    std::smatch match;
    if (!std::regex_match(text, match, compiled)) {
        return "";
    }

    if (group_index >= match.size()) {
        return "";
    }

    return match[group_index].str();
}

std::size_t regex_group_count(const std::string& pattern) {
    const std::regex compiled(pattern);
    return compiled.mark_count();
}

bool regex_matches(const std::string& text, const std::string& pattern) {
    return std::regex_match(text, std::regex(pattern));
}

std::string regex_replace_all(const std::string& text,
                              const std::string& pattern,
                              const std::string& replacement) {
    return std::regex_replace(text, std::regex(pattern), replacement);
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

    std::string email = "nhayashi@example.com";
    std::string email_pattern = "(.*)@(.*)\\.com";
    std::cout << "Regex group count: " << regex_group_count(email_pattern) << "\n";
    std::cout << "Regex group 1: [" << regex_group(email, email_pattern, 1) << "]\n";
    std::cout << "Regex group 2: [" << regex_group(email, email_pattern, 2) << "]\n";
    std::cout << "Regex matches: "
              << (regex_matches(email, email_pattern) ? "yes" : "no")
              << "\n";
    std::cout << "Regex replaced: ["
              << regex_replace_all(email, "@example\\.com", "@example.org")
              << "]\n";

    return 0;
}
