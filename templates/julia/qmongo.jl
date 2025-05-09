using Mongoc

# Connect to MongoDB (change parameters as needed)
client = Mongoc.Client(CONNECTION_STRING)

# Access a specific database
db = Mongoc.Database(client, DB_NAME)

# Access a specific collection
collection = Mongoc.Collection(db, COLLECTION_NAME)

# Query all documents
cursor = Mongoc.find(collection)

# Iterate over the results
for doc in cursor
    println(doc[KEY1] , " :: " , doc[KEY2])
end

# Optionally, close the client
Mongoc.destroy!(client)
