var tmdbConfig = {};
        
function tmdb_searchComplete(data) {
    for (var i = 0; i < Math.min(data.results.length, 6); i++) {
        $("#vavpush-tmdb-title" + i).text(data.results[i].title);
        if (data.results[i].poster_path != null) {
            $("#vavpush-tmdb-poster" + i).attr('src', tmdbConfig.base_url + "w154" + data.results[i].poster_path);
        }
        $("#vavpush-tmdb" + i).click({"data":data.results[i]}, function(event){
            vavp_thumb = tmdbConfig.base_url + "w154" + event.data.data.poster_path;
            vavp_title = event.data.data.title;
        });
    }
}

function tmdb_configComplete(data) {
    tmdbConfig.base_url = data.images.base_url;
}

function tmdb_search(query) {
    $.ajax({
        type: 'GET',
        url: api_root + 'search/movie',
        data: { "api_key": api_key, "language": "ru", "query": query},
        async: false,
        jsonpCallback: 'tmdb_searchComplete',
        contentType: 'application/json',
        dataType: 'jsonp',
        error: function(e) {
            console.log(e.message);
        }
    });
}

var api_root = "http://api.themoviedb.org/3/";
var api_key = "79c258d92fe4a66bab98194657b945e4";

function scriptLoaded() {
    $.ajax({
        type: 'GET',
        url: api_root + 'configuration',
        data: { "api_key": api_key },
        async: false,
        jsonpCallback: 'tmdb_configComplete',
        contentType: 'application/json',
        dataType: 'jsonp',
        error: function(e) {
            console.log(e.message);
        }
    });

    vavpushBookmarklet();
}

var vavp_title, vavp_thumb, vavp_args = [];

function submitVaVpush() {
  vavp_args.push("thumb="+vavp_thumb);
  vavp_args.push("title="+encodeURIComponent(vavp_title));
  var resultUrl = "http://2.vavpush.appspot.com/submit?" + vavp_args.join("&");
  location.href = resultUrl;
}

function vavpushBookmarklet(){
  var p = $('#video_player')[0];
  var fV = p.attributes.flashvars.value;
  var attrs = fV.split('&');

  for (var i = 0; i<attrs.length;i++) {
    var kv = attrs[i].split("=");

    if (kv[0].indexOf("thumb") == 0) {
        thumb = unescape(attrs[i].split("=")[1]);
        break;
    }
  }

  // get title
  vavp_title = $("#mv_min_title")[0].innerText;
  // ask TMDB for more info
  tmdb_search(vavp_title);

  // prepare quality attributes
  var f = ["240", "360", "480", "720"];

  for (var i = 3; i > video_max_hd; i--) {
    f.pop();
  }

  for (var i=0;i<f.length;i++){
    vavp_args.push("url="+pathToHD(f[i]));
  }
  var formats = "q=" + f.join("&q=");

  // prepare the resulting URL
  vavp_args.push(formats);

  // create a new confirmation card
  var card = [
    "<div><div>Add video ", vavp_title, " to watch queue</div>",
    "<div><img src='", thumb,"'><br/>" , vavp_title, "<br/><a onclick='submitVaVpush();return true;'>Add</a></div></div>"
  ];

  $("#vavpush-vkinfo").html(card.join(""));

  $("#vavpush-close").click(function() {
    $("#vavpush-dialog").remove();
  });
};

function pathToHD(res) {
  var s = (video_host.substr(0, 4) == "http")
    ? video_host
    : 'http://cs' + video_host + '.vkontakte.ru/';

  return s + 'u' + video_uid + '/video/' + video_vtag + '.' + res + '.mov';
}

