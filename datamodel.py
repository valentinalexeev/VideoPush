#!/usr/bin/env python
#
# Copyright 2011,2012 Valentin Alexeev
# Data model
from google.appengine.ext import db

class VideoItem(db.Model):
	tvcookie = db.IntegerProperty()
	title = db.StringProperty()
	thumb = db.StringProperty()
	offset = db.IntegerProperty(default=0)

class VideoItemUrl(db.Model):
	videoitem = db.ReferenceProperty(VideoItem, collection_name = "urls")
	quality = db.StringProperty()
	url = db.StringProperty()

class TvAccess(db.Model):
    tvcookie = db.IntegerProperty()
    user = db.UserProperty()
    isadmin = db.BooleanProperty()