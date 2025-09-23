#ifndef FILE_UTILS_H
#define FILE_UTILS_H

#include <stddef.h>  // for size_t

// -----------------------------------------------------------------------------
// File Utilities (file_utils.c)
// -----------------------------------------------------------------------------

// Read entire file into a malloc'ed buffer (caller must free)
char *read_file_fast(const char *filepath);

// Write a string to a file
// Returns 1 on success, 0 on failure
int write_file_fast(const char *filepath, const char *content);

// Read file lines into malloc'ed array of strings
// Caller must free each string and the array itself
// out_count will contain the number of lines
char **read_lines_fast(const char *filepath, size_t *out_count);

// Write array of strings to a file
// Returns 1 on success, 0 on failure
int write_lines_fast(const char *filepath, char **lines, size_t count);

// List files in a directory (excluding "." and "..")
// Returns malloc'ed array of malloc'ed strings (caller must free all)
// out_count will contain the number of entries
char **list_directory(const char *path, size_t *out_count);

// Get file size in bytes
// Returns 0 on error
size_t get_file_size(const char *filepath);

// Check if file exists (1 if yes, 0 if no)
int file_exists(const char *filepath);

// Check if directory exists (1 if yes, 0 if no)
int directory_exists(const char *path);

// Create directory (non-recursive)
// Returns 1 on success or if already exists, 0 on failure
int create_directory(const char *path);

// Delete a file
// Returns 1 on success, 0 on failure
int delete_file(const char *filepath);

// Copy file contents from source to destination
// Returns 1 on success, 0 on failure
int copy_file_fast(const char *source, const char *destination);

// Move (rename) file
// Returns 1 on success, 0 on failure
int move_file_fast(const char *source, const char *destination);

// Search for a substring inside a file
// Returns 1 if found, 0 otherwise
int search_in_file(const char *filepath, const char *search_term);

// Count the number of lines in a file
// Returns 0 on error
size_t count_lines(const char *filepath);

#endif // FILE_UTILS_H
