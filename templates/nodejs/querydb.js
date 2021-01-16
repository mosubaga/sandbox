const mongodb = require('mongodb');
const MongoClient = mongodb.MongoClient;

const url = '[dburl]';
const dbName = '[dbname]';

// Use the connect method to create a connection w/ the database
MongoClient.connect(url, (err, client) => {
    if (err) {
        throw err;
        return;
    }

    console.log('Database connection successful');
    const db = client.db(dbName);
    const collection = db.collection([collection_name]);
    collection.find([filter]).toArray((err, docs) => {
        if (err) {
            throw err;
        }
        console.log(docs);
        client.close();
    });
});