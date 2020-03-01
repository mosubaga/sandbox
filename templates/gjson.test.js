const getjson = require('./gjson');

test('Test template', () => {
  const sURL = "<URL>";
  console.log(sURL);
  return getjson.fetchContent(sURL).then(data => {
     expect("<json.data>").toEqual("something");
  });
});

