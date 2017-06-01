# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Linker Inkapelis.com para PalcoTV
# Version 0.2 (02/09/2016)
# Autor By Aquilesserr ___ *** ___ aquilesserr@gmail.com
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

thumbnail = "https://www.cubbyusercontent.com/pl/Inkapelis-logo.png/_bfb1645df4044af8a52b5fdc6760bf41"
fanart = "https://www.cubbyusercontent.com/pl/Inkapelis_fanart.jpg/_64f71a456c714ad5a66c67cf6ed2f502"

sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR seagreen]";ec3 = "[/COLOR]"
sc4 = "[COLOR red]";ec4 = "[/COLOR]"
sc5 = "[COLOR yellowgreen]";ec5 = "[/COLOR]"
version = " [0.2]"

web = "http://www.inkapelis.com/"
referer = "http://www.inkapelis.com/"

def inkapelis_linker0(params):
    plugintools.log("[%s %s] Linker Inkapelis %s" % (addonName, addonVersion, repr(params)))
   
    ################## Params Library ####################
    url_list=[];option_list=[];source=params.get("extra")
    ######################################################
    url = params.get("url")
    r = requests.get(url)
    data = r.content

    ####################################### Control for Linker ##########################################
    if source == "linker":
        plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker Inkapelis"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
        fondo = plugintools.find_single_match(data,'style="background-image: url\(([^)]+)\)').strip()
        if fondo =="": fondo = fanart 
        logo = plugintools.find_single_match(data,'<div class="col-xs-2 poster"> <img src="([^"]+)"')
        if logo =="": logo = thumbnail 
        bloq_info = plugintools.find_single_match(data,'<h2>Sinopsis</h2>(.*?)<span class="aa">Reparto</span>') 
        title = plugintools.find_single_match(bloq_info,'<span class="aa">Título</span> <span class="ab">([^<]+)</span>').upper().strip()
        votos = plugintools.find_single_match(bloq_info,'<span class="aa">Calificación</span> <span class="ab">([^<]+)</span>').strip()
        if votos =="": punt_imdb = 'N/D'
        year = plugintools.find_single_match(bloq_info,'<span class="aa">Año de lanzamiento</span> <span class="ab">([^<]+)</span>').strip()
        if year =="": year = 'N/D'
        durac = plugintools.find_single_match(bloq_info,'<span class="aa">Duración</span> <span class="ab">([^<]+)</span>').strip()
        if durac =="": durac = 'N/D'
        genrfull = plugintools.find_multiple_matches(bloq_info,'rel="category tag">([^<]+)</a>')
        genr = inkapelis_genr(genrfull)
        sinopsis = plugintools.find_single_match(bloq_info,'<p class="trasnparente">(.*?)</p>').strip().replace('<a href=','').replace('</strong>','').replace('<strong>','')
        datamovie = {
        'rating': sc3+'[B]Votos: [/B]'+ec3+sc+str(votos)+', '+ec,
        'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
        'year': sc3+'[B]Año: [/B]'+ec3+sc+str(year)+', '+ec,
        'duration': sc3+'[B]Duración: [/B]'+ec3+sc+str(durac)+'[CR]'+ec,
        'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
        datamovie["plot"]=datamovie["rating"]+datamovie["genre"]+datamovie["year"]+datamovie["duration"]+datamovie["sinopsis"]
        plugintools.addPeli(action="",url="",title=sc5+"[B]"+title+"[/B]"+ec5,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    #####################################################################################################
  
    lang_embed1 = plugintools.find_single_match(data,'<a href="#embed1" data-toggle="tab">(.*?)</a>').replace('Español','ESP').replace('Latino','LAT').replace('Subtitulado','SUB').replace('Original','V.O.').strip()
    if lang_embed1 !="":
    	quality_embed1 = plugintools.find_single_match(data,'id="embed1"><div class="calishow">(.*?)</div>')
    	url_embed1 = plugintools.find_single_match(data,'id="embed1">.*?src="([^"]+)"')
        if 'ok.ru' in url_embed1: url_embed1 = 'http:'+url_embed1
    	server1 = video_analyzer(url_embed1)
        ####################################### Control for Linker ##########################################
        if source == "linker":
            titlefull1 = sc+server1.title()+ec+" "+sc2+' [I]['+lang_embed1+'][/I]'+ec2+" "+sc+" Video: "+ec+sc5+quality_embed1+ec5
            plugintools.addPeli(action=server1,url=url_embed1,title=titlefull1,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)
        #####################################################################################################
        ####################################### Control for Library #########################################
        elif source == "library":
    	   titlefull1 = '[COLOR white]'+server1.title()+' '+'[/COLOR][COLOR lightyellow][I]['+lang_embed1.strip()+'] [/COLOR][COLOR lightblue]['+quality_embed1.replace(" Real ", "-")+'] [/COLOR][COLOR gold][Inkapelis][/I][/COLOR]'
           url_list.append(url_embed1);option_list.append(titlefull1)  
        ####################################################################################################  
    else: pass
    
    lang_embed2 = plugintools.find_single_match(data,'<a href="#embed2" data-toggle="tab">(.*?)</a>').replace('Español','ESP').replace('Latino','LAT').replace('Subtítulo','SUB -').replace('Original','V.O.').replace('Subtitulado','SUB').strip()
    if lang_embed2 !="":
    	quality_embed2 = plugintools.find_single_match(data,'id="embed2"><div class="calishow">(.*?)</div>')
    	url_embed2 = plugintools.find_single_match(data,'id="embed2">.*?src="([^"]+)"')
        if 'ok.ru' in url_embed2: url_embed2 = 'http:'+url_embed2
    	server2 = video_analyzer(url_embed2)
        ####################################### Control for Linker ##########################################
        if source == "linker":
            titlefull2 = sc+server2.title()+ec+" "+sc2+' [I]['+lang_embed2+'][/I]'+ec2+" "+sc+" Video: "+ec+sc5+quality_embed2+ec5
            plugintools.addPeli(action=server2,url=url_embed2,title=titlefull2,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)
        #####################################################################################################
        ####################################### Control for Library #########################################
        elif source == "library":
    	   titlefull2 = '[COLOR white]'+server2.title()+' '+'[/COLOR][COLOR lightyellow][I]['+lang_embed2.strip()+'] [/COLOR][COLOR lightblue]['+quality_embed2.replace(" Real ", "-")+'] [/COLOR][COLOR gold][Inkapelis][/I][/COLOR]'
           url_list.append(url_embed2);option_list.append(titlefull2)  
        #####################################################################################################
    else: pass
    
    lang_embed3 = plugintools.find_single_match(data,'<a href="#embed3" data-toggle="tab">(.*?)</a>').replace('Español','ESP').replace('Latino','LAT').replace('Subtítulo','SUB -').replace('Subtitulado','SUB').replace('Original','V.O.').strip()
    if lang_embed3 !="":
        quality_embed3 = plugintools.find_single_match(data,'id="embed3"><div class="calishow">(.*?)</div>')
        url_embed3 = plugintools.find_single_match(data,'id="embed3">.*?src="([^"]+)"')
        if 'ok.ru' in url_embed3: url_embed3 = 'http:'+url_embed3
        server3 = video_analyzer(url_embed3)
        ####################################### Control for Linker ##########################################
        if source == "linker":
            titlefull3 = sc+server3.title()+ec+" "+sc2+' [I]['+lang_embed3+'][/I]'+ec2+" "+sc+" Video: "+ec+sc5+quality_embed3+ec5
            plugintools.addPeli(action=server3,url=url_embed3,title=titlefull3,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)
        #####################################################################################################
        ####################################### Control for Library #########################################
        elif source == "library":
            titlefull3 = '[COLOR white]'+server3.title()+' '+'[/COLOR][COLOR lightyellow][I]['+lang_embed3.strip()+'] [/COLOR][COLOR lightblue]['+quality_embed3.replace(" Real ", "-")+'] [/COLOR][COLOR gold][Inkapelis][/I][/COLOR]'
            url_list.append(url_embed3);option_list.append(titlefull3)
        #####################################################################################################
    else: pass
    
    lang_embed4 = plugintools.find_single_match(data,'<a href="#embed4" data-toggle="tab">(.*?)</a>').replace('Español','ESP').replace('Latino','LAT').replace('Subtítulo','SUB -').replace('Subtitulado','SUB').replace('Original','V.O.').strip()
    if lang_embed4 !="":
        quality_embed4 = plugintools.find_single_match(data,'id="embed4"><div class="calishow">(.*?)</div>')
        url_embed4 = plugintools.find_single_match(data,'id="embed4">.*?src="([^"]+)"')
        if 'ok.ru' in url_embed4: url_embed4 = 'http:'+url_embed4
        server4 = video_analyzer(url_embed4)
        ####################################### Control for Linker ##########################################
        if source == "linker":
            titlefull4 = sc+server4.title()+ec+" "+sc2+' [I]['+lang_embed4+'][/I]'+ec2+" "+sc+" Video: "+ec+sc5+quality_embed4+ec5
            plugintools.addPeli(action=server4,url=url_embed4,title=titlefull4,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)
        #####################################################################################################
        ####################################### Control for Library #########################################
        elif source == "library":
            titlefull4 = '[COLOR white]'+server4.title()+' '+'[/COLOR][COLOR lightyellow][I]['+lang_embed4.strip()+'] [/COLOR][COLOR lightblue]['+quality_embed4.replace(" Real ", "-")+'] [/COLOR][COLOR gold][Inkapelis][/I][/COLOR]'
            url_list.append(url_embed4);option_list.append(titlefull4)
        #####################################################################################################
    else: pass

    bloq_server = plugintools.find_single_match(data,'class="dlmt">Opciones Para Ver Online</h2>(.*?)class="dlmt">Opciones Para Descargar</h2>')
    serverfull = plugintools.find_multiple_matches(bloq_server,'<tr><td>(.*?)</tr>')

    for item in serverfull:
    	lang = plugintools.find_single_match(item,'</span></td><td>([^<]+)</td><td>').replace('Español','ESP').replace('Latino','LAT').replace('Subtítulo','SUB -').replace('Subtitulado','SUB').replace('Original','V.O.').strip()
    	quality = plugintools.find_single_match(item,'</span></td><td>.*?</td><td>([^<]+)</td>').strip()
        url_vid = plugintools.find_single_match(item,'<a href="([^"]+)"')
        if 'ok.ru' in url_vid: url_vid = 'http:'+url_vid
        server = video_analyzer(url_vid)
        ####################################### Control for Linker ##########################################
        if source == "linker":
            titlefull = sc+server.title()+ec+" "+sc2+" [I]["+lang+"][/I] "+ec2+" "+sc+"Video: "+ec+sc5+quality+ec5
            plugintools.addPeli(action=server,url=url_vid,title=titlefull,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)
        #####################################################################################################
        ####################################### Control for Library #########################################
        elif source == "library":
            titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+lang.strip()+'] [/COLOR][COLOR lightblue]['+quality.replace(" Real ", "-")+'] [/COLOR][COLOR gold][Inkapelis][/I][/COLOR]'
            url_list.append(url_vid);option_list.append(titlefull)
        #####################################################################################################       

    if source == "library": return option_list,url_list
    
################################################# Tools for Linker ##############################################

def inkapelis_genr(genrfull):
    
    if len(genrfull) ==5: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]+', '+genrfull[4]
    elif len(genrfull) ==4: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]
    elif len(genrfull) ==3: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]
    elif len(genrfull) ==2: genrfull = genrfull[0]+', '+genrfull[1]
    elif len(genrfull) ==1: genrfull = genrfull[0]
    elif len(genrfull) >5: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]+', '+genrfull[4]
    else: genrfull = 'N/D' 
    return genrfull

######################################### @ By Aquilesserr PalcoTv Team #########################################  
    