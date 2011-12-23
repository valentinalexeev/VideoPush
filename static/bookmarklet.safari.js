function vavpushBookmarklet(){
    var v=document.getElementById('theVideo');
    s=v.children;
    var r=[];
    for(var i=0;i<s.length;i++){
        r.push("<a href='http://vavpush.appspot.com/submit?url="+s[i].src+"&thumb="+v.attributes.poster.value+"&title="+document.getElementById('mv_min_title').innerHTML+"'>"+s[i].src+"</a>");
    }
    document.write(r.join("<br/>"))
}

setTimeout(vavpushBookmarklet, 100);