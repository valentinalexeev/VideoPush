#!/usr/bin/env python
#
# Copyright 2011,2012 Valentin Alexeev
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch

import cgi
import os
import urllib2
from urlparse import urlsplit
import logging
import httplib

from datamodel import *

class MainHandler(webapp.RequestHandler):
	def get(self):
		if 'tvcookie' in self.request.cookies:
			tvcookie = int(cgi.escape(self.request.cookies['tvcookie']))
			#videos = db.GqlQuery("SELECT * FROM VideoItem WHERE tvcookie = :1 ORDER BY title", tvcookie)
			videos = db.GqlQuery("SELECT * FROM VideoItem WHERE tvcookie = :1", tvcookie)
			template_values = {
				'videos': videos,
				'logout': users.create_logout_url('/')
			}
			path = os.path.join(os.path.dirname(__file__), 'templates/list.html')
			self.response.out.write(template.render(path, template_values))
		else:
			self.redirect('/static/tvlogin.html')

class VideoItemHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            if 'tvcookie' in self.request.cookies:
				tvcookie = int(cgi.escape(self.request.cookies['tvcookie']))
				q = db.GqlQuery('SELECT * FROM TvAccess WHERE user = :1 AND tvcookie = :2', user, tvcookie)
												
				if q.get():
					logging.info('User %s access ok to tv %s', user, tvcookie)
					
					item = VideoItem()
					item.tvcookie = tvcookie
					item.title = cgi.escape(self.request.get('title'))
					item.thumb = cgi.escape(self.request.get('thumb'))
					item.put()
					
					urlsL = self.request.get_all('url')
					qualitiesL = self.request.get_all('q')
					
					for pair in zip(urlsL, qualitiesL):
						logging.info("Adding URL %s for %s", pair[0], tvcookie)
						itemurl = VideoItemUrl()
						itemurl.videoitem = item
						itemurl.url = cgi.escape(pair[0])
						itemurl.quality = cgi.escape(pair[1])
						itemurl.put()
					self.redirect('/')
				else:
					logging.info('User %s access failed to tv %s', user, tvcookie)
					self.redirect('/static/error.noaccess.html')
            else:
                self.redirect('/static/tvlogin.html')
        else:
            self.redirect(users.create_login_url(self.request.uri))

class VideoPlayerHandler(webapp.RequestHandler):
    def get(self):
		key = cgi.escape(self.request.get('key'))
		quality = cgi.escape(self.request.get('quality'))
		vi = None
		
		try:
			vi = VideoItem.get(key)
		except:
			self.redirect('/static/error.nosuchvideo.html')
			return
		
		urlItem = vi.urls.filter("quality = ", quality).get()
		
		if not urlItem:
			self.redirect('/static/error.nosuchquality.html')
			return
		
		template_values = {
			'thumb': vi.thumb,
			'offset': vi.offset,
			'url': urlItem.url,
			'key': key
		}
		
		player = "templates/player-object.html";
		
		if "SmartTV" in self.request.headers['User-Agent']:
			# let's try to use <video> player
			player = "templates/player-video.html";
		
		path = os.path.join(os.path.dirname(__file__), player)
		self.response.out.write(template.render(path, template_values))

class VideoDeleteHandler(webapp.RequestHandler):
    def get(self):
        if 'tvcookie' in self.request.cookies:
			item = VideoItem.get(cgi.escape(self.request.get('key')))
			for url in item.urls:
				url.delete()
			item.delete()
			self.redirect('/')
        else:
            self.redirect('/static/tvlogin.html')

class VideoPauseHandler(webapp.RequestHandler):
	def get(self):
		if 'tvcookie' in self.request.cookies:
			item = VideoItem.get(cgi.escape(self.request.get('key')))
			item.offset = cgi.escape(self.request.get('offset'))
			item.put()
			self.redirect('/')
		else:
			self.redirect('/static/tvlogin.html')

class TvLoginHandler(webapp.RequestHandler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'tvcookie=' + cgi.escape(self.request.get('tvcookie')) + ";max-age=" + str(60 * 60 * 24 * 365) + ";path=/")
        self.redirect('/')

class TvLogoutHandler(webapp.RequestHandler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'tvcookie=;Max-Age=0;path=/')
        self.redirect(users.create_logout_url('/'))

class TvRegisterHandler(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		
		if user:	
			if users.is_current_user_admin():
				access = TvAccess();
				access.tvcookie = int(cgi.escape(self.request.get('tvcookie')))
				access.user = users.User(cgi.escape(self.request.get('userid')))
				access.put()
				self.redirect('/static/tvregister.html')
			else:
				self.redirect('/static/error.unauthorized.html')
		else:
			self.redirect(users.create_login_url(self.request.uri))	

# Entry point

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([
        ('/', MainHandler),
        ('/submit', VideoItemHandler),
        ('/delete', VideoDeleteHandler),
        ('/player', VideoPlayerHandler),
        ('/tvlogin', TvLoginHandler),
		('/tvlogout', TvLogoutHandler),
		('/tvregister', TvRegisterHandler),
		('/pause', VideoPauseHandler)
        ],debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
