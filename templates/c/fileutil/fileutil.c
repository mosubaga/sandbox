#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <unistd.h>
#include <errno.h>

// Read entire file into a malloc'ed buffer (caller must free)
char *read_file_fast(const char *filepath) {
    FILE *file = fopen(filepath, "rb");
    if (!file) {
        fprintf(stderr, "Cannot open file: %s\n", filepath);
        return NULL;
    }

    fseek(file, 0, SEEK_END);
    long size = ftell(file);
    rewind(file);

    char *content = (char *)malloc(size + 1);
    if (!content) {
        fclose(file);
        return NULL;
    }

    fread(content, 1, size, file);
    content[size] = '\0';
    fclose(file);
    return content;
}

// Write string to file
int write_file_fast(const char *filepath, const char *content) {
    FILE *file = fopen(filepath, "wb");
    if (!file) {
        fprintf(stderr, "Cannot create file: %s\n", filepath);
        return 0;
    }
    fwrite(content, 1, strlen(content), file);
    fclose(file);
    return 1;
}

// Read file lines into malloc'ed array of strings
// Caller must free each line and the array itself
char **read_lines_fast(const char *filepath, size_t *out_count) {
    FILE *file = fopen(filepath, "r");
    if (!file) {
        fprintf(stderr, "Cannot open file: %s\n", filepath);
        return NULL;
    }

    size_t capacity = 16;
    size_t count = 0;
    char **lines = malloc(capacity * sizeof(char *));
    if (!lines) {
        fclose(file);
        return NULL;
    }

    char buffer[4096];
    while (fgets(buffer, sizeof(buffer), file)) {
        size_t len = strlen(buffer);
        if (len > 0 && buffer[len - 1] == '\n') buffer[len - 1] = '\0';
        lines[count] = strdup(buffer);
        count++;
        if (count >= capacity) {
            capacity *= 2;
            lines = realloc(lines, capacity * sizeof(char *));
        }
    }

    fclose(file);
    *out_count = count;
    return lines;
}

// Write lines from array to file
int write_lines_fast(const char *filepath, char **lines, size_t count) {
    FILE *file = fopen(filepath, "w");
    if (!file) {
        fprintf(stderr, "Cannot create file: %s\n", filepath);
        return 0;
    }

    for (size_t i = 0; i < count; i++) {
        fprintf(file, "%s\n", lines[i]);
    }

    fclose(file);
    return 1;
}

// Directory listing
char **list_directory(const char *path, size_t *out_count) {
    DIR *dir = opendir(path);
    if (!dir) {
        fprintf(stderr, "Error opening directory: %s\n", path);
        return NULL;
    }

    struct dirent *entry;
    size_t capacity = 16;
    size_t count = 0;
    char **files = malloc(capacity * sizeof(char *));
    if (!files) {
        closedir(dir);
        return NULL;
    }

    while ((entry = readdir(dir)) != NULL) {
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) continue;

        size_t path_len = strlen(path) + strlen(entry->d_name) + 2;
        char *fullpath = malloc(path_len);
        snprintf(fullpath, path_len, "%s/%s", path, entry->d_name);

        files[count] = fullpath;
        count++;
        if (count >= capacity) {
            capacity *= 2;
            files = realloc(files, capacity * sizeof(char *));
        }
    }

    closedir(dir);
    *out_count = count;
    return files;
}

// Get file size
size_t get_file_size(const char *filepath) {
    struct stat st;
    if (stat(filepath, &st) != 0) {
        fprintf(stderr, "Error getting file size: %s\n", filepath);
        return 0;
    }
    return (size_t)st.st_size;
}

// Check if file exists
int file_exists(const char *filepath) {
    struct stat st;
    return stat(filepath, &st) == 0 && S_ISREG(st.st_mode);
}

// Check if directory exists
int directory_exists(const char *path) {
    struct stat st;
    return stat(path, &st) == 0 && S_ISDIR(st.st_mode);
}

// Create directory (recursively)
int create_directory(const char *path) {
    if (mkdir(path, 0755) == 0) return 1;
    if (errno == EEXIST) return 1;
    return 0;
}

// Delete file
int delete_file(const char *filepath) {
    return unlink(filepath) == 0;
}

// Copy file
int copy_file_fast(const char *source, const char *destination) {
    FILE *src = fopen(source, "rb");
    if (!src) return 0;
    FILE *dst = fopen(destination, "wb");
    if (!dst) {
        fclose(src);
        return 0;
    }

    char buffer[4096];
    size_t bytes;
    while ((bytes = fread(buffer, 1, sizeof(buffer), src)) > 0) {
        fwrite(buffer, 1, bytes, dst);
    }

    fclose(src);
    fclose(dst);
    return 1;
}

// Move file (rename)
int move_file_fast(const char *source, const char *destination) {
    return rename(source, destination) == 0;
}

// Search for text in file
int search_in_file(const char *filepath, const char *search_term) {
    FILE *file = fopen(filepath, "r");
    if (!file) {
        fprintf(stderr, "Cannot open file: %s\n", filepath);
        return 0;
    }

    char buffer[4096];
    while (fgets(buffer, sizeof(buffer), file)) {
        if (strstr(buffer, search_term)) {
            fclose(file);
            return 1;
        }
    }

    fclose(file);
    return 0;
}

// Count lines in file
size_t count_lines(const char *filepath) {
    FILE *file = fopen(filepath, "r");
    if (!file) {
        fprintf(stderr, "Cannot open file: %s\n", filepath);
        return 0;
    }

    size_t line_count = 0;
    char buffer[4096];
    while (fgets(buffer, sizeof(buffer), file)) {
        line_count++;
    }

    fclose(file);
    return line_count;
}

// ---------------- MAIN ----------------
int main() {
    const char *lang = "C";
    printf("Hello and welcome to %s!\n", lang);

    const char *input1 = "[File_path]";
    size_t line_count = count_lines(input1);
    printf("%s\n%zu\n", input1, line_count);
    printf("Line count: %zu\n\n", line_count);

    const char *input2 = "[File_path]";
    line_count = count_lines(input2);
    printf("%s\n%zu\n", input2, line_count);
    printf("Line count: %zu\n\n", line_count);

    // Example directory listing
    size_t file_count = 0;
    char **files = list_directory("DIR_PATH", &file_count);
    if (files) {
        printf("Files in directory:\n");
        for (size_t i = 0; i < file_count; i++) {
            printf("  %s\n", files[i]);
            free(files[i]);
        }
        free(files);
    }

    return 0;
}
