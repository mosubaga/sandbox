var http = require('http');
var fs = require('fs');

http.createServer(function (req, res) {
    res.writeHead(200, {'Content-Type': 'text/html'});

    var keyword  = '[KeyWord]';
    var root_dir = "[RootDir]";
    var files    = walk(root_dir);
    var match    = /^.*\.([FileExt])$/;

    var i = 0;

    res.write('<b>Found following:</b><br><br>');

    for (var x in files){
       if (match.test(files[x])){
          var j = 1;
          var lines = fs.readFileSync(files[x]).toString().split('\n');
          for (var k = 0, len = lines.length; k < len; k++) {
            if (lines[k].match(keyword)){
                files[x] = files[x].replace(root_dir,"");
                res.write(files[x]+" ("+ j +") :");
                res.write(lines[k]);
                res.write('<br>');
                i++;
            }
          j++;
          }
       }
    }

    res.write("<br><b>Found " + i + "hits</b>");
    res.end('<br><b>List Complete</b>');
}).listen(8080);

var walk = function(dir) {
    var results = []
    var list = fs.readdirSync(dir)
    list.forEach(function(file) {
    	console.log(file)
        file = dir + '/' + file
        var stat = fs.statSync(file)
        if (stat && stat.isDirectory()) results = results.concat(walk(file))
        else results.push(file)
    })
    return results
}
