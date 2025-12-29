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
char *trim(const char *str);

// Returns a newly allocated string for a regex capture group.
// group_index 0 is the entire match, 1+ are capture groups.
// Returns NULL on no match, invalid index, or error.
char *regex_group(const char *text, const char *pattern, size_t group_index);

// Returns the number of capture groups in the regex pattern.
// Returns -1 if the pattern is invalid.
int regex_group_count(const char *pattern);

// Checks whether the entire text matches the regex pattern.
// Returns 1 for a match, 0 for no match, -1 for invalid pattern.
int regex_matches(const char *text, const char *pattern);

// Replaces all matches of the regex pattern with the replacement string.
// Returns a newly allocated string (must be freed by caller).
char *regex_replace_all(const char *text, const char *pattern, const char *replacement);

#endif // STRINGUTIL_H
