#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <boost/program_options.hpp>
#include <boost/filesystem.hpp>

namespace po = boost::program_options;
namespace fs = boost::filesystem;

bool is_text_file(const fs::path& file_path) {
    boost::system::error_code ec;
    auto file_size = fs::file_size(file_path, ec);
    if (ec) {
        return false;
    }
    if (file_size == 0) {
        return true; // Empty file is safe to treat as text
    }

    std::ifstream in(file_path.string(), std::ios::binary);
    if (!in.is_open()) {
        return false;
    }

    constexpr size_t buffer_size = 8192;
    char buffer[buffer_size];
    in.read(buffer, buffer_size);
    std::streamsize bytes_read = in.gcount();
    if (bytes_read == 0) {
        return true;
    }

    size_t non_printable_count = 0;
    for (std::streamsize i = 0; i < bytes_read; ++i) {
        unsigned char c = static_cast<unsigned char>(buffer[i]);
        if (c == '\0') {
            return false; // Null byte indicates binary format
        }
        // Check for ASCII control characters excluding standard whitespace/control
        if ((c < 0x07) || (c > 0x0D && c < 0x1B) || (c > 0x1F && c < 0x20) || (c == 0x7F)) {
            non_printable_count++;
        }
    }

    // If more than 1% of sampled bytes are unusual control characters, treat as binary
    if (static_cast<double>(non_printable_count) / static_cast<double>(bytes_read) > 0.01) {
        return false;
    }

    return true;
}

void process_file(const fs::path& file_path, const std::string& old_text, const std::string& new_text) {
    std::ifstream in(file_path.string(), std::ios::binary);
    if (!in.is_open()) {
        std::cerr << "Warning: Could not open file: " << file_path.string() << "\n";
        return;
    }

    std::string content((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());
    in.close();

    if (content.empty()) {
        return;
    }

    // Find all occurrences of old_text
    std::vector<size_t> match_positions;
    size_t pos = 0;
    while ((pos = content.find(old_text, pos)) != std::string::npos) {
        match_positions.push_back(pos);
        pos += old_text.length();
    }

    if (match_positions.empty()) {
        return;
    }

    // Precompute newline positions for line number lookup
    std::vector<size_t> newline_positions;
    for (size_t i = 0; i < content.size(); ++i) {
        if (content[i] == '\n') {
            newline_positions.push_back(i);
        }
    }

    auto get_line_number = [&](size_t char_pos) -> size_t {
        auto it = std::lower_bound(newline_positions.begin(), newline_positions.end(), char_pos);
        return 1 + std::distance(newline_positions.begin(), it);
    };

    // Log each replacement
    for (size_t match_pos : match_positions) {
        size_t line_num = get_line_number(match_pos);
        std::cout << "File: " << file_path.string() << ", Line " << line_num
                  << ": replaced \"" << old_text << "\" with \"" << new_text << "\"\n";
    }

    // 1. Create backup file with extension .bak (original content)
    fs::path backup_path = file_path.string() + ".bak";
    boost::system::error_code ec;
    fs::copy_file(file_path, backup_path, fs::copy_options::overwrite_existing, ec);
    if (ec) {
        std::cerr << "Error: Failed to create backup file " << backup_path.string()
                  << ": " << ec.message() << "\n";
        return;
    }

    // 2. Perform replacement
    std::string new_content;
    new_content.reserve(content.size() + match_positions.size() * (new_text.size() > old_text.size() ? (new_text.size() - old_text.size()) : 0));
    size_t last_pos = 0;
    for (size_t match_pos : match_positions) {
        new_content.append(content, last_pos, match_pos - last_pos);
        new_content.append(new_text);
        last_pos = match_pos + old_text.length();
    }
    new_content.append(content, last_pos, content.size() - last_pos);

    // 3. Write modified content to file
    std::ofstream out(file_path.string(), std::ios::binary | std::ios::trunc);
    if (!out.is_open()) {
        std::cerr << "Error: Could not write to file: " << file_path.string() << "\n";
        return;
    }
    out.write(new_content.data(), new_content.size());
    out.close();
}

int main(int argc, char* argv[]) {
    po::options_description desc("Allowed options");
    desc.add_options()
        ("help,h", "Produce help message")
        ("directory,d", po::value<std::string>()->required(), "Target directory name")
        ("old,o", po::value<std::string>()->required(), "Old text to search")
        ("new,n", po::value<std::string>()->required(), "New text to replace");

    po::variables_map vm;
    try {
        po::store(po::parse_command_line(argc, argv, desc), vm);
        if (vm.count("help")) {
            std::cout << desc << "\n";
            return 0;
        }
        po::notify(vm);
    } catch (const po::error& e) {
        std::cerr << "Error: " << e.what() << "\n\n";
        std::cerr << desc << "\n";
        return 1;
    }

    std::string directory = vm["directory"].as<std::string>();
    std::string old_text = vm["old"].as<std::string>();
    std::string new_text = vm["new"].as<std::string>();

    if (old_text.empty()) {
        std::cerr << "Error: Old text cannot be empty.\n";
        return 1;
    }

    fs::path target_path(directory);
    boost::system::error_code ec;
    if (!fs::exists(target_path, ec) || ec) {
        std::cerr << "Error: Path does not exist: " << directory << "\n";
        return 1;
    }

    if (fs::is_regular_file(target_path, ec)) {
        if (target_path.extension() != ".bak" && is_text_file(target_path)) {
            process_file(target_path, old_text, new_text);
        }
        return 0;
    }

    if (!fs::is_directory(target_path, ec)) {
        std::cerr << "Error: Path is neither a regular file nor a directory: " << directory << "\n";
        return 1;
    }

    for (fs::recursive_directory_iterator it(target_path, ec), end; it != end; it.increment(ec)) {
        if (ec) {
            std::cerr << "Warning: Error accessing directory entry: " << ec.message() << "\n";
            ec.clear();
            continue;
        }

        const fs::path& current_path = it->path();

        // Skip backup files
        if (current_path.extension() == ".bak") {
            continue;
        }

        boost::system::error_code status_ec;
        if (!fs::is_regular_file(current_path, status_ec) || status_ec) {
            continue;
        }

        if (!is_text_file(current_path)) {
            continue; // Skip binary files
        }

        process_file(current_path, old_text, new_text);
    }

    return 0;
}