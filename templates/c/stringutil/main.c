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
}
