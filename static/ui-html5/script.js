function CoverList() {
  this._data = [];
  this._selected = -1;
}

CoverList.prototype.clearAll = function() {
  this._data = [];
  this._selected = -1;

  $("#covers").empty();
}

CoverList.prototype.addJsonItem = function (jsonItem, noRedraw) {
  this._data.push(jsonItem);
  if (this._data.length == 1) {
    this._selected = 0;
  }
  this.drawItem($("#covers"), this._data[this._data.length - 1], this._data.length - 1);
}

CoverList.prototype.drawItem = function (container, data, i) {
  var k = document.createElement('img');
  k.src = data.cover;
  k.className = "cover";
  k.id = "cover" + i;
  k.clid = i;
  container.append(k);
  $("#" + k.id).click(function(event){
    cl.setSelected(event.target.clid);
    showDetails();
  });
  if (i == this._selected) {
    this.markSelected();
  }
}

CoverList.prototype.markSelected = function () {
  var data = this._data[this._selected];
  $("#cover" + this._selected).addClass("cover-selected");
  $("#title").text(data.title);
  $("#descr").text(data.description);
}

CoverList.prototype.setSelected = function (newSelected) {
  $("#cover"+this._selected).removeClass("cover-selected");
  this._selected = newSelected;
  this.markSelected();
}

CoverList.prototype.redraw = function() {
  $("#covers").empty();
  for(var i = 0; i < this._data.length; i++) {
    this.drawItem($("#covers"), this._data[i], i);
  }
}

CoverList.prototype.getSelected = function () {
  if (this._selected >= 0) {
    return this._data[this._selected];
  }
  return {};
}

CoverList.prototype.next = function(shift) {
  if (!shift) {
    shift = 1
  }

  $("#cover"+this._selected).removeClass("cover-selected");

  this._selected = Math.min(Math.max(0, (this._selected + shift) % this._data.length), this._data.length - 1);

  this.markSelected();
}

var cl = new CoverList();

function clearAll() {
  cl.clearAll();
}

function addJsonItem(){
  var json = {
    title:"kddkenfkdnd" + Math.random(),
    description:"dkhkddcnknc;kljl;jfdsgl;skdjgfl;dsjgl;jkdsg;lskjfl;sdjgl;kdsjgklsjfdg;lsjkdgflj",
    cover:"http://st.kinopoisk.ru/images/film_big/571288.jpg",
    urls:{240:"1"}
  };
  cl.addJsonItem(json, false);
}

function next() {
  cl.next();
}

function down() {
  cl.next(9);
}

function up() {
  cl.next(-9);
}

function prev() {
  cl.next(-1);
}

function showDetails() {
  var selected = cl.getSelected();
  if (selected != {}) {
    
    $("#details-title").text(selected.title);
    $("#details-cover")[0].src = selected.cover;
    $("#details-descr").text(selected.description);

    $("#details-overlay").show();
    $("#details").show();
  }
}

function hideDetails() {
  $("#details-overlay").hide();
  $("#details").hide();
  $("#covers").focus();
}

function fromJson() {
  $.ajax({
    url: "/ajax?method=list",
    dataType: "text json",
    contentType: "application/json; charset=utf-8",
  }).done(function(data){
    for (var i = 0; i < data.items.length; i++) {
      cl.addJsonItem(data.items[i]);
    }
  }).error(function (jqXHR, textStatus, errorThrown) {
        alert (textStatus);
        alert (errorThrown);
  });
}

$(window).ready(function(){
  $("html body").keyup(function(event) {
    switch (event.which) {
      case VK_UP: up(); break;
      case VK_DOWN: down(); break;
      case VK_LEFT: prev(); break;
      case VK_RIGHT: next(); break;
      case VK_ENTER: showDetails(); break;
      case VK_0: hideDetails(); break;
    }
    event.preventDefault();
  });

  $("#covers").focus();
  fromJson();
});
