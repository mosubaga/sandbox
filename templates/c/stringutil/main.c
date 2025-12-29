#include <stdio.h>
#include <stdlib.h>
#include "stringutil.h"

int main()
{

   printf("== Test Started ==\n");

   printf("== Testing String replace ==\n");
   char *original = "Hello, World!";
   char *search = "World";
   char *replace = "Universe";
   char *result = replace_all(original, search, replace);
   printf("Original: %s\n", original);
   printf("Result: %s\n", result);
   free(result);

   printf("== Testing String contains ==\n");
   char *text = "Hello, World!";
   char *substring = "World";

   printf("String: '%s'\n", text);
   int contains = does_contain(text, substring);
   printf("Contains 'World': %d\n", contains);

   substring = "Goodbye";
   contains = does_contain(text, substring);
   printf("Contains 'Goodbye': %d\n", contains);

   printf("== Testing String trim ==\n");
   char *str = "   Hello World!!   ";
   printf("String with space: '%s'\n", str);
   char *trimmed = trim(str);
   printf("Trimmed: '%s'\n", trimmed);
   free(trimmed);

   printf("== Testing Regex group functions ==\n");
   const char *email = "nhayashi@example.com";
   const char *pattern = "(.*)@(.*)\\.com";
   printf("Regex group count: %d\n", regex_group_count(pattern));

   char *group1 = regex_group(email, pattern, 1);
   char *group2 = regex_group(email, pattern, 2);
   printf("Regex group 1: '%s'\n", group1 ? group1 : "(null)");
   printf("Regex group 2: '%s'\n", group2 ? group2 : "(null)");
   free(group1);
   free(group2);

   printf("Regex matches: %d\n", regex_matches(email, pattern));

   char *regex_replaced = regex_replace_all(email, "@example\\.com", "@example.org");
   printf("Regex replaced: %s\n", regex_replaced ? regex_replaced : "(null)");
   free(regex_replaced);
}
