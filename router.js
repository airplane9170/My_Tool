const express  = require("express");
const router   = express.Router();

router.get('/main_window', function(req, res){
    res.render("doit_javascript", {title:'EJS'}) // 그림파일을 전달할 때 render() 사용, 그림과 데이터를 같이 보냄({title:'EJS'})
});

router.post('/plz_do', function(req, res){
    console.log(req.body)
});

module.exports = router;