(function () {function lS(u,c) {var s = document.createElement("script");s.type = "text/javascript";if (s.readyState) s.onreadystatechange = function () {if (s.readyState == "loaded" || s.readyState == "complete") {s.onreadystatechange = null;c();}};else s.onload = function () {c();};s.src = u;document.getElementsByTagName("head")[0].appendChild(s);}lS("https://ajax.googleapis.com/ajax/libs/jquery/1.8.0/jquery.min.js", function () {var b="http://localhost:8080/static/";$('head').append( $('<link rel="stylesheet" type="text/css" />').attr('href', b+'card.css') );$('body').append($('<div id="vavpush-dialog"/>'));$("#vavpush-dialog").load(b+"card.html");$.getScript(b+"card.js", function() { scriptLoaded(); });});})();
