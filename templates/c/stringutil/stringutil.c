#include <ctype.h>
#include <regex.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LENGTH 4096 // Define a maximum line length

// -------------------------------------------------------
char *replace_all(const char *original, const char *search, const char *replace)
// -------------------------------------------------------
{

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

// Function to check if a file has the specified keyword
// -------------------------------------------------------
int does_contain(const char *text, const char *substring)
// -------------------------------------------------------
{

    char *result = strstr(text, substring);

    if (result != NULL) {
        return 1;
    }

    return 0;
}

// -------------------------------------------------------
char *trim(const char *str)
// -------------------------------------------------------
{
    // Allocate buffer for copy (including null terminator)
    char *copy = malloc(strlen(str) + 1);
    if (!copy) return NULL;
    strcpy(copy, str);

    char *start = copy;
    char *end;

    // Trim leading spaces
    while (isspace((unsigned char)*start)) start++;

    // If all spaces
    if (*start == 0) {
        copy[0] = '\0';
        return copy;
    }

    // Trim trailing spaces
    end = start + strlen(start) - 1;
    while (end > start && isspace((unsigned char)*end)) end--;
    *(end + 1) = '\0';

    // Move trimmed string to beginning of buffer if needed
    if (start != copy) {
        memmove(copy, start, end - start + 2); // +1 for length, +1 for null
    }

    return copy;
}

// -------------------------------------------------------
char *regex_group(const char *text, const char *pattern, size_t group_index)
// -------------------------------------------------------
{
    if (!text || !pattern) return NULL;

    regex_t regex;
    if (regcomp(&regex, pattern, REG_EXTENDED) != 0) {
        return NULL;
    }

    size_t match_count = regex.re_nsub + 1;
    regmatch_t *matches = calloc(match_count, sizeof(regmatch_t));
    if (!matches) {
        regfree(&regex);
        return NULL;
    }

    int exec_status = regexec(&regex, text, match_count, matches, 0);
    if (exec_status != 0) {
        free(matches);
        regfree(&regex);
        return NULL;
    }

    if (group_index >= match_count) {
        free(matches);
        regfree(&regex);
        return NULL;
    }

    regmatch_t match = matches[group_index];
    if (match.rm_so == -1 || match.rm_eo == -1) {
        free(matches);
        regfree(&regex);
        return NULL;
    }

    size_t length = (size_t)(match.rm_eo - match.rm_so);
    char *result = malloc(length + 1);
    if (!result) {
        free(matches);
        regfree(&regex);
        return NULL;
    }

    memcpy(result, text + match.rm_so, length);
    result[length] = '\0';

    free(matches);
    regfree(&regex);
    return result;
}

// -------------------------------------------------------
int regex_group_count(const char *pattern)
// -------------------------------------------------------
{
    if (!pattern) return -1;

    regex_t regex;
    if (regcomp(&regex, pattern, REG_EXTENDED) != 0) {
        return -1;
    }

    int count = (int)regex.re_nsub;
    regfree(&regex);
    return count;
}

// -------------------------------------------------------
int regex_matches(const char *text, const char *pattern)
// -------------------------------------------------------
{
    if (!text || !pattern) return 0;

    regex_t regex;
    if (regcomp(&regex, pattern, REG_EXTENDED) != 0) {
        return -1;
    }

    int status = regexec(&regex, text, 0, NULL, 0);
    regfree(&regex);

    return status == 0 ? 1 : 0;
}

// -------------------------------------------------------
char *regex_replace_all(const char *text, const char *pattern, const char *replacement)
// -------------------------------------------------------
{
    if (!text || !pattern || !replacement) return NULL;

    regex_t regex;
    if (regcomp(&regex, pattern, REG_EXTENDED) != 0) {
        return NULL;
    }

    size_t replacement_len = strlen(replacement);
    size_t capacity = strlen(text) + 1;
    char *result = malloc(capacity);
    if (!result) {
        regfree(&regex);
        return NULL;
    }

    size_t result_len = 0;
    const char *cursor = text;
    regmatch_t match;

    while (regexec(&regex, cursor, 1, &match, 0) == 0) {
        if (match.rm_so == match.rm_eo) {
            if (*cursor == '\0') {
                break;
            }

            if (result_len + 2 > capacity) {
                capacity *= 2;
                char *resized = realloc(result, capacity);
                if (!resized) {
                    free(result);
                    regfree(&regex);
                    return NULL;
                }
                result = resized;
            }

            result[result_len++] = *cursor;
            cursor++;
            continue;
        }

        size_t prefix_len = (size_t)match.rm_so;
        size_t needed = result_len + prefix_len + replacement_len + 1;
        if (needed > capacity) {
            while (capacity < needed) {
                capacity *= 2;
            }
            char *resized = realloc(result, capacity);
            if (!resized) {
                free(result);
                regfree(&regex);
                return NULL;
            }
            result = resized;
        }

        memcpy(result + result_len, cursor, prefix_len);
        result_len += prefix_len;
        memcpy(result + result_len, replacement, replacement_len);
        result_len += replacement_len;

        cursor += match.rm_eo;
    }

    size_t remaining = strlen(cursor);
    if (result_len + remaining + 1 > capacity) {
        capacity = result_len + remaining + 1;
        char *resized = realloc(result, capacity);
        if (!resized) {
            free(result);
            regfree(&regex);
            return NULL;
        }
        result = resized;
    }

    memcpy(result + result_len, cursor, remaining);
    result_len += remaining;
    result[result_len] = '\0';

    regfree(&regex);
    return result;
}
