# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de Canal Onda Cádiz, emisión en web Livestream.com by DarioMO
# Version 0.1 (03.08.2016)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------

import os
import sys
import urllib
import urllib2
import re

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import time

import plugintools, requests
from resources.tools.resolvers import *
from resources.tools.media_analyzer import *
from __main__ import *
#from datetime import datetime

url1 = "https://livestream.com/Onda-Cadiz/directo"
url2 = "http://ondaluz.tv/bahia/"
url_radio = "http://195.55.74.207/adc/radio.mp3"
url_videos = "http://www.youtube.com/channel/UCpOz3CN6mDlxkE7-m5AS1aQ/playlists"
#regex_tube = "plugin://plugin.video.live.streamspro/?fanart=C%3a%5cUsers%5cusuario%5cAppData%5cRoaming%5cKodi%5caddons%5cplugin.video.live.streamspro%5cfanart.jpg&mode=53&name=Video%20Youtube%20&url=plugin%3a%2f%2fplugin.video.youtube%2fuser%2fREF-VIDEO%2f"
#regex_tube = "plugin://plugin.video.live.streamspro/?fanart=C%3a%5cUsers%5cusuario%5cAppData%5cRoaming%5cKodi%5caddons%5cplugin.video.live.streamspro%5cfanart.jpg&amp;mode=53&amp;name=Video%20Youtube%20&amp;url=plugin%3a%2f%2fplugin.video.youtube%2fuser%2fREF-VIDEO%2f"

def ondacadiz0(params):
	
	r = requests.get(url1)	
	data = r.content
	
	plugintools.add_item(action="",url="",title="[COLOR deepskyblue][B]Carnavales de Cadiz[/B][/COLOR][COLOR gold][I]      *** By LReylist ***[/I][/COLOR]",thumbnail="https://d16teuje7e44sv.cloudfront.net/spa/cities/spain/cadiz-medium.jpg",fanart="https://www.bungalowsclub.com/info/wp-content/uploads/2014/01/car4.jpg",folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail="https://d16teuje7e44sv.cloudfront.net/spa/cities/spain/cadiz-medium.jpg",fanart="https://www.bungalowsclub.com/info/wp-content/uploads/2014/01/car4.jpg", folder=False, isPlayable=False)

	link =  plugintools.find_single_match(data,'m3u8_url"(.*?)",').replace(':"' , '')

	plugintools.add_item(action="play",url=link,title="[COLOR orange][B]                                  ······Ver Onda Cádiz······[/COLOR][/B]",thumbnail="http://i.imgur.com/n9thmJD.png",fanart="https://www.bungalowsclub.com/info/wp-content/uploads/2014/01/car4.jpg",folder=False,isPlayable=True)

	r = requests.get(url2)	
	data = r.content
	
	link =  plugintools.find_single_match(data,'file: "(.*?)"')

	plugintools.add_item(action="play",url=link,title="[COLOR orange][B]                               ······Ver OndaLuz Cádiz······[/COLOR][/B]",thumbnail="https://pepecon.files.wordpress.com/2010/12/valla5.jpg",fanart="https://www.bungalowsclub.com/info/wp-content/uploads/2014/01/car4.jpg",folder=False,isPlayable=True)
	plugintools.add_item(action="play",url=url_radio,title="[COLOR lime][B]                             ······Oir Onda Cádiz Radio······[/COLOR][/B]",thumbnail="http://ocadizdigital.es/sites/default/files/_carnaval_banner/onda-cadiz-radio2.jpg",fanart="https://www.bungalowsclub.com/info/wp-content/uploads/2014/01/car4.jpg",folder=False,isPlayable=True)

	plugintools.add_item(action="videos_carnaval",url="",title="[COLOR red][B]                        ······Videoteca de Carnavales······[/COLOR][/B]",thumbnail="http://turyhoteles.com/wp-content/uploads/2016/01/carnaval-de-cadiz-Comparsas-chirigotas-Vidactiva-700x393.jpg",fanart="https://www.bungalowsclub.com/info/wp-content/uploads/2014/01/car4.jpg",folder=True,isPlayable=False)


def videos_carnaval(params):

	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": url_videos}
	r=requests.get(url_videos, headers=headers)
	data = r.content
	
	listas =  plugintools.find_multiple_matches(data,'channels-content-item(.*?)yt-lockup-notifications-container hid')
	
	for item in listas:
		#nomlista = plugintools.find_single_match(item,'ltr" title=(.*?)"').replace('"' , '')
		nomlista = plugintools.find_single_match(item,'ltr" title(.*?)"  aria').replace('="' , '')
		nomlista = nomlista.replace('"' , '')

		logo = plugintools.find_single_match(item,'src="(.*?)"')
		numvideos = plugintools.find_single_match(item,'<b>(.*?)</b>')
		reflista = plugintools.find_single_match(item,'amp;list=(.*?)"')
		
		titulo = "[COLOR olive]" + nomlista + "[I][COLOR chocolate]   (" + numvideos + " Videos)[/I][/COLOR]"
		
		plugintools.add_item(action="carga_carnavales",url=reflista,title=titulo,thumbnail="http://turyhoteles.com/wp-content/uploads/2016/01/carnaval-de-cadiz-Comparsas-chirigotas-Vidactiva-700x393.jpg",fanart="https://www.bungalowsclub.com/info/wp-content/uploads/2014/01/car4.jpg",folder=True,isPlayable=False)


		
def carga_carnavales(params):
	lista = "http://www.youtube.com/playlist?list=" + params.get("url")
	fanart = params.get("fanart")
	titulo = params.get("title")
	
	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', "Referer": lista}
	r=requests.get(lista, headers=headers)
	data = r.content

	plugintools.add_item(action="",url="",title=titulo,thumbnail="https://d16teuje7e44sv.cloudfront.net/spa/cities/spain/cadiz-medium.jpg",fanart="https://www.bungalowsclub.com/info/wp-content/uploads/2014/01/car4.jpg",folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail="https://d16teuje7e44sv.cloudfront.net/spa/cities/spain/cadiz-medium.jpg",fanart="https://www.bungalowsclub.com/info/wp-content/uploads/2014/01/car4.jpg", folder=False, isPlayable=False)

	videos = plugintools.find_multiple_matches(data, '<tr class="pl-video yt-uix-tile(.*?)pl-video-edit-options')
			
	for item in videos:
		video = plugintools.find_single_match(item, '//i.ytimg.com/vi/(.*?)/')
		titu_vid = plugintools.find_single_match(item, 'title="(.*?)"')
		logo_vid = plugintools.find_single_match(item, 'data-thumb="(.*?)"')
		duracion = plugintools.find_single_match(item, 'minutos">(.*?)<')

		titu = titu_vid + "     [I][COLOR yellow](" + duracion + ")[/I]"
		#plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + titu + '[/COLOR]', url = url_montada , thumbnail = logo_vid , fanart = fanart , folder = False , isPlayable = True)
		plugintools.add_item( action = "lanza_video_tube" , title = '[COLOR white]' + titu + '[/COLOR]', url = video , thumbnail = logo_vid , fanart = fanart , folder = False , isPlayable = False)


def lanza_video_tube(params):		
	url = params.get("url")

	xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id='+url+')')




		
		




