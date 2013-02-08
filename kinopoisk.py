#!/usr/bin/python
# -*- coding: utf-8 -*-
import httplib,urllib,re
import urllib2
from lxml import html
from lxml import etree
import string
import time
import os
import sys
import traceback
import codecs
from optparse import OptionParser

from google.appengine.api import urlfetch

kinopoisk_version = "0.1.1"
mythtv_version = "0.25"
title = "The kinopoisk.ru Query"
author = "Alex Vasilyev"
usage_examples = ""

class KinopoiskResult:
    def __init__(self, title, description, cover):
        self.title = title;
        self.description = description;
        self.cover = cover;

    def get_title(self):
        return self.title

    def as_json(self):
        return '{"title": "%s", "description": "%s", "cover": "%s"}' % self.title, self.description, self.cover;

def comment_out(str):
    s = str
    try:
        s = unicode(str, "utf8")
    except:
        pass

    print("# %s" % (s,))

def debug_out(str):
    if VERBOSE:
        comment_out(str)

def response_out(str):
    if DUMP_RESPONSE:
        s = str
        try:
            s = unicode(str, "utf8")
        except:
            pass
        print(s)

def print_exception(str):
    for line in str.splitlines():
        comment_out(line)


def title_correction(title):
    try:
        regexp= re.compile(r'<.*?>')
        title = regexp.sub('',  title)
        return title
    except:
        return title
        

#Замена различных спецсимволов и тегов HTML на обычные символы, 
#возможно есть более правильное решение, но вроде и это работает.
def  normilize_string(processingstring):
    try:
        symbols_to_remove = {}
        for i in range (len(symbols_to_remove)):
            processingstring = string.replace(processingstring,  unicode(symbols_to_remove.items()[i][0],  'utf-8'), unicode(symbols_to_remove.items()[i][1],  'utf-8'))
        return processingstring
    except:
        return ''

def outXML(rootElm):
    outfile = sys.stdout
    handle = unicode(etree.tostring(rootElm, pretty_print=True, encoding='utf-8', xml_declaration=True), 'utf-8')
    outfile.writelines(handle)
    outfile.close()

#Получение HTML страницы
def get_page(address,  data=0,  title=''):
    if data == 0:
        address = u'http://s.kinopoisk.ru' + address+urllib.quote(title.encode('utf8'))
    else:
        address = u'http://www.kinopoisk.ru' + address+urllib.quote(title.encode('utf8'))
        
    result = urlfetch.fetch(url = address, headers = {
            'User-agent': 'Mozilla/5.0 (X11; U; Linux i686; ru; rv:1.9.0.14) Gecko/2009090216 Ubuntu/9.04 (jaunty) Firefox/3.0.14',
            "Accept":  "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
            "Accept-Language":  "ru,en-us;q=0.7,en;q=0.3",
            "Accept-Charset": "windows-1251,utf-8;q=0.7,*;q=0.7",
            "Keep-Alive": "300",
            "Connection":  "keep-alive"})
    return result.content

#Ищем обои
def search_fanart(uid):
    data = get_page("/level/12/film/"+uid, 1)
    doc = html.document_fromstring(data)
    result = []
        
    posterNodes = doc.xpath("//div/table[@class='fotos fotos2']/tr/*") 
    for poster in posterNodes:
        hrefTag = poster.xpath("a")
        if len(hrefTag):
            posterURL= hrefTag[0].attrib["href"]
            result.append("http://www.kinopoisk.ru" + posterURL)
    return result

#Ищем обложки
def search_poster(uid):
    data = get_page("/level/17/film/"+uid, 1)
    doc = html.document_fromstring(data)
    result = []
        
    posterNodes = doc.xpath("//div/table[@class='fotos']/tr/*") 
    for poster in posterNodes:

        hrefTag = poster.xpath("a")
        if len(hrefTag):
            posterURL= hrefTag[0].attrib["href"]
            result.append("http://www.kinopoisk.ru" + posterURL)
            
    return result
        
