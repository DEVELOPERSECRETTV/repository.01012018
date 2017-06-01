# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Linker PeliculasDK para PalcoTV
# Version 0.1 (02.09.2016)
# Autor By Aquilesserr ___ *** ___ aquilesserr@gmail.com
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)  

import os
import sys
import urllib
import urllib2
import re

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools, requests
from resources.tools.resolvers import *
from resources.tools.media_analyzer import *

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

art = addonPath + "/art/"
temp = xbmc.translatePath(os.path.join('special://home/userdata/playlists/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/userdata/playlists', ''))

thumbnail = 'https://www.cubbyusercontent.com/pl/PeliculasDK_logo.PalcoTV.png/_396dd08b3f04465ab671497358bd66f4'
fanart = 'https://www.cubbyusercontent.com/pl/PeliculasDK_fondo.PalcoTV.jpg/_b18939e100044e74816eff7196078c30'

sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR seagreen]";ec3 = "[/COLOR]"
sc4 = "[COLOR red]";ec4 = "[/COLOR]"
sc5 = "[COLOR yellowgreen]";ec5 = "[/COLOR]"
version = " [0.1]"

web = "http://www.peliculasdk.com/"
ref = "http://www.peliculasdk.com/"

def peliculasdk_linker0(params):
    plugintools.log("[%s %s] Linker PeliculasDK  %s " % (addonName, addonVersion, repr(params)))

    ################## Params Library ####################
    url_list=[];option_list=[];source=params.get("extra")
    ######################################################
    url = params.get("url")
    r = requests.get(url)
    data = r.content
    print data
    ####################################### Control for Linker ##########################################
    if source == "linker":
        plugintools.add_item(action="",url="",title="[COLOR lightblue][B]linker PeliculasDK[/B]"+version+"[/COLOR][COLOR red][I] *** By Aquilesserr/PalcoTV Team ***[/I][/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
        poster = plugintools.find_single_match(data,'<div class="karatula">.*?src="(.*?)"')
        genrfull = plugintools.find_multiple_matches(data,'rel="category tag">(.*?)</a>')
        genr = peliculasdk_genr(genrfull)
        title = plugintools.find_single_match(data,'<a><img border="0" src=".*?></a>([^<]+)</h3>').upper().replace('&#8217;','').replace('&#8211;','').replace('&#8220;','"').replace('&#8221;','"') 

        ####################################### Analizando Cine X ###########################################
        if title =="":
            title = plugintools.find_single_match(data,'<td valign="top"><div class="caja_cont"><h3>(.*?)</h3>').upper().replace('&#8217;','').replace('&#8211;','').replace('&#8220;','"').replace('&#8221;','"') 
            calidad='Adultos';audio = 'Cine X';genr = 'Adultos'
        #####################################################################################################

        rating = plugintools.find_single_match(data,'Calificación IMDb: <span>(.*?)\n').replace('</B>','')
        if rating =="": rating = 'N/D'
        duration = plugintools.find_single_match(data,'Duración: <span>([^<]+)</span>')
        if duration =="": duration = 'N/D'
        year = plugintools.find_single_match(data,'Estreno: <span>([^<]+)</span>')
        if year =="": year = 'N/D'
        country = plugintools.find_single_match(data,'País: <span>([^<]+)</span>')
        if country =="": country = 'N/D'
        sinopsis = plugintools.find_single_match(data,'<span class="clms">Sinopsis: </span>(.*?)</div>').strip()
        if sinopsis =="":
            sinopsis = plugintools.find_single_match(data,'<div class="sinopsis">(.*?)</div>').strip()
        datamovie = {
        'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
        'duration': sc3+'[B]Duración: [/B]'+ec3+sc+str(duration)+', '+ec,
        'rating': sc3+'[B]Calificación: [/B]'+ec3+sc+str(rating)+', '+ec,
        'year': sc3+'[B]Año: [/B]'+ec3+sc+str(year)+', '+ec,
        'country': sc3+'[B]País: [/B]'+ec3+sc+str(country)+'[CR]'+ec,
        'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}    
        datamovie["plot"]=datamovie["genre"]+datamovie["duration"]+datamovie["rating"]+datamovie["year"]+datamovie["country"]+datamovie["sinopsis"]    
        plugintools.add_item(action="",url="",title=sc5+"[B]"+title+"[/B]"+ec5,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
        #####################################################################################################

    bloque_link = plugintools.find_single_match(data,'<div id="verpelicula">(.*?)<div id="mreporta">')
    if bloque_link =="":
        bloque_link = plugintools.find_single_match(data,'<div id="verpelicula">(.*?)<center><script type="text/javascript">')
    name_server = plugintools.find_multiple_matches(bloque_link,'<script>(.*?)\(\"(.*?)\"')
    audio = plugintools.find_single_match(data,'<li><a href="#tab1"><span class="re">.*?<span class="(.*?)"')
    audio = audio.replace('la','Latino').replace('su','Subtitulado').replace('es','Español')
    if audio =="": audio = 'N/D' 
    calidad = plugintools.find_single_match(data,'<li><a href="#tab1"><span class="re">.*?<span class=".*?".*?<span class="c">(.*?)</span>')  
    if calidad =="":calidad = 'N/D'
    
    for item in name_server:
        #plugintools.log("Nombre Servidor= "+str(item))
        server = item[0]
        id = item[1]

        ####################################### Control for Linker ##########################################
        if source == "linker":
            titlefull = sc+"[I]Ver en: "+ server.title()+'[/I] '+ec+sc2+'[I]['+str(audio)+" - "+str(calidad)+"][/I]"+ec2
            if ("allmy") in server:
                linkpeli = 'https://allmyvideos.net/'+item[1]
                plugintools.addPeli(action="allmyvideos",title=titlefull,url=linkpeli,info_labels=datamovie,thumbnail=poster,fanart=fanart,folder=False,isPlayable=True)
            if ("flash") in server:
                linkpeli = '"http://www.flashx.tv/'+item[1]+'.html'  
                plugintools.addPeli(action="flash",title=titlefull,url=linkpeli,info_labels=datamovie,thumbnail=poster,fanart=fanart,folder=False,isPlayable=True)
            if ("gamo") in server:
                linkpeli = 'http://www.gamovideo.com/'+item[1]   
                plugintools.addPeli(action="gamovideo",title=titlefull,url=linkpeli,info_labels=datamovie,thumbnail=poster,fanart=fanart,folder=False,isPlayable=True)
            if ("netu") in server:
                linkpeli = 'http://waaw.tv/watch_video.php?v='+item[1] 
                plugintools.addPeli(action="netu",title=titlefull,url=linkpeli,info_labels=datamovie,thumbnail=poster,fanart=fanart,folder=False,isPlayable=True)
            if ("okru") in server:
                linkpeli = 'http://ok.ru/videoembed/'+item[1]        
                plugintools.addPeli(action="okru",title=titlefull,url=linkpeli,info_labels=datamovie,thumbnail=poster,fanart=fanart,folder=False,isPlayable=True)
            if ("open") in server:
                linkpeli = 'https://openload.co/f/'+item[1]+'/'   
                plugintools.addPeli(action="openload",title=titlefull,url=linkpeli,info_labels=datamovie,thumbnail=poster,fanart=fanart,folder=False,isPlayable=True)
            if ("powvideo") in server:
                linkpeli = 'http://powvideo.net/'+item[1]    
                plugintools.addPeli(action="powvideo",title=titlefull,url=linkpeli,info_labels=datamovie,thumbnail=poster,fanart=fanart,folder=False,isPlayable=True)
            if ("streamin") in server:
                linkpeli = 'http://streamin.to/'+item[1] 
                plugintools.addPeli(action="streaminto",title=titlefull,url=linkpeli,info_labels=datamovie,thumbnail=poster,fanart=fanart,folder=False,isPlayable=True)
            if ("videomega") in server:
                linkpeli = 'http://videomega.tv/?ref='+item[1]   
                plugintools.addPeli(action="videomega",title=titlefull,url=linkpeli,info_labels=datamovie,thumbnail=poster,fanart=fanart,folder=False,isPlayable=True)
        #####################################################################################################
        ####################################### Control for Library #########################################
        elif source == "library":
            titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+audio+'] [/COLOR][COLOR lightblue]['+calidad+'] [/COLOR][COLOR gold][Oranline][/I][/COLOR]'        
            if ("allmy") in server:
                linkpeli = 'https://allmyvideos.net/'+item[1]  
                titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+str(audio)+'] [/COLOR][COLOR lightblue]['+str(calidad)+'] [/COLOR][COLOR gold][HDFull][/I][/COLOR]'
                url_list.append(linkpeli);option_list.append(titlefull)
            if ("flash") in server:
                linkpeli = '"http://www.flashx.tv/'+item[1]+'.html'  
                titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+str(audio)+'] [/COLOR][COLOR lightblue]['+str(calidad)+'] [/COLOR][COLOR gold][HDFull][/I][/COLOR]'
                url_list.append(linkpeli);option_list.append(titlefull)
            if ("gamo") in server:
                linkpeli = 'http://www.gamovideo.com/'+item[1]   
                titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+str(audio)+'] [/COLOR][COLOR lightblue]['+str(calidad)+'] [/COLOR][COLOR gold][HDFull][/I][/COLOR]'
                url_list.append(linkpeli);option_list.append(titlefull)
            if ("netu") in server:
                linkpeli = 'http://waaw.tv/watch_video.php?v='+item[1] 
                titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+str(audio)+'] [/COLOR][COLOR lightblue]['+str(calidad)+'] [/COLOR][COLOR gold][HDFull][/I][/COLOR]'
                url_list.append(linkpeli);option_list.append(titlefull)
            if ("okru") in server:
                linkpeli = 'http://ok.ru/videoembed/'+item[1]        
                titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+str(audio)+'] [/COLOR][COLOR lightblue]['+str(calidad)+'] [/COLOR][COLOR gold][HDFull][/I][/COLOR]'
                url_list.append(linkpeli);option_list.append(titlefull)
            if ("open") in server:
                linkpeli = 'https://openload.co/f/'+item[1]+'/'   
                titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+str(audio)+'] [/COLOR][COLOR lightblue]['+str(calidad)+'] [/COLOR][COLOR gold][HDFull][/I][/COLOR]'
                url_list.append(linkpeli);option_list.append(titlefull)
            if ("powvideo") in server:
                linkpeli = 'http://powvideo.net/'+item[1]    
                titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+str(audio)+'] [/COLOR][COLOR lightblue]['+str(calidad)+'] [/COLOR][COLOR gold][HDFull][/I][/COLOR]'
                url_list.append(linkpeli);option_list.append(titlefull)
            if ("streamin") in server:
                linkpeli = 'http://streamin.to/'+item[1] 
                titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+str(audio)+'] [/COLOR][COLOR lightblue]['+str(calidad)+'] [/COLOR][COLOR gold][HDFull][/I][/COLOR]'
                url_list.append(linkpeli);option_list.append(titlefull)
            if ("videomega") in server:
                linkpeli = 'http://videomega.tv/?ref='+item[1]    
                titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+str(audio)+'] [/COLOR][COLOR lightblue]['+str(calidad)+'] [/COLOR][COLOR gold][HDFull][/I][/COLOR]'
                url_list.append(linkpeli);option_list.append(titlefull)
            #####################################################################################################

    if source == "library": return option_list,url_list

################################################# Tools for Linker ##############################################

def peliculasdk_genr(genrfull):

    if len(genrfull) ==5: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]+', '+genrfull[4]
    elif len(genrfull) ==4: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]
    elif len(genrfull) ==3: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]
    elif len(genrfull) ==2: genrfull = genrfull[0]+', '+genrfull[1]
    elif len(genrfull) ==1: genrfull = genrfull[0]
    return genrfull
        
######################################### @ By Aquilesserr PalcoTv Team #########################################
    
