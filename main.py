#!/usr/bin/env python
#
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
from google.appengine.ext import db
import cgi
import os
import urllib2
import logging
                                      
class MainHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            videos = db.GqlQuery("SELECT * FROM VideoSubmit WHERE author = :1", user)
            template_values = {
                'videos': videos,
                'logout': users.create_logout_url('/')
            }
            path = os.path.join(os.path.dirname(__file__), 'templates/list.html')
            self.response.out.write(template.render(path, template_values))
        
        else:
            self.redirect(users.create_login_url(self.request.uri))

class VideoSubmitHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            urls = self.request.get_all('url')

            for url in urls:
                logging.info("Adding URL %s for %s", url, user)
                item = VideoSubmit()
                item.author = user
                item.url = cgi.escape(url)
                item.title = cgi.escape(self.request.get('title'))
                item.thumb = cgi.escape(self.request.get('thumb'))
                item.put()
#                request = urllib2.Request(url)
#                request.get_method = lambda: 'HEAD'
#                try:
#                    response = urllib2.urlopen(request)
#                    logging.info("Adding URL %s for %s", url, user)

#                    item = VideoSubmit()
#                    item.author = user
#                    item.url = cgi.escape(url)
#                    item.title = cgi.escape(self.request.get('title'))
#                    item.thumb = cgi.escape(self.request.get('thumb'))
#                    item.put()
#                except urllib2.HTTPError, e:
#                    logging.info("Failed to add URL %s for %s code %i", url, user, e.code)
#                    self.response.out.write(e.code);
            self.redirect('/')
        else:
            self.redirect(users.create_login_url(self.request.uri))

class VideoPlayerHandler(webapp.RequestHandler):
    def get(self):
        template_values = {
            'url': cgi.escape(self.request.get('url'))
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/player.html')
        self.response.out.write(template.render(path, template_values))

class VideoDeleteHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            videos = db.GqlQuery("SELECT * FROM VideoSubmit WHERE author = :1 AND url = :2", user, cgi.escape(self.request.get('url')))
            for video in videos:
                video.delete()
            self.redirect('/')
        
        else:
            self.redirect(users.create_login_url(self.request.uri))

class VideoSubmit(db.Model):
    author = db.UserProperty()
    url = db.StringProperty()
    title = db.StringProperty()
    thumb = db.StringProperty()

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([
        ('/', MainHandler),
        ('/submit', VideoSubmitHandler),
        ('/delete', VideoDeleteHandler),
        ('/player', VideoPlayerHandler)
        ],debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
