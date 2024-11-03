package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func main() {

	// Replace the URI with your MongoDB connection string.
	uri := "[MongoURL]" // or your MongoDB Atlas URI

	// Set client options
	clientOptions := options.Client().ApplyURI(uri)

	// Create a new MongoDB client
	client, err := mongo.NewClient(clientOptions)
	if err != nil {
		log.Fatal(err)
	}

	// Create a context with a timeout for the connection
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	// Connect to the MongoDB server
	err = client.Connect(ctx)
	if err != nil {
		log.Fatal(err)
	}

	// Ping the MongoDB server to verify the connection
	err = client.Ping(ctx, nil)
	if err != nil {
		log.Fatal("Unable to connect to MongoDB:", err)
	}
	fmt.Println("Connected to MongoDB!\n")

	// Choose the database and collection you want to work with
	collection := client.Database("[DataDB]").Collection("[CollectioName]")

	// Query for documents in the collection
	filter := bson.D{{"INT", bson.D{{"$gte", 90}}}} // Query to find documents where age > 25

	// Find the documents matching the filter
	cursor, err := collection.Find(ctx, filter)
	if err != nil {
		log.Fatal(err)
	}
	defer cursor.Close(ctx)

	// Iterate over the result set
	var results []bson.M
	if err = cursor.All(ctx, &results); err != nil {
		log.Fatal(err)
	}

	// Print the documents
	for _, result := range results {
		fmt.Println(result["INT"])
	}

	// Close the MongoDB connection when done
	if err := client.Disconnect(ctx); err != nil {
		log.Fatal(err)
	}
	fmt.Println("\nDisconnected from MongoDB.")
}
