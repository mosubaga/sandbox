#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <libgen.h>
#include <unistd.h>

#define MAX_FILES 5000
#define MAX_PATH_LENGTH 5000

// Structure to hold the file list
typedef struct {
    char **files;
    int count;
    int capacity;
} FileList;

// Initialize the file list
FileList* init_file_list() {
    FileList *list = malloc(sizeof(FileList));
    if (!list) {
        fprintf(stderr, "Memory allocation failed\n");
        return NULL;
    }
    
    list->files = malloc(sizeof(char*) * MAX_FILES);
    if (!list->files) {
        fprintf(stderr, "Memory allocation failed\n");
        free(list);
        return NULL;
    }
    
    list->count = 0;
    list->capacity = MAX_FILES;
    return list;
}

char* replace_all(const char *original, const char *search, const char *replace) {

    if (!original || !search || !replace) return NULL;
    
    // Count occurrences
    int count = 0;
    const char *tmp = original;
    while ((tmp = strstr(tmp, search)) != NULL) {
        count++;
        tmp += strlen(search);
    }
    
    if (count == 0) {
        // No occurrences found
        char *result = malloc(strlen(original) + 1);
        strcpy(result, original);
        return result;
    }
    
    // Calculate new string length
    int search_len = strlen(search);
    int replace_len = strlen(replace);
    int new_len = strlen(original) + count * (replace_len - search_len);
    
    // Allocate memory for result
    char *result = malloc(new_len + 1);
    if (!result) return NULL;
    
    // Build the result string
    char *dest = result;
    const char *src = original;
    
    while ((tmp = strstr(src, search)) != NULL) {
        // Copy everything before the match
        int prefix_len = tmp - src;
        strncpy(dest, src, prefix_len);
        dest += prefix_len;
        
        // Copy the replacement
        strcpy(dest, replace);
        dest += replace_len;
        
        // Move source pointer past the match
        src = tmp + search_len;
    }
    
    // Copy the remaining part
    strcpy(dest, src);
    
    return result;
}

// Add a file to the list
int add_file(FileList *list, const char *filepath) {
    if (list->count >= list->capacity) {
        // Resize array if needed
        list->capacity *= 2;
        list->files = realloc(list->files, sizeof(char*) * list->capacity);
        if (!list->files) {
            fprintf(stderr, "Memory reallocation failed\n");
            return -1;
        }
    }
    
    // Allocate memory for the filepath and copy it
    list->files[list->count] = malloc(strlen(filepath) + 1);
    if (!list->files[list->count]) {
        fprintf(stderr, "Memory allocation failed for filepath\n");
        return -1;
    }
    
    strcpy(list->files[list->count], filepath);
    list->count++;
    return 0;
}

// Check if file has .tsx extension
int has_tsx_extension(const char *filename) {
    const char *ext = strrchr(filename, '.');
    return (ext && strcmp(ext, ".tsx") == 0);
}

// Recursive function to scan directory
int scan_directory(const char *dirpath, FileList *list) {
    DIR *dir;
    struct dirent *entry;
    struct stat statbuf;
    char fullpath[MAX_PATH_LENGTH];
    
    dir = opendir(dirpath);
    if (!dir) {
        fprintf(stderr, "Cannot open directory: %s\n", dirpath);
        return -1;
    }
    
    while ((entry = readdir(dir)) != NULL) {
        // Skip current and parent directory entries
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
            continue;
        }
        
        // Build full path
        snprintf(fullpath, sizeof(fullpath), "%s/%s", dirpath, entry->d_name);
        
        // Get file/directory information
        if (stat(fullpath, &statbuf) == -1) {
            fprintf(stderr, "Cannot stat: %s\n", fullpath);
            continue;
        }
        
        if (S_ISDIR(statbuf.st_mode)) {
            // If it's a directory, recursively scan it
            if (scan_directory(fullpath, list) == -1) {
                closedir(dir);
                return -1;
            }
        } else if (S_ISREG(statbuf.st_mode)) {
            // If it's a regular file and has .tsx extension, add it to the list
            if (has_tsx_extension(entry->d_name)) {
                if (add_file(list, fullpath) == -1) {
                    closedir(dir);
                    return -1;
                }
                printf("Found: %s\n", fullpath);
            }
        }
    }
    
    closedir(dir);
    return 0;
}

