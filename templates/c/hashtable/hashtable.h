
/* ===== hashtable.h ===== */
#ifndef HASHTABLE_H
#define HASHTABLE_H

#define HASH_TABLE_SIZE 100

// Forward declarations
typedef struct Entry Entry;
typedef struct HashTable HashTable;

// Structure definitions
struct Entry {
    char* key;
    char* value;
    struct Entry* next;
};

struct HashTable {
    Entry* buckets[HASH_TABLE_SIZE];
    int size;
};

// Function prototypes
HashTable* create_hashtable(void);
int hashtable_put(HashTable* ht, const char* key, const char* value);
char* hashtable_get(HashTable* ht, const char* key);
int hashtable_exists(HashTable* ht, const char* key);
int hashtable_remove(HashTable* ht, const char* key);
char** hashtable_keys(HashTable* ht, int* num_keys);
void hashtable_print(HashTable* ht);
void hashtable_destroy(HashTable* ht);

#endif /* HASHTABLE_H */
