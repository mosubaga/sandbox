const axios = require('axios');

const getjson = {

  fetchContent: (sURL) => 
    axios
      .get(sURL)
      .then(res => res.data)
      .catch(err => 'error')
};

module.exports = getjson;