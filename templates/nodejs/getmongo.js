const mongodb = require('mongodb');
const MongoClient = mongodb.MongoClient;

const url = '[mongo_url]';
const dbName = '[db_name]';

// Use the connect method to create a connection w/ the database
MongoClient.connect(url, (err, client) => {
    if (err) {
        throw err;
        return;
    }

    console.log('Database connection successful');
    const db = client.db(dbName);
    const collection = db.collection('npblegends');
    collection.find([filter]).toArray((err, docs) => {
        if (err) {
            throw err;
        }
        
        docs.forEach(sb =>{
            console.log(`[something]`)
        })
        client.close();
    });
});