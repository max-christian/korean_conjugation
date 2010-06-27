var sys = require('sys'),
    fs  = require('fs');

fs.readdir('./test', function(err, files) {
    files.forEach(function(file) {
        f = require('./test/' + file.replace('.js', ''));
    });
});
