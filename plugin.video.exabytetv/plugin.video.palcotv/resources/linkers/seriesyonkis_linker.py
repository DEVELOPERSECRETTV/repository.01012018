# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Linker de SeriesYonkis para PalcoTV
# Version 0.2 (01.04.2016)
# Kodi Add-on by Juarrox (juarrox@gmail.com)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a las librerías de pelisalacarta de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import re,urllib,urllib2,sys

import plugintools, requests
from resources.tools.resolvers import *
from resources.tools.media_analyzer import *
from resources.tools.bers_sy import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

thumbnail = 'https://www.cubbyusercontent.com/pl/seriesyonkis_logo_palco.png/_f2f9d376137041309a4260836e98f19c'
fanart = 'https://www.cubbyusercontent.com/pl/seriesyonkis_fondo_palco.jpg/_26e214e2bd8244de92f7787c2ac2ee50'

sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR seagreen]";ec3 = "[/COLOR]"
sc4 = "[COLOR red]";ec4 = "[/COLOR]"
sc5 = "[COLOR yellowgreen]";ec5 = "[/COLOR]"
version = " [0.2]"

referer = 'http://www.seriesyonkis.sx/'

def serieyonkis_linker0(params):
    plugintools.log('[%s %s] Linker SeriesYonkis %s' % (addonName, addonVersion, repr(params)))
    
    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker SeriesYonkis"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

    bers_sy_on = plugintools.get_setting("bers_sy_on")
    bers_sy_level = plugintools.get_setting("bers_sy_level")
    plugintools.log("bers_sy_on= "+bers_sy_on)
    plugintools.log("bers_sy_level= "+bers_sy_level)
	
    if bers_sy_on == "true" and bers_sy_level == "1":  # Control para ejecutar el BERS para toda la serie
        bers_sy0(params)
    else:    
        datamovie={}
        if params.get("plot") != "":
                datamovie["Plot"]=params.get("plot")  # Cargamos sinopsis de la serie... (si existe)
        else:
                datamovie["Plot"]="."
       
        url = params.get("url")
        request_headers=[]
        request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
        request_headers.append(["Referer", referer])
        data,response_headers = plugintools.read_body_and_headers(url,headers=request_headers)

        title = plugintools.find_single_match(data,'<h1 class="underline" title="(.*?)\(').strip()
        year = plugintools.find_single_match(data,'<h1 class="underline" title=".*?\((.*?)\)').strip()
        if year =="": year = 'N/D'
        punt = plugintools.find_single_match(data,'<div class="rating">\s+<p>(.*?)</p>').strip().replace('\n','').replace('\t','')
        if punt =="": punt = 'N/D'
        n_temp = plugintools.find_single_match(data,'id="votes">\s+<p>\s+([0-9]+).*?<span id="votes_value">').strip().replace('\n','').replace('\t','').replace('|','')
        if n_temp =="": n_temp = 'N/D'
        sinopsis = plugintools.find_single_match(data,'<p style=";">(.*?)</p>').strip()
        if sinopsis =="": sinopsis = 'N/D'
        logo = plugintools.find_single_match(data, '<img src="([^"]+)"')
        datamovie = {
        'season': sc3+'[B]Temporadas Disponibles: [/B]'+ec3+sc+str(n_temp)+', '+ec,
        'rating': sc3+'[B]Puntuación: [/B]'+ec3+sc+str(punt)+', '+ec,
        'year': sc3+'[B]Año: [/B]'+ec3+sc+str(year)+'[CR]'+ec,
        'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
    
        datamovie["plot"]=datamovie["season"]+datamovie["rating"]+datamovie["year"]+datamovie["sinopsis"]

        plugintools.add_item(action="",url="",title=sc5+"[B]"+title+"[/B]"+ec5,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)  
        
        bloq_temp = plugintools.find_single_match(data,'<div id="section-content">(.*?)</ul>')
        temps = plugintools.find_multiple_matches(bloq_temp,'<h3 class="season"(.*?)</li>')
        for item in temps:
            name_temp = plugintools.find_single_match(item,'<strong class="season_title">(.*?)</strong>').strip()
            plugintools.addPeli(action="",url="",title=sc2+'-- '+name_temp+' --'+ec2,info_labels=datamovie,thumbnail=logo,fanart=fanart,folder=False,isPlayable=False)
            capis = plugintools.find_multiple_matches(item,'<td class="episode-title">(.*?)</td>')
            for entri in capis:
                url_cap = plugintools.find_single_match(entri,'href="([^"]+)')
                url_cap = 'http://www.seriesyonkis.sx'+url_cap
                num_cap = plugintools.find_single_match(entri,'<strong>(.*?)</strong>')
                num_cap = num_cap.strip()
                title_cap = plugintools.find_single_match(entri,'</strong>(.*?)</a>')
                title_cap = title_cap.strip()
                title_capi = sc+num_cap+title_cap+ec.strip()
                title_fixed = num_cap + title_cap
                title_fixed = title_fixed.strip()
                plugintools.addPeli(action="enlaces_capi_linker",title=title_capi,url=url_cap,info_labels=datamovie,thumbnail=logo,fanart=fanart,folder=True,extra=title_fixed,isPlayable=False)
        
def enlaces_capi_linker(params):
    plugintools.log('[%s %s] Linker SeriesYonkis %s' % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker SeriesYonkis"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

    datamovie = {}
    datamovie["Plot"] = params.get("plot")

    url = params.get("url")
    title_fixed = params.get("extra")
    referer = 'http://www.seriesyonkis.sx/'
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer]) 

    data,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)   
    
    matches = plugintools.find_single_match(data,'<h2 class="header-subtitle veronline">(.*?)</table>')
    match_veronline = plugintools.find_single_match(matches, '<tbody>(.*?)</tbody>')
    match_links = plugintools.find_multiple_matches(match_veronline, '<tr>(.*?)</tr>')
    for entry in match_links:
        title_url = plugintools.find_single_match(entry,'title="([^"]+)')
        page_url = plugintools.find_single_match(entry,'<a href="([^"]+)')
        name_server = plugintools.find_single_match(entry,'watch via([^"]+)')
        idioma_capi = plugintools.find_single_match(entry,'<span class="flags(.*?)</span></td>')
        idioma_capi_fixed = idioma_capi.split(">")

        if len(idioma_capi_fixed) >= 2: idioma_capi = idioma_capi_fixed[1]
        if idioma_capi == "English": idioma_capi = ' [ENG]'
        elif idioma_capi == "english": idioma_capi = ' [ENG]'            
        elif idioma_capi == "Español": idioma_capi = ' [ESP]'
        elif idioma_capi == "Latino": idioma_capi = ' [LAT]'
        elif idioma_capi.find("English-Spanish SUBS") >= 0: idioma_capi = ' [VOSE]'
        elif idioma_capi.find("Japanese-Spanish SUBS") >= 0: idioma_capi = ' [VOSE]'
        else: idioma_capi = " [N/D]"
                     
        plot = datamovie["Plot"]
        source_web="seriesyonkis"
        bers_sy_on = plugintools.get_setting("bers_sy_on")  # Control para activar BERS para el capítulo
        page_url = 'http://www.seriesyonkis.sx'+page_url
        server = video_analyzer(name_server)
        img_server = plugintools.find_single_match(entry,'<img height="35" src="([^"]+)"')
        if img_server =="":
            img_server = thumbnail
        title = sc+title_fixed+ec+sc2+' [I]'+idioma_capi+ec2+sc5+'[/I]  [I]['+server+'][/I]'+ec5

        plugintools.add_item(action="getlink_linker",title=title,url=page_url,thumbnail=img_server,info_labels=datamovie,fanart=fanart,folder=False,isPlayable=True)
        if bers_sy_on == 1:  # Control para ejecutar BERS a nivel de capítulo
                bers_sy1(plot, title_fixed, title, title_serie, page_url, thumbnail, fanart, source_web)
       
def getlink_linker(params):
    plugintools.log('[%s %s] Linker SeriesYonkis %s' % (addonName, addonVersion, repr(params)))  

    page_url = params.get("url")

    referer = 'http://www.seriesyonkis.sx/'
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])    
    data,response_headers = plugintools.read_body_and_headers(page_url, headers=request_headers)   
    match = plugintools.find_single_match(data,'<table class="episodes full-width">(.*?)</table>')
    url_final = plugintools.find_single_match(match,'<a class="link p2" href="([^"]+)')
    params["url"]=url_final
    resolvers = server_analyzer(params)
    
############################################# @ By PalcoTv Team #################################################