# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Linker Pelisadicto.com para PalcoTV
# Version 0.3 (02/09/2016)
# Kodi Add-on by Juarrox (juarrox@gmail.com)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Librerías Plugintools por Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re
import shutil
import zipfile

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools, requests
from resources.tools.resolvers import *
from resources.tools.media_analyzer import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

thumbnail = 'https://www.cubbyusercontent.com/pl/Pelisadicto_logo.png/_06e2a54361bb4a0bb673918d692ce6fc'
fanart = 'https://www.cubbyusercontent.com/pl/Pelisadicto_fanart.jpg/_62590dc339114905bebbceec8999531a'

sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR seagreen]";ec3 = "[/COLOR]"
sc4 = "[COLOR red]";ec4 = "[/COLOR]"
sc5 = "[COLOR yellowgreen]";ec5 = "[/COLOR]"
version = " [0.2]"

def pelisadicto_linker0(params):
    plugintools.log("[%s %s] linker Pelisadicto %s" % (addonName, addonVersion, repr(params))) 

    ##################### Params Library ###########################
    url_list=[];option_list=[];source=params.get("extra")
    ################################################################
    url = params.get("url")
    r = requests.get(url)
    data = r.content

    ####################################### Control for Linker ##########################################
    if source == "linker":
        plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker Pelisadicto"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
        logo = 'http://pelisadicto.com'+ plugintools.find_single_match(data,'<img style="width.*?src="([^"]+)"')
        if logo =="": logo = thumbnail
        title = plugintools.find_single_match(data,'<meta property="og:title" content="(.*?)\(').strip()
        if title =="": title = plugintools.find_single_match(data,'<meta property="og:title" content="(.*?)"')
        year = plugintools.find_single_match(data,'<meta property="og:title" content=".*?\((.*?)\)')
        bloq_genr = plugintools.find_single_match(data,'<p>Genero(.*?)</p>')
        genrfull = plugintools.find_multiple_matches(bloq_genr,'title=".*?">(.*?)<')
        genr = pelisadicto_genr(genrfull)
        sinopsis = plugintools.find_single_match(data,'<p>(.*?)</p>').strip().replace('\n','')
        datamovie = {
        'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
        'year': sc3+'[B]Año: [/B]'+ec3+sc+str(year)+'[CR]'+ec,
        'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
        datamovie["plot"]=datamovie["genre"]+datamovie["year"]+datamovie["sinopsis"]
        plugintools.addPeli(action="",url="",title=sc5+"[B]"+title+"[/B]"+ec5,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)  
    #####################################################################################################

    bloq_link = plugintools.find_single_match(data,'<tbody>(.*?)</table>')
    link = plugintools.find_multiple_matches(bloq_link,'<tr>(.*?)</tr>')
    for item in link:
        lang = plugintools.find_single_match(item,'<td><img src="([^"]+)"')
        if '1.png' in lang: lang = sc2+'[I][ESP][/I]'+ec2
        if '2.png' in lang: lang = sc2+'[I][LAT][/I]'+ec2
        if '3.png' in lang: lang = sc2+'[I][ENG-SUB][/I]'+ec2
        if '4.png' in lang: lang = sc2+'[I][ENG][/I]'+ec2
        quality = plugintools.find_single_match(item,'<td><img src=".*?</td>\s+<td>(.*?)</td>')
        url_server = plugintools.find_single_match(item,' href="([^"]+)"')
        server = video_analyzer(url_server)
        ####################################### Control for Linker ##########################################
        if source == "linker":
            titlefull = sc+server.title()+ec+" "+lang+"  "+sc+"Video: "+ec+sc5+quality+ec5
            plugintools.addPeli(action=server,url=url_server,title=titlefull,info_labels=datamovie,thumbnail=logo,fanart=fanart,folder=False,isPlayable=True)
        #####################################################################################################
        ####################################### Control for Library #########################################
        elif source == "library":
            plugintools.log("server= "+server);plugintools.log("lang= "+lang);plugintools.log("quality= "+quality)
            titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR]'+lang.replace("palegreen", "lightyellow").strip()+' [COLOR lightgreen][I]['+quality+'] [/COLOR][COLOR gold][HDFull][/I][/COLOR]'
            plugintools.log("titlefull= "+titlefull);plugintools.log("url_server= "+url_server)
            url_list.append(url_server);option_list.append(titlefull)
        #####################################################################################################

    if params.get("extra") == "library": return option_list,url_list
        
################################################# Tools for Linker ##############################################

def pelisadicto_genr(genrfull):
    try:
        if len(genrfull) ==5: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]+', '+genrfull[4]
        elif len(genrfull) ==4: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]
        elif len(genrfull) ==3: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]
        elif len(genrfull) ==2: genrfull = genrfull[0]+', '+genrfull[1]
        elif len(genrfull) ==1: genrfull = genrfull[0]
        return genrfull
    except: pass

############################################# @ By PalcoTv Team #################################################
