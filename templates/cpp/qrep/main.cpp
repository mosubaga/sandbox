/*
 * qprep.cpp
 *
 * A grep-like tool built with Boost that recursively scans a directory
 * tree and prints every line matching a given regex pattern, along
 * with the file name and line number.
 *
 * Performance choices, compared to the GLib version:
 *   - Files are memory-mapped (boost::iostreams::mapped_file_source)
 *     instead of read line-by-line through buffered I/O. The OS pages
 *     the file in on demand and we scan raw bytes directly, which
 *     avoids a read() syscall + buffer copy per line.
 *   - boost::regex is used with newline-delimited scanning over the
 *     mapped region rather than materializing a std::string per line
 *     before matching where avoidable.
 *   - boost::filesystem::recursive_directory_iterator avoids manual
 *     recursion/bookkeeping and skips symlink loops by default.
 *
 * Build:
 *   g++ -O2 -std=c++17 qprep.cpp -o qprep \
 *       -lboost_filesystem -lboost_regex -lboost_program_options -lboost_iostreams
 *
 * Usage:
 *   ./qprep [OPTIONS] PATTERN DIRECTORY
 *
 * Options:
 *   -i, --ignore-case      Case-insensitive matching
 *   -n, --no-line-number   Hide line numbers in output
 *   -h, --help             Show usage
 *
 * Example:
 *   ./qprep -i "error" ./logs
 */

#include <boost/filesystem.hpp>
#include <boost/iostreams/device/mapped_file.hpp>
#include <boost/program_options.hpp>
#include <boost/regex.hpp>

#include <cstdio>
#include <iostream>
#include <string>

namespace fs   = boost::filesystem;
namespace io   = boost::iostreams;
namespace po   = boost::program_options;

/*
 * Scan a single file, already memory-mapped, for lines matching regex.
 * Walks the mapped bytes directly rather than copying the whole file
 * into a std::string first.
 */
static void search_file(const fs::path &path,
                         const boost::regex &regex,
                         bool show_line_numbers)
{
    io::mapped_file_source file;
    try {
        file.open(path.string());
    } catch (const std::exception &) {
        // Skip unreadable/empty files (permissions, broken symlinks, zero-length, etc.)
        return;
    }
    if (!file.is_open())
        return;

    const char *begin = file.data();
    const char *end   = begin + file.size();
    const char *line_start = begin;
    int lineno = 0;

    while (line_start < end) {
        const char *line_end = static_cast<const char *>(
            memchr(line_start, '\n', end - line_start));
        const char *actual_end = line_end ? line_end : end;

        ++lineno;

        // boost::regex_search works directly on a [begin, end) range,
        // so no per-line string allocation is needed just to match.
        if (boost::regex_search(line_start, actual_end, regex)) {
            std::string line(line_start, actual_end);
            if (show_line_numbers)
                std::cout << path.string() << ":" << lineno << ": " << line << "\n";
            else
                std::cout << path.string() << ": " << line << "\n";
        }

        if (!line_end)
            break;
        line_start = line_end + 1;
    }
}

/*
 * Recursively walk a directory, searching every regular file found.
 * boost::filesystem::recursive_directory_iterator handles the
 * recursion and skips symlinked directories by default (avoiding
 * infinite loops on cyclic symlinks).
 */
static void scan_directory(const fs::path &dir,
                            const boost::regex &regex,
                            bool show_line_numbers)
{
    boost::system::error_code ec;
    fs::recursive_directory_iterator it(dir, ec), endit;

    if (ec) {
        std::cerr << "Warning: could not open directory '" << dir.string()
                   << "': " << ec.message() << "\n";
        return;
    }

    for (; it != endit; it.increment(ec)) {
        if (ec) {
            std::cerr << "Warning: error while traversing '" << dir.string()
                       << "': " << ec.message() << "\n";
            ec.clear();
            continue;
        }

        const fs::path &p = it->path();

        if (fs::is_regular_file(p, ec) && !ec) {
            search_file(p, regex, show_line_numbers);
        }
        // Directories are descended into automatically; everything
        // else (sockets, fifos, broken symlinks) is skipped.
    }
}

int main(int argc, char **argv)
{
    bool ignore_case  = false;
    bool hide_linenum = false;
    std::string pattern;
    std::string directory;

    po::options_description visible("Options");
    visible.add_options()
        ("help,h", "Show this help message")
        ("ignore-case,i", po::bool_switch(&ignore_case), "Case-insensitive matching")
        ("no-line-number,n", po::bool_switch(&hide_linenum), "Hide line numbers in output");

    po::options_description hidden("Hidden");
    hidden.add_options()
        ("pattern", po::value<std::string>(&pattern), "Pattern to search for")
        ("directory", po::value<std::string>(&directory), "Directory to search");

    po::positional_options_description positional;
    positional.add("pattern", 1).add("directory", 1);

    po::options_description all;
    all.add(visible).add(hidden);

    po::variables_map vm;
    try {
        po::store(po::command_line_parser(argc, argv)
                       .options(all)
                       .positional(positional)
                       .run(),
                   vm);
        po::notify(vm);
    } catch (const po::error &e) {
        std::cerr << "Error parsing arguments: " << e.what() << "\n\n";
        std::cerr << "Usage: " << argv[0] << " [OPTIONS] PATTERN DIRECTORY\n" << visible << "\n";
        return 1;
    }

    if (vm.count("help") || pattern.empty() || directory.empty()) {
        std::cerr << "Usage: " << argv[0] << " [OPTIONS] PATTERN DIRECTORY\n" << visible << "\n";
        return vm.count("help") ? 0 : 1;
    }

    boost::regex regex;
    try {
        boost::regex::flag_type flags = boost::regex::normal;
        if (ignore_case)
            flags = flags | boost::regex::icase;
        regex.assign(pattern, flags);
    } catch (const boost::regex_error &e) {
        std::cerr << "Invalid pattern '" << pattern << "': " << e.what() << "\n";
        return 1;
    }

    fs::path dir_path(directory);
    boost::system::error_code ec;
    if (!fs::is_directory(dir_path, ec) || ec) {
        std::cerr << "'" << directory << "' is not a directory\n";
        return 1;
    }

    scan_directory(dir_path, regex, !hide_linenum);

    return 0;
}