// Free the file list memory
void free_file_list(FileList *list) {
    if (list) {
        if (list->files) {
            for (int i = 0; i < list->count; i++) {
                free(list->files[i]);
            }
            free(list->files);
        }
        free(list);
    }
}

// Print all files in the list
void print_file_list(const FileList *list) {
    
    printf("\n=== Files Found ===\n");
    printf("Total files: %d\n\n", list->count);
    
    printf("API Paths:\n");
    char *apiname = "api_name";
    for (int i = 0; i < list->count; i++) {

        char *tmp = strdup(list->files[i]);
        char *apitest = dirname(tmp);

        if (!apiname || strcmp(apiname, apitest) != 0) {
            apiname = (char *)malloc(strlen(apitest)+1);
            strcpy(apiname,apitest);
            printf("API: %s,%lu\n", apiname, strlen(apitest) + 1);
        }

        free(tmp);
    }

    free(apiname);
}

// Write file list to a text file (one file per line)
int write_file_list_to_text(const FileList *list, const char *output_file, const char *base_dir) {
    FILE *fp = fopen(output_file, "w");
    if (!fp) {
        fprintf(stderr, "Error: Cannot open file '%s' for writing\n", output_file);
        return -1;
    }
    
    fprintf(fp, "#!/bin/bash\n\n");
    
    // Write each file path
    for (int i = 0; i < list->count; i++) {

        char *baseline = replace_all(list->files[i], ".jsx", ".baseline.tsx");
        char *stage = replace_all(baseline, base_dir, ".");

        fprintf(fp, "rm -rf %s\n", baseline);
        fprintf(fp, "cp %s %s\n", list->files[i], baseline);
        fprintf(fp, "git add %s\n\n", stage);
        free(baseline);
        free(stage);    
    }
    
    fclose(fp);
    printf("File list written to: %s\n", output_file);
    return 0;
}

int main(int argc, char *argv[]) {
    const char *directory;
    const char *output_file = "base.sh";
    const char *format = "txt"; // default format
    FileList *tsx_files;
    
    // Check command line arguments
    if (argc < 2 || argc > 4) {
        printf("Usage: %s <directory_path> [output_file]\n", argv[0]);
        printf("Examples:\n");
        printf("  %s /path/to/project\n", argv[0]);
        return 1;
    }
    
    directory = argv[1];
    if (argc >= 3) {
        output_file = argv[2];
    }

    // Check if directory exists
    struct stat statbuf;
    if (stat(directory, &statbuf) != 0 || !S_ISDIR(statbuf.st_mode)) {
        fprintf(stderr, "Error: '%s' is not a valid directory\n", directory);
        return 1;
    }
    
    // Initialize file list
    tsx_files = init_file_list();
    if (!tsx_files) {
        return 1;
    }
    
    printf("Scanning directory: %s\n", directory);
    printf("Looking for .tsx files...\n\n");
    
    // Scan the directory recursively
    if (scan_directory(directory, tsx_files) == -1) {
        fprintf(stderr, "Error occurred during directory scanning\n");
        free_file_list(tsx_files);
        return 1;
    }
    
    // Print results to console
    print_file_list(tsx_files);
    
    // Write to file if output file specified
    if (output_file) {
        printf("\nWriting results to file...\n");
        
        // Default to text format
        write_file_list_to_text(tsx_files, output_file, directory);
    }
        
    // Clean up
    free_file_list(tsx_files);
    
    return 0;
}