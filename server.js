var express = require('express');
var request = require('request');
var app = express();
var server = require("http").createServer(app);
server.listen(3000, function () {
	console.log("server is listenning....")
});

var url =  'https://linksvip.net/GetLinkFs';
var headers =  {
	    'Content-Type': 'application/x-www-form-urlencoded',
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
		'Content-Length': '106',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Cookie': 'user=icarderx%40gmail.com;pass=4a65cd106ca7d10258560a017f486104',
		'Host': 'linksvip.net',
		'Referer': 'https: //linksvip.net/',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv: 53.0) Gecko/20100101 Firefox/53.0',
		'X-Requested-With': 'XMLHttpRequest'
  	};

app.get("/get", function(req, res){
	//res.end(req.query.link);
	var form = {
			link: 'https://www.fshare.vn/file/TJYWEZH7AIHM', 
			hash: 'y5MkLuNtItRVORyEUt224GrVb4lL.tev',
			pass: 'undefined',
			captcha: ''
		};
	request.post({ url: url, form: form, headers: headers }, function(error, response, body){
		 res.end(body);
	});
});

function hash() {
    var lenght = 32 || 9;
    var s = ""
    var code = "LinksVIP.Net2014eCrVtByNgMfSvDhFjGiHoJpKlLiEuRyTtYtUbInOj9u4y81r5o26q4a0v";
    for (var i = 0; i < lenght; i++) {
        s += code.charAt(Math.floor(Math.random() * code.length))
    }
    ;return s
}