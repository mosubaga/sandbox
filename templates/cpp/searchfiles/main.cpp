#include <iostream>
#include <filesystem>
#include <string>
#include <fstream>

using namespace std;

std::string trim(const std::string& line)
{
    const char* WhiteSpace = " \t\v\r\n";
    std::size_t start = line.find_first_not_of(WhiteSpace);
    std::size_t end = line.find_last_not_of(WhiteSpace);
    return start == end ? std::string() : line.substr(start, end - start + 1);
}

void readfileline(string file_name, string keyword) {
    // Create a vector to store the lines of the file.

    // Open the file for reading.
    std::ifstream input_file(file_name);
    if (!input_file.is_open()) {
        cout << "Error opening file." << endl;
    }

    // Read the file line by line and store the lines in the vector.
    string line;
    int index{1};
    while (getline(input_file, line)) {
        if (line.find(keyword) != std::string::npos) {
            cout << "[" << file_name << "]" << " :: <" << index << "> :: " << trim(line) << endl;
        }
        index++;
    }

    // Close the file.
    input_file.close();
}

void searchFiles(const std::string& directory, const std::string& keyword) {
    for (const auto& entry : std::filesystem::directory_iterator(directory)) {
        if (entry.is_directory()) {
            searchFiles(entry.path().string(), keyword); // Recursive call for subdirectories
        } else if (entry.is_regular_file()) {
            std::string fileName = entry.path().filename().string();
            if ((fileName.find(".py") != std::string::npos) || (fileName.find(".pl") != std::string::npos) || (fileName.find(".rb") != std::string::npos))
            {
                string filename = entry.path().string();
                readfileline(filename,keyword);
            }
        }
    }
}

int main() {
    std::string keyword = "[KEYWORD]";
    std::string startingDirectory;
    startingDirectory = "[ROOT_DIR]";
    searchFiles(startingDirectory, keyword);

    return 0;
}
