#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <sys/stat.h>
#include <string.h>
#include <ctype.h>

#define MAX_LINE_LENGTH 2048 // Define a maximum line length

char *trim(char *str) {
    char *end;

    // Trim leading spaces
    while (isspace((unsigned char)*str)) {
        str++;
    }

    if (*str == 0)  // All spaces?
        return str;

    // Trim trailing spaces
    end = str + strlen(str) - 1;
    while (end > str && isspace((unsigned char)*end)) {
        end--;
    }
    *(end + 1) = 0;

    return str;
}

void search_keyword_in_file(const char *filename, const char *keyword) 
{

    FILE *file = fopen(filename, "r");  // Open the file in read mode
    if (file == NULL) {
        perror("Error opening file");
        return;
    }

    char line[MAX_LINE_LENGTH];  // Array to store each line

    int i = 1;

    while (fgets(line, sizeof(line), file)) {  // Read the file line by line
        // Check if the keyword is found in the line
        char *trimmed_str = trim(line);
        if (strstr(line, keyword)) {
            printf("%s: [%d] %s\n", filename, i, trimmed_str);  // Print the line if keyword is found
        }
        i++;
    }

    fclose(file);  // Close the file
}

// Function to check if a file has the specified extension
int has_extension(const char *filename, const char *extension) {
    // Find the position of the last dot in the filename
    const char *dot = strrchr(filename, '.');
    
    // If there is no dot or it's at the beginning, it's not an extension
    if (!dot || dot == filename) {
        return 0;
    }

    // Compare the file extension with the provided one (case-sensitive)
    return strcmp(dot + 1, extension) == 0;
}

void list_files_recursively(const char *dir_path, const char *extension, const char *keyword) {
    DIR *dir = opendir(dir_path);
    if (dir == NULL) {
        perror("opendir");
        return;
    }

    struct dirent *entry;
    struct stat file_stat;
    char full_path[2048];

    while ((entry = readdir(dir)) != NULL) {
        // Skip the current directory (.) and parent directory (..)
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
            continue;

        // Build the full path
        snprintf(full_path, sizeof(full_path), "%s/%s", dir_path, entry->d_name);

        // Get file information
        if (stat(full_path, &file_stat) == -1) {
            perror("stat");
            continue;
        }

        // If it's a directory, recursively list its contents
        if (S_ISDIR(file_stat.st_mode)) {
            // printf("Directory: %s\n", full_path);
            list_files_recursively(full_path, extension,keyword);  // Recursion
        }
        // If it's a file and has the specified extension, print its name
        else if (S_ISREG(file_stat.st_mode)) {
            if (has_extension(entry->d_name, extension)) {
                search_keyword_in_file(full_path, keyword);
            }
        }
    }

    closedir(dir);
}

int main(int argc, char *argv[]) {
    // Check if both directory path and extension are provided
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <directory_path> <file_extension> <keyword>\n", argv[0]);
        return EXIT_FAILURE;
    }

    // List files recursively starting from the provided directory, filtering by the specified extension
    list_files_recursively(argv[1], argv[2], argv[3]);

    return EXIT_SUCCESS;
}