#Получаем названия фильмов похожие на наш фильм
def search_title(title):

    data = get_page("/index.php?first=no&kp_query=",  0, title)
    doc = html.document_fromstring(data)
    
    #Проверяем ту ли страницу (т.е. страницу с результатами поиска) мы получили
    regexp= re.compile(unicode("Скорее всего, вы ищете", "utf8"), re.DOTALL)
    result = regexp.search(data)
    if result == None:
        #Если не ту, то парсим страницу фильма на которую нас перенаправил кинопоиск
        titlestr = doc.xpath("//h1[@class='moviename-big']") [0].text.strip()
        idstr = doc.xpath("//link[@rel='canonical']") [0].attrib["href"].split("/")[-2]
        sys.stdout.write( u'%s:%s\n' % (idstr, normilize_string(titlestr)))
    else:
        titleNodes = doc.xpath("//div[@class='search_results' or @class='search_results search_results_last']/div[@class='element most_wanted' or @class='element']/div[@class='info']") 
        
        for titleNode in titleNodes:
            titleInfo = titleNode.xpath("p[@class='name']/a")
            sys.stdout.write( u'%s:%s\n' % (titleInfo[0].attrib["href"].split("/")[-4], normilize_string(titleInfo[0].text)))

#Ищем и отдаем метаданные фильма
def search_data(uid, rating_country):

    #def addMultiValues(parentNode, parentNodeName, dataNode, xpathTuple, nodeName, valueName,  attributesDict={}):
    def addMultiValues(dataNode, xpathTuple):
        result = ''
        temp_list = []
        for xpathString in xpathTuple:
            if len(dataNode) and len(dataNode.xpath(xpathString)):
                for node in dataNode.xpath(xpathString):
                    if node.text != "...":
                        temp_list.append(node.text)
        result = ",".join(temp_list)
        return result

    filmdata = {'title' : '',
            'countries' : '',
            'year' : '',
            'directors' : '',
            'cast' : '',
            'genre' : '',
            'user_rating' : '',
            'movie_rating' : '',
            'plot' : '',
#  'release_date' : '',
             'runtime' : '',
             'url' : '', 
             'coverart' : '',
             'fanart' : ''
            #'writers' : '',
        }
        
    data = get_page("/level/1/film/"+uid, 1)
    print (data)
    doc = html.document_fromstring(data)
        
    filmdata['title'] = doc.xpath("//h1[@class='moviename-big']") [0].text.strip()
        
    userRatingNodes = doc.xpath("//div[@id='block_rating']/div/div/a/span")
    if len(userRatingNodes):
        filmdata['user_rating'] = userRatingNodes[0].text

    infoNodes = doc.xpath("//table[@class='info']/*") 
    for infoNode in infoNodes:
        dataNodes =infoNode.xpath("td")  
        if dataNodes[0].text == u"год":
            filmdata['year'] = dataNodes[1].xpath("div/a") [0].text
        elif dataNodes[0].text == u"страна":
            filmdata['countries'] = addMultiValues(dataNodes[1],  ("a", "div/a"))
        elif dataNodes[0].text == u"режиссер":
            filmdata['directors'] = addMultiValues(dataNodes[1], ("a", "div/a"))
        elif dataNodes[0].text == u"жанр":
            filmdata['genre'] = addMultiValues(dataNodes[1], ("a", "div/a"))
        elif dataNodes[0].text == u"время":
            filmdata['runtime']  = dataNodes[1].text.split()[0]
        elif dataNodes[0].text == u"рейтинг MPAA":
            filmdata['movie_rating'] = dataNodes[1].xpath("a")[0].attrib["href"].split("/")[-2]
        
    actorNodes = doc.xpath("//td[@class='actor_list']/div")
    if len(actorNodes):
        filmdata['cast'] = addMultiValues(actorNodes[0], ("a", "span/a"))

    descNodes = doc.xpath("//div[@class='brand_words']")
    filmdata['plot'] = normilize_string(descNodes[0].text)
        
    posters = search_poster(uid)
    if len(posters):
        filmdata['coverart'] = posters[0]
        
    fanarts = search_fanart(uid)
    if len(fanarts):
        filmdata['fanart'] = fanarts[0]

    filmdata['url'] = "http://www.kinopoisk.ru/level/1/film/"+uid
    return KinopoiskResult(title, description, coverart)

#        print("""\
#            Title:%(title)s
#            Year:%(year)s
#            Director:%(directors)s
#            Plot:%(plot)s
#            UserRating:%(user_rating)s
#            Cast:%(cast)s
#            Genres:%(genre)s
#            Countries:%(countries)s
#            Runtime:%(runtime)s
#            MovieRating:%(movie_rating)s
#            Coverart:%(coverart)s
#            Fanart:%(fanart)s
#            URL:%(url)s
#    """ % filmdata)
