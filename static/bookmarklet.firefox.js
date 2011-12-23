function vavpushBookmarklet(){
  var p = document.getElementById('video_player')
  var fV = p.attributes.flashvars.value;
  var attrs = fV.split('&');
  var vU, vtag, title, thumb, args = [];
  for (var i = 0; i<attrs.length;i++) {
    if (attrs[i].match("thumb")) {
        var url = unescape(attrs[i].split("=")[1]);
        thumb = url;
        vU = url.substring(0, url.lastIndexOf('/'));
    } else if (attrs[i].match("vtag")) {
        vtag = attrs[i].split("=")[1];
    }
  }
  title = document.getElementById("mv_min_title").innerHTML;

  args.push("thumb="+thumb);
  args.push("title="+encodeURIComponent(title));

  var rvU = vU + "/" + vtag + ".", videoUrl;
  var f = ["240", "360", "480", "720"];
  for (var i=0;i<f.length;i++){
    videoUrl = rvU+f[i]+".mp4";
    args.push("url="+videoUrl);
  }
  var resultUrl = "http://vavpush.appspot.com/submit?" + args.join("&");
//  var resultUrl = "http://192.168.0.103/submit?" + args.join("&");

  var card = [
    "<html><head><title>Add video ", title, " to watch queue</title></head>",
    "<body><img src='", thumb,"'><br/>" , title, "<br/><a href='", resultUrl,"'>add</a></body>"
  ];

  document.write(card.join(""));
}
setTimeout(vavpushBookmarklet, 100);
