#ifndef STRINGUTIL_H
#define STRINGUTIL_H

#include <stddef.h>

// Define the same maximum line length as in the source file
#define MAX_LINE_LENGTH 4096

// Replaces all occurrences of 'search' with 'replace' in 'original'.
// Returns a newly allocated string (must be freed by caller).
// Returns NULL if allocation fails or input is invalid.
char *replace_all(const char *original, const char *search, const char *replace);

// Checks if 'substring' is contained within 'text'.
// Returns 1 if found, 0 otherwise.
int does_contain(const char *text, const char *substring);

// Trims leading and trailing whitespace from a string.
// Returns a pointer to the trimmed string.
char *trim(char *str);

#endif // STRINGUTIL_H
