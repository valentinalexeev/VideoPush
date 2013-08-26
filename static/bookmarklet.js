function vavpushBookmarklet(){
  // get the thumbnail from flash player's flashvars
  var p = document.getElementById('video_player')
  var fV = p.attributes.flashvars.value;
  var attrs = fV.split('&');

  var title, thumb, args = [];

  for (var i = 0; i<attrs.length;i++) {
    var kv = attrs[i].split("=");

    if (kv[0].indexOf("jpg") == 0) {
        thumb = unescape(attrs[i].split("=")[1]);
        break;
    }
  }

  // get title
  title = document.getElementById("mv_min_title").innerHTML;

  // prepare quality attributes
  var f = ["240", "360", "480", "720"];

  for (var i = 3; i > video_max_hd; i--) {
    f.pop();
  }

  for (var i=0;i<f.length;i++){
    args.push("url="+pathToHD(f[i]));
  }
  var formats = "q=" + f.join("&q=");

  // prepare the resulting URL
  args.push(formats);
  args.push("thumb="+thumb);
  args.push("title="+encodeURIComponent(title));

  var resultUrl = "http://vavpush.appspot.com/submit?" + args.join("&");

  // create a new confirmation card
  var card = [
    "<html><head><title>Add video ", title, " to watch queue</title></head>",
    "<body><img src='", thumb,"'><br/>" , title, "<br/><a href='", resultUrl,"'>add</a></body>"
  ];

  // show the card
  document.write(card.join(""));
};

function pathToHD(res) {
  return [ 'http://cs', video_host, '.vk.me/u', video_uid, '/videos/', video_vtag, '.', res, '.mp4' ].join("");
}

setTimeout(vavpushBookmarklet, 100);
