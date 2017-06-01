# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Linker AnimeFLV.com para PalcoTV
# Version 0.1 (28/05/2016)
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

import plugintools, requests, json
from resources.tools.resolvers import *
from resources.tools.media_analyzer import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

thumbnail = "https://www.cubbyusercontent.com/pl/Animeflv_logo_palcotv.png/_6ff9150542014d8d81fb2fb01a4dffbf"
fanart = "https://www.cubbyusercontent.com/pl/Animeflv_fanart_palcotv.jpg/_c9da419d81be423f85951668b61fdf05"

sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR seagreen]";ec3 = "[/COLOR]"
sc4 = "[COLOR red]";ec4 = "[/COLOR]"
sc5 = "[COLOR yellowgreen]";ec5 = "[/COLOR]"
version = " [0.1]"

web = "http://animeflv.net/"
referer = "http://animeflv.net/animes/"

def animeflv_linker0(params):
    plugintools.log("[%s %s] Linker AnimeFLV %s" % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    headers = {'Host':'animeflv.net','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0','Referer':referer}
    r = requests.get(url,headers=headers)
    data = r.content
    #tipe 1: Series, tipe_2: Ovas, tipe_3: Pelicula
    if 'http://animeflv.net/anime' in url: params["url"] = url; animeflv_videoserie(params)
    elif 'http://animeflv.net/ova' in url: params["url"] = url; animeflv_videoserie(params)
    elif 'http://animeflv.net/pelicula' in url: params["url"] = url; animeflv_videopeli(params) 

def animeflv_videopeli(params):
    plugintools.log("[%s %s] Linker AnimeFLV %s" % (addonName, addonVersion, repr(params)))

    url = params.get("url") 
    headers = {'Host':'animeflv.net','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0','Referer':web}
    r = requests.get(url,headers=headers)
    data = r.content
    bloq_info = plugintools.find_single_match(data,'<div class="anime_info">(.*?)<div class="clear"></div>')
    logo = plugintools.find_single_match(bloq_info,'<img src="([^"]+)"')
    if logo =="": logo = thumbnail 
    title = plugintools.find_single_match(bloq_info,'<h1>([^<]+)</h1>').upper().strip()
    title = title.replace('&aacute;','á').replace('&eacute;','é').replace('&iacute;','í').replace('&oacute;','ó').replace('&uacute;','ú')
    title = title.replace('&amp;','').replace('&#039;','').replace('&ntilde;','ñ')
    estado = plugintools.find_single_match(bloq_info,'<span class="serie_estado_2">([^<]+)</span>').strip().replace('&oacute;','ó')
    if estado =="": estado = 'N/D'

    #bloq_genr = plugintools.find_single_match(data,'<li><b>Generos:</b>(.*?)</li>')
    genrfull = plugintools.find_multiple_matches(bloq_info,'<a href="/animes/genero/(.*?)/')
    genr = animeflv_genr(genrfull)
    if genr =="": genr = 'N/D'
    year = plugintools.find_single_match(bloq_info,'<li><b>Fecha de Inicio:</b>([^<]+)</li>').strip()
    if year =="": year = 'N/D'

    sinopsis = plugintools.find_single_match(bloq_info,'<div class="sinopsis">(.*?)</div>').strip()
    sinopsis = sinopsis.replace('&ldquo;','').replace('&rdquo;','').replace('&quot;','').replace('&#039;','').replace('&ntilde;','ñ')
    sinopsis = sinopsis.replace('&amp;','').replace('&aacute;','á').replace('&eacute;','é').replace('&iacute;','í').replace('&oacute;','ó').replace('&uacute;','ú')
    datamovie_pass = genr+'|'+year+'|'+sinopsis #Parametros para animeflv_resolverlink
    
    ################ Control comprueba si la Peli dispone de varios enlaces ##########################

    bloq_vid = plugintools.find_single_match(bloq_info,'<ul class="anime_episodios"(.*?)</ul>')
    vid = plugintools.find_multiple_matches(bloq_vid,'<li><a(.*?)</li>')
    if len(vid)>1:
        plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker AnimeFLV"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
        for item in vid:
            datamovie = {
            'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
            'year': sc3+'[B]Fecha de Inicio: [/B]'+ec3+sc+str(year)+'[CR]'+ec,
            'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
            datamovie["plot"] = datamovie["genre"]+datamovie["year"]+datamovie["sinopsis"]
            url_vid = plugintools.find_single_match(item,'href="([^"]+)"')
            url_vid = 'http://animeflv.net'+url_vid
            title_epis = plugintools.find_single_match(item,'href=".*?">([^<]+)</a>')
            plugintools.addPeli(action="animeflv_resolverlink",url=url_vid,title=sc+title_epis+ec,info_labels=datamovie,extra=datamovie_pass,thumbnail=logo,fanart=fanart,folder=True,isPlayable=False)
    
    ############################# Else la Peli solo dispone de un link ##############################
    else:
        url_vid = plugintools.find_single_match(bloq_info,'<ul class="anime_episodios".*?<a href="([^"]+)"')
        url_vid = 'http://animeflv.net'+url_vid
        params["url"] = url_vid; params["extra"] = datamovie_pass; params["thumbnail"] = logo; params["title"] = title
        animeflv_resolverlink(params) #Pasando todos los parametros a animeflv_resolverlink sin paradas en add_item
    

def animeflv_videoserie(params):
    plugintools.log("[%s %s] Linker AnimeFLV %s" % (addonName, addonVersion, repr(params)))

    url = params.get("url"); genr = params.get("extra")

    headers = {'Host':'animeflv.net','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0','Referer':web}
    r = requests.get(url,headers=headers)
    data = r.content
    bloq_info = plugintools.find_single_match(data,'<div class="anime_info">(.*?)<div class="clear"></div>')
    logo = plugintools.find_single_match(bloq_info,'<img src="([^"]+)"')
    if logo =="": logo = thumbnail 
    title = plugintools.find_single_match(bloq_info,'<h1>([^<]+)</h1>').upper().strip()
    title = title.replace('&aacute;','á').replace('&eacute;','é').replace('&iacute;','í').replace('&oacute;','ó').replace('&uacute;','ú')
    title = title.replace('&amp;','').replace('&#039;','').replace('&ntilde;','ñ')
    estado = plugintools.find_single_match(bloq_info,'<span class="serie_estado.*?">([^<]+)</span>').strip().replace('&oacute;','ó')
    if estado =="": estado = 'N/D'
    year = plugintools.find_single_match(bloq_info,'<li><b>Fecha de Inicio:</b>([^<]+)</li>').strip()
    if year =="": year = 'N/D'
    sinopsis = plugintools.find_single_match(bloq_info,'<div class="sinopsis">(.*?)</div>').strip()
    sinopsis = sinopsis.replace('&ldquo;','').replace('&rdquo;','').replace('&quot;','').replace('&ntilde;','ñ').replace('&#039;','')
    sinopsis = sinopsis.replace('&amp;','').replace('&aacute;','á').replace('&eacute;','é').replace('&iacute;','í').replace('&oacute;','ó').replace('&uacute;','ú')

    titlefull = sc5+'[B]'+title+'[/B]'+sc+'  Estado: '+ec+sc3+'[I]('+estado+')[/I]'+ec3

    datamovie = {
    'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
    'year': sc3+'[B]Fecha de Inicio: [/B]'+ec3+sc+str(year)+'[CR]'+ec,
    'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
    datamovie["plot"] = datamovie["genre"]+datamovie["year"]+datamovie["sinopsis"]
    
    bloq_epis = plugintools.find_single_match(bloq_info,'<ul class="anime_episodios"(.*?)</ul>')
    epis = plugintools.find_multiple_matches(bloq_epis,'<a href="(.*?)">(.*?)</a></li>')
    
    datamovie_pass = genr+'|'+year+'|'+sinopsis #Pasando los datos a animeflv_resolverlink

    if len(epis) > 1:
        plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker AnimeFLV"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
        plugintools.add_item(action="",url="",title=titlefull,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
        for item in epis:
            try:
                url_vid = item[0];url_vid = 'http://animeflv.net'+url_vid
                title = item[1]
                title = title.replace('&aacute;','á').replace('&eacute;','é').replace('&iacute;','í').replace('&oacute;','ó').replace('&uacute;','ú')
                title = title.replace('&amp;','').replace('&#039;','').replace('&ntilde;','ñ')
                plugintools.addPeli(action="animeflv_resolverlink",url=url_vid,title=sc+title+ec,info_labels=datamovie,extra=datamovie_pass,thumbnail=logo,fanart=fanart,folder=True,isPlayable=False)
            except:pass

    #################### Control para OVAS, saltando a animeflv_resolverlink si dispone de un solo link ########################################################
    
    elif len(epis) <= 1:
        try:
            epis = plugintools.find_single_match(bloq_epis,'<a href="(.*?)">(.*?)</a></li>')
            url_vid = str(epis[0])
            url_vid = 'http://animeflv.net'+url_vid
            title = str(epis[-1])
            params["url"] = url_vid; params["extra"] = datamovie_pass; params["thumbnail"] = logo; params["title"] = title #Cogiendo los parametros necesarios
            animeflv_resolverlink(params)
        except:pass

    ############################################################################################################################################################
            
def animeflv_resolverlink(params):
    plugintools.log("[%s %s] Linker AnimeFLV %s" % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker AnimeFLV"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    
    url = params.get("url")
    logo = params.get("thumbnail")
    title = params.get("title").replace(sc,'').replace(ec,'')
    title = title.replace('&AACUTE;','Á').replace('&EACUTE;','É').replace('&IACUTE;','Í').replace('&OACUTE;','Ó').replace('&UACUTE;','Ú')
    
    try:
        datamovie = params.get("extra").split('|')
        datamovie = {
        'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(datamovie[0])+', '+ec,
        'year': sc3+'[B]Fecha de Inicio: [/B]'+ec3+sc+str(datamovie[1])+'[CR]'+ec,
        'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(datamovie[2])+ec}
        datamovie["plot"] = datamovie["genre"]+datamovie["year"]+datamovie["sinopsis"]
    except:
        datamovie = {'sinopsis': sc3+'[B]No hay Descripción Disponible[/B]'+ec3}
        datamovie["plot"] = datamovie["sinopsis"]

    headers = {'Host':'animeflv.net','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0','Referer':web}
    r = requests.get(url,headers=headers)
    data = r.content
    
    plugintools.addPeli(action="",url="",title=sc5+"[B]"+title+"[/B]"+ec5,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    
    bloq_opc = plugintools.find_single_match(data,'<div class="box_opc" id="opciones_box"(.*?)<div class="box_opc" id="descargas_box"')
    control_server = plugintools.find_single_match(bloq_opc,'/img/servers/(.*?)\.') # Comprueba que existen conectores
    if control_server =="":
        plugintools.addPeli(action="",url="",title=sc4+'No hay Enlaces Disponibles'+ec4,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    else: 
        opc = plugintools.find_multiple_matches(bloq_opc,'<div class="opcion video_opcion"(.*?)</div>')
        bloq_url = plugintools.find_single_match(data,'var videos =(.*?)\]\};')
        url_vid = plugintools.find_multiple_matches(bloq_url,'src=.*?"(.*?)"')
        i = 0
        for item in opc:
            name_server = plugintools.find_single_match(item,'/img/servers/(.*?)\.')
            opcion = plugintools.find_single_match(item,'class="server"/><b>(.*?)</b>')
            lang = plugintools.find_single_match(item,'<b>Audio:</b> <img src="/img/idiomas/(.*?)\.')
            if 'ES' in lang: lang = '[I][Esp][/I]'
            elif 'JP' in lang: lang = '[I][Jap][/I]'
            else: lang = 'N/D'
            sub = plugintools.find_single_match(item,'<b>Subs:</b> <img src="/img/idiomas/(.*?)\.')
            if 'ES' in sub: sub = '[I][Esp][/I]'
            elif 'JP' in sub: sub = '[I][Jap][/I]'
            else: sub = 'N/D'
            server_url = url_vid[i].replace('\\','')
            if 'dailymotion' in server_url: server_url = 'http:'+server_url # Resolviendo el error de ausencia de http: en Dailymotion
            server = video_analyzer(name_server)
            
            if 'izanagi' in server_url: server = 'izanagi'
            elif 'yotta' in server_url: server = 'yotta'
            elif 'kami' in server_url: server = 'kami'
            j = i+1 # Numeracion para las Opciones
            titlefull = sc+'Opc.'+str(j)+'   Aud: '+ec+sc2+lang+ec2+sc+'  Sub: '+ec+sc2+sub+ec2+sc5+' [I]['+server.title()+'][/I]'+ec5
            plugintools.addPeli(action=server,url=server_url,title=titlefull,info_labels=datamovie,thumbnail=logo,fanart=fanart,folder=False,isPlayable=True)
            i = i+1
   
################################################### Herramientas #################################################

def animeflv_genr(genrfull):
    
    if len(genrfull) ==5: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]+', '+genrfull[4]
    elif len(genrfull) ==4: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]
    elif len(genrfull) ==3: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]
    elif len(genrfull) ==2: genrfull = genrfull[0]+', '+genrfull[1]
    elif len(genrfull) ==1: genrfull = genrfull[0]
    elif len(genrfull) >5: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]+', '+genrfull[4]
    else: genrfull = 'N/D' 
    return genrfull

#################################################### Conectores ##################################################

def izanagi(params):
    plugintools.log('[%s %s] Izanagi %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14",'Referer':referer}
    r = requests.get(url,headers=headers)
    data = r.content
    url_js = plugintools.find_single_match(data,"\.get\('(.*?)'")
    url_js = urllib.unquote(url_js) 
    r = requests.get(url_js,headers=headers)
    data_js = r.content
    try:
        js = json.loads(data_js)
        media_url = js["file"]
        print '$'*45+'- By PalcoTV Team -'+'$'*45,media_url,'$'*109
    except:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    plugintools.play_resolved_url(media_url)

def yotta(params):
    plugintools.log('[%s %s] Yotta %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14",'Referer':referer}
    r = requests.get(url,headers=headers)
    data = r.content
    url_js = plugintools.find_single_match(data,"\.get\('(.*?)'")
    url_js = urllib.unquote(url_js) 
    r = requests.get(url_js,headers=headers)
    data_js = r.content
    try:
        js = json.loads(data_js)
        media_url = js["sources"][0]['file']
        print '$'*218+'- By PalcoTV Team -'+'$'*218,media_url,'$'*455
    except:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    plugintools.play_resolved_url(media_url)

def kami(params):
    plugintools.log('[%s %s] Yotta %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14",'Referer':referer}
    r = requests.get(url,headers=headers)
    data = r.content
    sources = plugintools.find_single_match(data,"sources: \[\{(.*?)\}\],")
    media_url = plugintools.find_multiple_matches(sources,'file: "([^"]+)"')
    try:
        media_url = media_url[0] 
        print '$'*43+'- By PalcoTV Team -'+'$'*43,media_url,'$'*105
    except:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    plugintools.play_resolved_url(media_url)
    
######################################### @ By Aquilesserr PalcoTv Team ######################################### 
    

    