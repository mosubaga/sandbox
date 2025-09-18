#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <sys/stat.h>
#include <string.h>
#include <ctype.h>

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