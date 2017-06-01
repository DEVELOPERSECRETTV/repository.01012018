# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Linker Jkanime.com para PalcoTV
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

thumbnail = "https://www.cubbyusercontent.com/pl/Jkanime_logo.png/_ed7d4b5b2272467db40674286963762f"
fanart = "https://www.cubbyusercontent.com/pl/Jkanime_fondo.jpg/_86f0b8170ab84c2f8c12f14b0965f9a6"

sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR seagreen]";ec3 = "[/COLOR]"
sc4 = "[COLOR red]";ec4 = "[/COLOR]"
sc5 = "[COLOR yellowgreen]";ec5 = "[/COLOR]"
version = " [0.1]"

web = "http://jkanime.net/"
referer = "http://jkanime.net/"

def jkanime_linker0(params):
    plugintools.log("[%s %s] Linker Jkanime %s" % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    r = requests.get(url)
    data = r.content
    tipe = plugintools.find_single_match(data,'class="labl">Tipo:</span>(.*?)</span></div>')
    #tipe: Series, Ovas, Pelicula
    if 'Serie' in tipe: params["url"] = url; jkanime_videoserie(params)
    if 'ONA' in tipe: params["url"] = url; jkanime_videoserie(params)
    elif 'Pelicula' in tipe: params["url"] = url; jkanime_videopeli(params)
    elif 'OVA' in tipe: params["url"] = url; jkanime_videopeli(params)
    elif 'Especial' in tipe: params["url"] = url; jkanime_videoserie(params) 
    
def jkanime_videopeli(params):
    
    url = params.get("url")
    r = requests.get(url)
    data = r.content
    
    bloq_info = plugintools.find_single_match(data,'<div class="cont_top"></div>(.*?)<div id="footer">')
    logo = plugintools.find_single_match(bloq_info,'<img title=".*?src="([^"]+)"')
    if logo =="": logo = thumbnail 
    title = plugintools.find_single_match(bloq_info,'<div  class="sinopsis_title title21">([^<]+)</div>').upper().strip()
    estado = plugintools.find_single_match(bloq_info,'<div><span class="labl">Estado:</span>.*?">([^<]+)</span>').strip()
    if estado =="": estado = 'N/D'
    genrfull = plugintools.find_multiple_matches(bloq_info,'http://jkanime.net/genero/(.*?)/')
    genr = jkanime_genr(genrfull)
    year = plugintools.find_single_match(bloq_info,'<div><span class="labl">Emitido:</span>.*?">(.*?)</span>').strip().replace('<br/>','')
    if year =="": year = 'N/D'
    duration = plugintools.find_single_match(bloq_info,'<div><span class="labl">Duracion:</span>.*?">([^<]+)</span>').strip().replace('<br/>','')
    if duration =="": duration = 'N/D'
    url_vid = plugintools.find_single_match(bloq_info,'<div class="listbox".*?<a href="([^"]+)"')
    sinopsis = plugintools.find_single_match(bloq_info,'<div class="sinoptext">\s+<p>(.*?)</p>').strip().replace('<br/>','')

    titlefull = sc5+'[B]'+title+'[/B]'+ec5+sc+'  Estado: '+ec+sc3+'[I]('+estado+')[/I]'+ec3

    datamovie = {
    'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
    'duration': sc3+'[B]Duración: [/B]'+ec3+sc+str(duration)+', '+ec,
    'year': sc3+'[B]Fecha de Inicio: [/B]'+ec3+sc+str(year)+'[CR]'+ec,
    'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
    datamovie["plot"] = datamovie["genre"]+datamovie["duration"]+datamovie["year"]+datamovie["sinopsis"]

    datamovie_pass = genr+'|'+duration+'|'+year+'|'+sinopsis
    params["url"] = url_vid; params["extra"] = datamovie_pass; params["thumbnail"] = logo; params["title"] = titlefull #Cogiendo los parametros necesarios
    jkanime_resolverlink(params)

def jkanime_videoserie(params):
    plugintools.log("[%s %s] Linker Jkanime %s" % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    r = requests.get(url)
    data = r.content
    
    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker Jkanime"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    bloq_info = plugintools.find_single_match(data,'<div class="cont_top"></div>(.*?)<div id="footer">')
    logo = plugintools.find_single_match(bloq_info,'<img title=".*?src="([^"]+)"')
    if logo =="": logo = thumbnail 
    title = plugintools.find_single_match(bloq_info,'<div  class="sinopsis_title title21">([^<]+)</div>').upper().strip()
    estado = plugintools.find_single_match(bloq_info,'<div><span class="labl">Estado:</span>.*?">([^<]+)</span>').strip()
    if estado =="": estado = 'N/D'
    genrfull = plugintools.find_multiple_matches(bloq_info,'http://jkanime.net/genero/(.*?)/')
    genr = jkanime_genr(genrfull)
    year = plugintools.find_single_match(bloq_info,'<div><span class="labl">Emitido:</span>.*?">(.*?)</span>').strip().replace('<br/>','')
    if year =="": year = 'N/D'
    duration = plugintools.find_single_match(bloq_info,'<div><span class="labl">Duracion:</span>.*?">([^<]+)</span>').strip().replace('<br/>','')
    if duration =="": duration = 'N/D'
    sinopsis = plugintools.find_single_match(bloq_info,'<div class="sinoptext">\s+<p>(.*?)</p>').strip().replace('<br/>','')

    titlefull = sc5+'[B]'+title+'[/B]'+ec5+sc+'  Estado: '+ec+sc3+'[I]('+estado+')[/I]'+ec3

    datamovie = {
    'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
    'duration': sc3+'[B]Duración: [/B]'+ec3+sc+str(duration)+', '+ec,
    'year': sc3+'[B]Fecha de Inicio: [/B]'+ec3+sc+str(year)+'[CR]'+ec,
    'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
    datamovie["plot"] = datamovie["genre"]+datamovie["duration"]+datamovie["year"]+datamovie["sinopsis"]

    datamovie_pass = genr+'|'+duration+'|'+year+'|'+sinopsis
    plugintools.add_item(action="",url="",title=titlefull,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)

    ############ Extración de Episodios ##########
     
    epis_list = plugintools.find_single_match(data,'<div class="listnavi">(.*?)</div>')
    epis_bloq = plugintools.find_multiple_matches(epis_list,'<a  class="listpag list22" href="#pag(.*?)">')
    id_file = plugintools.find_single_match(data,'ajax/pagination_episodes/(.*?)/')
    for item in epis_bloq:
        #http://jkanime.net/ajax/pagination_episodes/814/2/
        url = 'http://jkanime.net/ajax/pagination_episodes/'+id_file+'/'+item+'/'
        info_epis = extrac_epis(url)
        try:
            for item in info_epis:
                number_epis = item[0]
                title_epis = item[1].decode('unicode_escape').encode('utf8') 
                url = plugintools.find_single_match(data,"href: '(.*?)'")
                url_epis = url+number_epis+'/'
                titlefull = sc+'Episodio '+str(number_epis)+ec+' - '+sc5+title_epis+ec5
                plugintools.addPeli(action="jkanime_resolverlink",url=url_epis,title=titlefull,info_labels=datamovie,extra=datamovie_pass,thumbnail=logo,fanart=fanart,folder=True,isPlayable=False)
        except:pass

    ##############################################
         
def jkanime_resolverlink(params):
    plugintools.log("[%s %s] Linker Jkanime %s" % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Parser Linker Jkanime"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    
    url = params.get("url")
    logo = params.get("thumbnail")
    title = params.get("title")
    try:
        datamovie = params.get("extra").split('|')
        datamovie = {
        'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(datamovie[0])+', '+ec,
        'duration': sc3+'[B]Duración: [/B]'+ec3+sc+str(datamovie[1])+', '+ec,
        'year': sc3+'[B]Fecha de Inicio: [/B]'+ec3+sc+str(datamovie[2])+'[CR]'+ec,
        'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(datamovie[3])+ec}
        datamovie["plot"] = datamovie["genre"]+datamovie["year"]+datamovie["sinopsis"]
    except:
        datamovie = {'sinopsis': sc3+'[B]No hay Descripción Disponible[/B]'+ec3}
        datamovie["plot"] = datamovie["sinopsis"]

    headers = {'Host':'jkanime.net','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0','Referer':web}
    r = requests.get(url,headers=headers)
    data = r.content
    
    plugintools.add_item(action="",url="",title=title,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    
    bloq_opc = plugintools.find_single_match(data,'<select id="select_lang">(.*?)<div class="video_nav"')
    if bloq_opc =="":
        bloq_opc = plugintools.find_single_match(data,'<div class="video_option_act">(.*?)<div class="video_left">')
    control_server = plugintools.find_single_match(bloq_opc,'href="#">(.*?)</a>') # Comprueba que existen conectores
    if control_server =="":
        plugintools.addPeli(action="",url="",title=sc4+'No hay Enlaces Disponibles'+ec4,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    else:
        lang = plugintools.find_single_match(bloq_opc,'<option value=".*?">(.*?)</option>')
        if lang =="": lang = 'N/D' 
        opc_server = plugintools.find_multiple_matches(bloq_opc,'href="#">(.*?)</a>')
        opc_url = plugintools.find_multiple_matches(bloq_opc,'<iframe class="player_conte" src=(.*?)\s')
        i = 0
        for item in opc_server:
            try:
                if 'Desuka' in item: name_server = '[I][Desuka][/I]';server = 'play_video'
                elif 'Anime' in item: name_server = '[I][Anime][/I]';server = 'openload'
                elif 'Misuki' in item: name_server = '[I][Misuki][/I]';server = 'play_video'
                elif 'Xtreme S' in item: name_server = '[I][Xtreme S][/I]';server = 'play_video'
                elif 'Xtreme HD' in item: name_server = '[I][Xtreme HD][/I]';server = 'play_video'
                elif 'Dailymotion' in item: name_server = '[I][Dailymotion][/I]';server = 'dailymotion'
                ####### Reemplazando espacios y comillas extraidas para corregir el error #######
                url_server = opc_url[i].replace(' ','').replace('"','').replace("'",'')
                ################################################################################# 
                j = i+1 # Numeracion para las Opciones
                titlefull = sc+'Opc.'+str(j)+': '+ec+sc2+'[I]['+lang+'][/I]'+ec2+sc5+'  '+name_server+ec5
                plugintools.addPeli(action=server,url=url_server,title=titlefull,info_labels=datamovie,thumbnail=logo,fanart=fanart,folder=False,isPlayable=True)
                i = i+1
            except:pass
        
################################################### Herramientas #################################################

def jkanime_genr(genrfull):
    
    if len(genrfull) ==5: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]+', '+genrfull[4]
    elif len(genrfull) ==4: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]
    elif len(genrfull) ==3: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]
    elif len(genrfull) ==2: genrfull = genrfull[0]+', '+genrfull[1]
    elif len(genrfull) ==1: genrfull = genrfull[0]
    elif len(genrfull) >5: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]+', '+genrfull[4]
    else: genrfull = 'N/D' 
    return genrfull

def extrac_epis(url):

    r = requests.get(url)#,headers=headers)
    data = r.content
    info_epis = plugintools.find_multiple_matches(data,'number":"(.*?)","title":"(.*?)"')
    return info_epis

#################################################### Conectores ##################################################

def play_video(params):
    plugintools.log('[%s %s] Play Video %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14",'Referer':referer}
    r = requests.get(url,headers=headers)
    data = r.content
    try:
        url_redir = plugintools.find_single_match(data,'<embed class=".*?&file=(.*?)"')
        r = requests.get(url_redir,allow_redirects=False)
        time.sleep(5)
        media_url = r.headers['location']
        if media_url =="": 
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "El Servidor ha Denegado el Acceso", 3 , art+'icon.png'))
        else:
            print '$'*45+'- By PalcoTV Team -'+'$'*45,media_url,'$'*109
            plugintools.play_resolved_url(media_url)
    except:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
     
######################################### @ By Aquilesserr PalcoTv Team ######################################### 
    

    
    

 
    

    