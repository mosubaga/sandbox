/* ===== hashtable.c ===== */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "hashtable.h"

// Hash function - simple djb2 algorithm
static unsigned int hash(const char* key) {
    unsigned long hash = 5381;
    int c;
    
    while ((c = *key++)) {
        hash = ((hash << 5) + hash) + c; // hash * 33 + c
    }
    
    return hash % HASH_TABLE_SIZE;
}

// Create a new entry
static Entry* create_entry(const char* key, const char* value) {
    Entry* entry = malloc(sizeof(Entry));
    if (!entry) return NULL;
    
    // Allocate memory for key and value strings
    entry->key = malloc(strlen(key) + 1);
    entry->value = malloc(strlen(value) + 1);
    
    if (!entry->key || !entry->value) {
        free(entry->key);
        free(entry->value);
        free(entry);
        return NULL;
    }
    
    strcpy(entry->key, key);
    strcpy(entry->value, value);
    entry->next = NULL;
    
    return entry;
}

// Create a new hash table
HashTable* create_hashtable(void) {
    HashTable* ht = malloc(sizeof(HashTable));
    if (!ht) return NULL;
    
    // Initialize all buckets to NULL
    for (int i = 0; i < HASH_TABLE_SIZE; i++) {
        ht->buckets[i] = NULL;
    }
    ht->size = 0;
    
    return ht;
}

// Insert or update a key-value pair
int hashtable_put(HashTable* ht, const char* key, const char* value) {
    if (!ht || !key || !value) return 0;
    
    unsigned int index = hash(key);
    Entry* entry = ht->buckets[index];
    
    // Check if key already exists (update case)
    while (entry) {
        if (strcmp(entry->key, key) == 0) {
            // Update existing entry
            free(entry->value);
            entry->value = malloc(strlen(value) + 1);
            if (!entry->value) return 0;
            strcpy(entry->value, value);
            return 1;
        }
        entry = entry->next;
    }
    
    // Key doesn't exist, create new entry
    Entry* new_entry = create_entry(key, value);
    if (!new_entry) return 0;
    
    // Insert at beginning of chain (most efficient)
    new_entry->next = ht->buckets[index];
    ht->buckets[index] = new_entry;
    ht->size++;
    
    return 1;
}

// Get value by key
char* hashtable_get(HashTable* ht, const char* key) {
    if (!ht || !key) return NULL;
    
    unsigned int index = hash(key);
    Entry* entry = ht->buckets[index];
    
    while (entry) {
        if (strcmp(entry->key, key) == 0) {
            return entry->value;
        }
        entry = entry->next;
    }
    
    return NULL;  // Key not found
}

// Check if key exists
int hashtable_exists(HashTable* ht, const char* key) {
    return hashtable_get(ht, key) != NULL;
}

// Remove a key-value pair
int hashtable_remove(HashTable* ht, const char* key) {
    if (!ht || !key) return 0;
    
    unsigned int index = hash(key);
    Entry* entry = ht->buckets[index];
    Entry* prev = NULL;
    
    while (entry) {
        if (strcmp(entry->key, key) == 0) {
            // Remove entry from chain
            if (prev) {
                prev->next = entry->next;
            } else {
                ht->buckets[index] = entry->next;
            }
            
            // Free memory
            free(entry->key);
            free(entry->value);
            free(entry);
            ht->size--;
            
            return 1;
        }
        prev = entry;
        entry = entry->next;
    }
    
    return 0;  // Key not found
}

// Get all keys
char** hashtable_keys(HashTable* ht, int* num_keys) {
    if (!ht || !num_keys) return NULL;
    
    *num_keys = ht->size;
    if (ht->size == 0) return NULL;
    
    char** keys = malloc(sizeof(char*) * ht->size);
    if (!keys) return NULL;
    
    int key_count = 0;
    for (int i = 0; i < HASH_TABLE_SIZE; i++) {
        Entry* entry = ht->buckets[i];
        while (entry) {
            keys[key_count] = malloc(strlen(entry->key) + 1);
            if (keys[key_count]) {
                strcpy(keys[key_count], entry->key);
                key_count++;
            }
            entry = entry->next;
        }
    }
    
    return keys;
}

// Print all key-value pairs
void hashtable_print(HashTable* ht) {
    if (!ht) return;
    
    printf("Hash Table Contents:\n");
    printf("Size: %d\n", ht->size);
    
    for (int i = 0; i < HASH_TABLE_SIZE; i++) {
        Entry* entry = ht->buckets[i];
        if (entry) {
            printf("Bucket %d: ", i);
            while (entry) {
                printf("[\"%s\" => \"%s\"]", entry->key, entry->value);
                entry = entry->next;
                if (entry) printf(" -> ");
            }
            printf("\n");
        }
    }
}

// Free hash table memory
void hashtable_destroy(HashTable* ht) {
    if (!ht) return;
    
    for (int i = 0; i < HASH_TABLE_SIZE; i++) {
        Entry* entry = ht->buckets[i];
        while (entry) {
            Entry* temp = entry;
            entry = entry->next;
            free(temp->key);
            free(temp->value);
            free(temp);
        }
    }
    
    free(ht);
}
