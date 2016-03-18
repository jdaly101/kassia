var express = require('express');
var swig = require('swig');

var app = express();
app.engine('html', swig.renderFile);
app.set('view engine', 'html');
app.set('views', __dirname + '/views');

app.use(express.static('.tmp'));

app.get('/', function(req, res) {
  res.render('index', {});
});

app.listen(3000);