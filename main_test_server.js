const express = require("express");
const app = express();
const ejs = require("ejs");
const mainRouter = require("./router/router");

app.get('/', function(req, res){
    res.send('Hello World')
});

app.use('/', mainRouter)

app.use("/views", express.static(__dirname + '/views'));
app.set('view engine', "ejs"); // 파일 확정자를 ejs로 해야 됨

// 8080Port로 연결 
app.listen(8000, function(){
    console.log("드디어 된다!")
});
