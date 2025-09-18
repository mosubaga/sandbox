/* ===== example_usage.c ===== */
#include <stdio.h>
#include <stdlib.h>
#include "hashtable.h"

int main() 
{

    // Create hash table
    HashTable* ht = create_hashtable();
    if (!ht) {
        printf("Failed to create hash table\n");
        return 1;
    }
    
    // Insert some key-value pairs
    hashtable_put(ht, "name", "Alice");
    hashtable_put(ht, "age", "25");
    hashtable_put(ht, "city", "Boston");
    hashtable_put(ht, "occupation", "Engineer");
    
    // Retrieve and display values
    printf("Name: %s\n", hashtable_get(ht, "name"));
    printf("Age: %s\n", hashtable_get(ht, "age"));
    printf("City: %s\n", hashtable_get(ht, "city"));
    printf("Occupation: %s\n", hashtable_get(ht, "occupation"));
    
    // Check existence
    if (hashtable_exists(ht, "email")) {
        printf("Email exists\n");
    } else {
        printf("Email doesn't exist\n");
    }
    
    // Update value
    hashtable_put(ht, "age", "26");
    printf("Updated age: %s\n", hashtable_get(ht, "age"));
    
    // Display all contents
    printf("\n");
    hashtable_print(ht);
    
    // Get and display all keys
    int num_keys;
    char** keys = hashtable_keys(ht, &num_keys);
    if (keys) {
        printf("\nAll keys:\n");
        for (int i = 0; i < num_keys; i++) {
            printf("  %s\n", keys[i]);
            free(keys[i]);
        }
        free(keys);
    }
    
    // Remove a key
    if (hashtable_remove(ht, "city")) {
        printf("\nRemoved 'city' successfully\n");
        hashtable_print(ht);
    }
    
    // Clean up
    hashtable_destroy(ht);
    printf("\nHash table destroyed\n");
    
    return 0;
}
