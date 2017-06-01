# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Linker Reyanime.com para PalcoTV
# Version 0.1 (15/06/2016)
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

thumbnail = "https://www.cubbyusercontent.com/pl/Reyanime_logo.PalcoTv.png/_2779caba023d42b3ad636fea33ac701c"
fanart = "https://www.cubbyusercontent.com/pl/Reyanime_fondoPalcoTV.jpg/_18d837d27ff14acea11f87d44e96d49c"

sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR seagreen]";ec3 = "[/COLOR]"
sc4 = "[COLOR red]";ec4 = "[/COLOR]"
sc5 = "[COLOR yellowgreen]";ec5 = "[/COLOR]"
version = " [0.1]"

web = "http://reyanime.com/"
referer = "http://reyanime.com/"

def reyanime_linker0(params):
    plugintools.log("[%s %s] Linker Reyanime %s" % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    r = requests.get(url)
    data = r.content
    
    bloq_info = plugintools.find_single_match(data,'<div class="cuerpo-todo">(.*?)<div class="lista-cap-title">')
    logo = 'http://reyanime.com'+plugintools.find_single_match(bloq_info,'<img src="([^"]+)"')
    if logo =="": logo = thumbnail 
    title_vid = plugintools.find_single_match(bloq_info,'<h1>(.*?)<b>').upper().strip()
    if title_vid =="": title_vid = 'N/D'
    tipe = plugintools.find_single_match(bloq_info,'<b>(.*?)</b>').strip()
    if tipe =="": tipe = 'N/D'
    title = title_vid+' '+tipe
    estado = plugintools.find_single_match(bloq_info,'<div class="box-([^<]+)">')
    if estado =="": estado = 'N/D'
    genrfull = plugintools.find_multiple_matches(bloq_info,'<a href="/genero/.*?">(.*?)</a>')
    genr = reyanime_genr(genrfull)
    if genr =="": genr = 'N/D'
    year = plugintools.find_single_match(bloq_info,'<div class="sinopsis".*?<span>(.*?)</span>').strip()
    if year =="": year = 'N/D'
    sinopsis = plugintools.find_single_match(bloq_info,'<div class="sinopsis".*?</h2>(.*?)</div>').strip().replace('&quot;','').replace('&amp;','')
    datamovie = {
    'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
    'year': sc3+'[B]Fecha: [/B]'+ec3+sc+str(year)+'[CR]'+ec,
    'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
    datamovie["plot"] = datamovie["genre"]+datamovie["year"]+datamovie["sinopsis"]

    titlefull = sc5+'[B]'+title+'[/B]'+ec5+sc+'  Estado: '+ec+sc3+'[I]('+estado+')[/I]'+ec3

    bloq_epis = plugintools.find_single_match(data,'<div class="lista-cap-title">(.*?)<div class="lista-cap-title">')
    epis = plugintools.find_multiple_matches(bloq_epis,'href="(.*?)">\s+<b>(.*?)</a>')
    
    datamovie_pass = genr+'|'+year+'|'+sinopsis #Pasando los datos a reyanime_resolverlink

    if len(epis) > 1:
        plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker Reyanime"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
        plugintools.add_item(action="",url="",title=titlefull,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
        
        for item in epis:
            try:
                url_vid = item[0];url_vid = 'http://reyanime.com'+url_vid
                title = item[1].replace('</b>','').strip()
                plugintools.addPeli(action="reyanime_resolverlink",url=url_vid,title=sc+title+ec,info_labels=datamovie,extra=datamovie_pass,thumbnail=logo,fanart=fanart,folder=True,isPlayable=False)
            except:pass
    elif len(epis) <= 1:
        try:
            url = plugintools.find_single_match(bloq_epis,'href="(.*?)"')
            url_vid = 'http://reyanime.com'+url
            title = str(title_vid)
            titlefull = sc5+'[B]'+title+'[/B]'+ec5+sc+'  Estado: '+ec+sc3+'[I]('+estado+')[/I]'+ec3
            params["url"] = url_vid; params["extra"] = datamovie_pass; params["thumbnail"] = logo; params["title"] = titlefull #Cogiendo los parametros necesarios
            reyanime_resolverlink(params)
        except:pass

def reyanime_resolverlink(params):
    plugintools.log("[%s %s] Linker Reyanime %s" % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker Reyanime"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    
    url = params.get("url")
    logo = params.get("thumbnail")
    title = params.get("title")
    if not sc5 in title:
        title = title.replace(sc,sc5).replace(ec,ec5)
        title = sc5+'[B]'+title+'[/B]'+ec5
    try:
        datamovie = params.get("extra").split('|')
        datamovie = {
        'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(datamovie[0])+', '+ec,
        'year': sc3+'[B]Fecha: [/B]'+ec3+sc+str(datamovie[1])+'[CR]'+ec,
        'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(datamovie[2])+ec}
        datamovie["plot"] = datamovie["genre"]+datamovie["year"]+datamovie["sinopsis"]
    except:
        datamovie = {'sinopsis': sc3+'[B]No hay Descripción Disponible[/B]'+ec3}
        datamovie["plot"] = datamovie["sinopsis"]

    headers = {'Host':'reyanime.com','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0','Referer':referer}
    r = requests.get(url,headers=headers)
    data = r.content
    plugintools.addPeli(action="",url="",title=title,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    bloq_opc = plugintools.find_single_match(data,'<div class="lista-capt">(.*?)<div class="video-redes">')
    control_server = plugintools.find_single_match(bloq_opc,'tabsArray(.*?)</iframe>') # Comprueba que existen conectores
    if control_server =="":
        plugintools.addPeli(action="",url="",title=sc4+'No hay Enlaces Disponibles'+ec4,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    else: 
        bloq_opc = plugintools.find_single_match(data,'<div class="lista-capt">(.*?)<div class="video-redes">')
        name_server = plugintools.find_multiple_matches(bloq_opc,'<a rel="nofollow" href=".*?>(.*?)</a>')
        print name_server
        url_vid = plugintools.find_multiple_matches(bloq_opc,'<iframe src="(.*?)"')
        i = 0
        for item in name_server:
            server_url = url_vid[i]
            
            if '/picasa?v=' in server_url: server = 'picasa'; tipe_resolver = 'resolver_tipe_2' 
            elif '/az?v=' in server_url: server = 'anaforce'; tipe_resolver = 'resolver_tipe_1' 
            elif '/amz?v=' in server_url: server = 'amazon'; tipe_resolver = 'amazon' 
            elif '/maz?v=' in server_url: server = 'larata'; tipe_resolver = 'resolver_tipe_2'  
            elif '/h5?v=8f8V' in server_url: server = 'datacloudmail'; tipe_resolver = 'resolver_tipe_1'
            elif '/docsgo?v=' in server_url: server = 'googledocs'; tipe_resolver = 'resolver_tipe_2' 
            elif '/send?v=' in server_url: server = 'sendvid'; tipe_resolver = 'resolver_tipe_2'
            elif '/msend?v=' in server_url: server = 'sendvid'; tipe_resolver = 'resolver_tipe_3'
            #elif '/bitcasa?v=' in server_url: server = 'bitcasa'  
            #elif '/shared?v=' in server_url: server = 'shared' 
            #elif '/4shared?v=' in server_url: server = '4shared' 
            #elif '/zipy?v=' in server_url: server = 'zippyshare' 
            ########################### Conectores en resolvers.py ##################################
            elif '/nov?v=' in server_url: server = 'novamov'; tipe_resolver = 'resolver_tipe_conector'
            elif '/mnov?v=' in server_url: server = 'novamov'; tipe_resolver = 'resolver_tipe_conector'  
            elif '/nowv?v=' in server_url: server = 'nowvideo'; tipe_resolver = 'resolver_tipe_conector'
            elif '/mnowv?v=' in server_url: server = 'nowvideo'; tipe_resolver = 'resolver_tipe_conector'
            elif '/rut?v=' in server_url: server = 'rutube'; tipe_resolver = 'resolver_tipe_conector'
            elif '/mrut?v=' in server_url: server = 'rutube'; tipe_resolver = 'resolver_tipe_conector'
            elif '/mp4?v=' in server_url: server = 'mp4upload'; tipe_resolver = 'resolver_tipe_conector'
            elif '/vimp?v=' in server_url: server = 'vimple'; tipe_resolver = 'resolver_tipe_conector'  
            elif '/vidweed?v=' in server_url: server = 'videoweed'; tipe_resolver = 'resolver_tipe_conector' 
            elif '/vk?v=' in server_url: server = 'vk'; tipe_resolver = 'resolver_tipe_conector' 
            elif '/mvk?v=' in server_url: server = 'newvk'; tipe_resolver = 'resolver_tipe_conector'
            #elif '/bam?v=' in server_url: server = 'videobam' 
            #elif '/mbam?v=' in server_url: server = 'videobam'
            else: server = 'unknown'
            #########################################################################################
            j = i+1 # Numeracion de Opciones
            if not'unknown' in server:
                titlefull = sc+'Opc.'+str(j)+ec+sc5+' [I]['+server.title()+'][/I]'+ec5
                plugintools.addPeli(action=tipe_resolver,url=server_url,title=titlefull,info_labels=datamovie,thumbnail=logo,fanart=fanart,folder=False,isPlayable=True)
            i = i+1
    
################################################### Herramientas #################################################

def reyanime_genr(genrfull):
    
    if len(genrfull) ==5: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]+', '+genrfull[4]
    elif len(genrfull) ==4: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]
    elif len(genrfull) ==3: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]
    elif len(genrfull) ==2: genrfull = genrfull[0]+', '+genrfull[1]
    elif len(genrfull) ==1: genrfull = genrfull[0]
    elif len(genrfull) >5: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]+', '+genrfull[4]
    else: genrfull = 'N/D' 
    return genrfull

#################################################### Conectores ##################################################

def resolver_tipe_conector(params):
    plugintools.log('[%s %s] Resolver Tipe Conector %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    try:
        ########################################### Modificando urls ############################################
        if '/nowv?v=' in url:
            media_url = url.replace('http://ozhe.larata.in/repro-rc/nowv?v=','http://www.nowvideo.sx/video/')
        elif '/mnowv?v=' in url:
            media_url = url.replace('http://ozhe.larata.in/repro-rc/mnowv?v=','http://www.nowvideo.sx/video/')
        elif '/nov?v=' in url:
            media_url = url.replace('http://ozhe.larata.in/repro-rc/nov?v=','http://www.novamov.com/video/')
        elif '/mnov?v=' in url:
            media_url = url.replace('http://ozhe.larata.in/repro-rc/mnov?v=','http://www.novamov.com/video/')
        elif '/mp4?v=' in url:
            media_url = url.replace('http://ozhe.larata.in/repro-rc/mp4?v=','http://www.mp4upload.com/')
        elif '/vidweed?v=' in url:
            media_url = url.replace('http://ozhe.larata.in/repro-rc/vidweed?v=','http://www.videoweed.es/file/')
        #########################################################################################################
        else:
            headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14",'Referer':referer}
            r = requests.get(url,headers=headers)
            data = r.content
            media_url = plugintools.find_single_match(data,'<iframe src="([^"]+)"')
            if media_url =="":
                media_url = plugintools.find_single_match(data,'<embed src="(.*?)"')

        if media_url.find("rutube.ru") >= 0: params["url"]=media_url; rutube(params)
        elif media_url.find("vimple.ru") >= 0: params["url"]=media_url; vimple(params)
        elif media_url.find("videoweed.es") >= 0: params["url"]=media_url; videoweed(params)
        elif media_url.find("nowvideo.sx") >= 0: params["url"]=media_url; nowvideo(params)
        elif media_url.find("novamov.com") >= 0: params["url"]=media_url; novamov(params)
        elif media_url.find("mp4upload.com") >= 0: params["url"]=media_url; mp4upload(params)
        ################################# Opciones VK #######################################
        elif media_url.find("videosxd.org") >= 0: params["url"]=media_url; vk(params)
        elif media_url.find("vkontakte.ru") >= 0: params["url"]=media_url; vk(params)
        #####################################################################################
    except:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))

def resolver_tipe_1(params):
    plugintools.log('[%s %s] Resolver Tipe 1 %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14",'Referer':referer}
    r = requests.get(url,headers=headers)
    data = r.content
    try:
        media_url = plugintools.find_single_match(data,'file: "([^"]+)"')
        if media_url =="":
            media_url = plugintools.find_single_match(data,"file: '([^']+)'")
        print '$'*45+'- By PalcoTV Team -'+'$'*45,media_url,'$'*109
    except:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    plugintools.play_resolved_url(media_url)

def resolver_tipe_2(params):
    plugintools.log('[%s %s] Resolver Tipe 2 %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14",'Referer':referer}
    r = requests.get(url,headers=headers)
    data = r.content
    try:
        url_iframe = plugintools.find_single_match(data,'<iframe src="([^"]+)"')
        headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14",'Referer':referer}
        r = requests.get(url_iframe,headers=headers)
        data = r.content
        media_url = plugintools.find_single_match(data,'file: "([^"]+)"')
        if media_url =="": media_url = plugintools.find_single_match(data,'file=([^&]+)&')
        if media_url =="": media_url = plugintools.find_single_match(data,'link:"(.*?)"')
        print '$'*48+'- By PalcoTV Team -'+'$'*48,media_url,'$'*115
    except:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    plugintools.play_resolved_url(media_url)

def resolver_tipe_3(params):
    plugintools.log('[%s %s] Resolver Tipe 3 %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14",'Referer':referer}
    r = requests.get(url,headers=headers)
    data = r.content
    try:
        iframe = plugintools.find_single_match(data,'src="([^"]+)"')
        url_iframe = 'http:'+ iframe
        headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14",'Referer':referer}
        r = requests.get(url_iframe,headers=headers)
        data = r.content
        media = plugintools.find_single_match(data,'var video_source = "([^"]+)"')
        media_url = 'http:'+ media
        print '$'*45+'- By PalcoTV Team -'+'$'*45,media_url,'$'*109
    except:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    plugintools.play_resolved_url(media_url)

def amazon(params):
    plugintools.log('[%s %s] Amazon %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14",'Referer':referer}
    r = requests.get(url,headers=headers)
    data = r.content
    try:
        url_iframe = plugintools.find_single_match(data,'<iframe src="([^"]+)"')
        headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14",'Referer':referer}
        r = requests.get(url_iframe,headers=headers)
        data = r.content
        url_amazon = plugintools.find_single_match(data,'link:"(.*?)"')
        r = requests.get(url_amazon)
        data = r.content
        url_reponse = plugintools.find_single_match(data,'downloadUrl: encodeURI\("(.*?)"')
        url_reponse_headers = 'https://www.amazon.com' + url_reponse
        r = requests.get(url_reponse_headers,allow_redirects=False)
        data = r.headers
        media_url = r.headers['location']
        print '$'*48+'- By PalcoTV Team -'+'$'*48,media_url,'$'*115
    except:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    plugintools.play_resolved_url(media_url)

######################################### @ By Aquilesserr PalcoTv Team ######################################### 

    
    
    
    