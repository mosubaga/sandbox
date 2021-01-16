const mongoose = require('mongoose');
mongoose.connect([db_url]);

const Schema = mongoose.Schema;
const Hitters = mongoose.model("DB", new Schema({}), "[collection_name]");
Hitters.find({[filter]}, function(err, doc)
{
    console.log((doc))
    mongoose.connection.close()
})
