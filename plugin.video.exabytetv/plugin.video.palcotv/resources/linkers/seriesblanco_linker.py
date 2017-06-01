# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Linker SeriesBlanco para PalcoTV
# Version 0.5 (13/09/2016)
# Kodi Add-on by Juarrox (juarrox@gmail.com)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Librerías Plugintools por Jesús (www.mimediacenter.info)
#------------------------------------------------------------

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
from resources.lib import cloudflare
from resources.lib import client
from resources.lib import cache

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

thumbnail = "https://www.cubbyusercontent.com/pl/Seriesblanco_logo_palcotv.png/_85f9d7c45c8f4d90945d7d36d39afdcc"
fanart = "https://www.cubbyusercontent.com/pl/Seriesblanco_fondo_palcotv.jpg/_9d8cecfc268244ad8cb7fbed8b368af7" 

sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR seagreen]";ec3 = "[/COLOR]"
sc4 = "[COLOR red]";ec4 = "[/COLOR]"
sc5 = "[COLOR yellowgreen]";ec5 = "[/COLOR]"
version = " [0.5]"

referer = "http://seriesblanco.com" 

def seriesblanco_linker0(params):
    plugintools.log('[%s %s] Linker SeriesBlanco %s' % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker SeriesBlanco"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    
    url = params.get("url") 
    #headers = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'}
    #r = requests.get(url,headers=headers)
    #data = r.content
    data = cloudflare.request(url)
    print data
    fondo = plugintools.find_single_match(data, "<meta property='og:image' content='(.*?)'")
    if fondo == "": fondo = fanart
    logo = plugintools.find_single_match(data,"<img id='port_serie' src='([^']+)'")
    if logo == "": logo = thumbnail
    info = plugintools.find_single_match(data, "<img id='port_serie'(.*?)</tbody></table>")
    votos = plugintools.find_single_match(info,"color='yellow'>(.*?)<").strip()
    if votos =="": votos = "N/D"
    title_ser = plugintools.find_single_match(info, "<h4>(.*?)</h4>").decode('unicode_escape').encode('utf8').strip()
    if title_ser == "": title_ser = "N/D"
    genr = plugintools.find_single_match(info, "<font color='skyblue'>G.*?nero:</font></b>(.*?)<br>").decode('unicode_escape').encode('utf8').strip()
    if genr == "": genr = "N/D"
    prod_ser = plugintools.find_single_match(info, "color='skyblue'>Productora[^<]+</font></b>(.*?)<br>").decode('unicode_escape').encode('utf8').strip()
    if prod_ser == "": prod_ser = "N/D"
    pais_ser = plugintools.find_single_match(info, "color='skyblue'>Pa[^<]+</font></b>(.*?)<br>").decode('unicode_escape').encode('utf8').strip()
    if pais_ser == "": pais_ser = "N/D"
    time_ser = plugintools.find_single_match(info,"color='skyblue'>Duraci[^<]+</font></b>(.*?)<br>").decode('unicode_escape').encode('utf8').strip()
    if time_ser == "": time_ser = "N/D"
    temp = plugintools.find_multiple_matches(data, "<h2 style='cursor: hand; cursor: pointer;'>(.*?)</tbody></table>")
    n_temp = len(temp)
    sinopsis = plugintools.find_single_match(info,"<p>(.*?)</p>").decode('unicode_escape').encode('utf8')
    sinopsis = sinopsis.replace('<br/>','').replace('<br />','').replace('<br>','').strip()
    if sinopsis == "": sinopsis = "N/D"
    
    datamovie = {
    'season': sc3+'[B]Temporadas Disponibles: [/B]'+ec3+sc+str(n_temp)+', '+ec,
    'votes': sc3+'[B]Votos: [/B]'+ec3+sc+str(votos)+', '+ec,
    'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
    'studio': sc3+'[B]Productora: [/B]'+ec3+sc+str(prod_ser)+', '+ec,
    'duration': sc3+'[B]Duración: [/B]'+ec3+sc+str(time_ser)+'[CR]'+ec,
    'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
    
    datamovie["plot"]=datamovie["season"]+datamovie["votes"]+datamovie["genre"]+datamovie["studio"]+datamovie["duration"]+datamovie["sinopsis"]

    plugintools.add_item(action="",title=sc5+"[B]"+title_ser+"[/B]"+ec5,url="",info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    for item in temp:
        title_temp = plugintools.find_single_match(item, "<u>(.*?)</u></h2>").decode('unicode_escape').encode('utf8')
        cap_temp = plugintools.find_multiple_matches(item,"<tr><td>(.*?)</td>")
        plugintools.add_item(action="",title=sc2+'-- '+title_temp+' --'+ec2,url="",thumbnail=logo,info_labels=datamovie,plot=sinopsis,fanart=fondo,folder=False,isPlayable=False)
        for cap in cap_temp:
            url_cap = plugintools.find_single_match(cap, "<a href='([^']+)")
            url_cap = 'http://www.seriesblanco.com'+url_cap
            title_cap = plugintools.find_single_match(cap, "'>(.*?)</a>")
            plugintools.addPeli(action="seriesblanco_linker1",title=sc+title_cap+ec,url=url_cap,thumbnail=logo,info_labels=datamovie,plot=sinopsis,fanart=fondo,folder=True,isPlayable=False)
    
def seriesblanco_linker1(params):
    plugintools.log('[%s %s] Linker SeriesBlanco %s' % (addonName, addonVersion, repr(params)))

    sinopsis = params.get("plot")
    datamovie = {}
    datamovie["Plot"]=sinopsis

    thumbnail = params.get("thumbnail")
    fanart = params.get("fanart")  
    
    headers = {'Host':"seriesblanco.com","User-Agent": 'User-Agent=Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12', 
    "Referer": referer}
    url = params.get("url").replace('www.seriesblanco.com','seriesblanco.com')
    data = cloudflare.request(url)
    #r = requests.get(url,headers=headers)
    #data = r.content
    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker SeriesBlanco"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    ###### No hay peticion Ajax ######
    match_listacapis = plugintools.find_single_match(data,"<h2>Visionados Online</h2>(.*?)<h2>Descarga</h2>")
    ###### Si hay peticion Ajax ######
    if match_listacapis =="":
        ###### Buscando la url y datos del envio post a la peticion ajax ######
        ajax = plugintools.find_single_match(data,"function LoadGrid(.*?)success:")
        ajaxrequest = plugintools.find_single_match(ajax,"url : '(.*?)'.*?data : \"(.*?)\"")
        ###### Petición ajax ######
        url_ajax = scrapertools.cache_page(referer + ajaxrequest[0], ajaxrequest[1])
        custom_post=ajaxrequest[1]
        body,response_headers = plugintools.read_body_and_headers(referer+ajaxrequest[0],post=custom_post)
        #plugintools.log("data= "+data)
        match_listacapis = plugintools.find_single_match(body,'<h2>Visionados Online</h2>(.*?)</table>')

    match_capi = plugintools.find_multiple_matches(match_listacapis,'<td><div class="grid_content sno">(.*?)</tr>')
    
    for entry in match_capi:
        img = plugintools.find_single_match(entry,"src='/servidores([^']+)")
        url_img = 'http://www.seriesblanco.com/servidores'+img
        url_capi = plugintools.find_single_match(entry,'<a href="([^"]+)"')
        #url_capi = 'http://www.seriesblanco.com'+url_capi
        #Puede ser seriesblanco.tv o seriesblanco.com
        lang_audio = plugintools.find_single_match(entry,'<img src="http://seriesblanco.tv/banderas/([^"]+)"')
        if lang_audio =="": 
            lang_audio = plugintools.find_single_match(entry,'<img src="http://seriesblanco.com/banderas/([^"]+)"')
        if lang_audio.find("es.png") >= 0: lang_audio = "ESP"
        elif lang_audio.find("la.png") >= 0: lang_audio = "LAT"
        elif lang_audio.find("vos.png") >= 0: lang_audio = "V.O.S."
        elif lang_audio.find("vo.png") >= 0: lang_audio = "V.O."            
        
        url_server = plugintools.find_single_match(entry,"<img src='/servidores/([^']+)")
        url_server = url_server.replace(".png", "").replace(".jpg", "")
        quality = plugintools.find_single_match(entry,'src=\'/servidores/.*?<div class="grid_content sno">.*?<div class="grid_content sno"><span>(.*?)<')
        #if quality == "": quality = "undefined"
        server = video_analyzer(url_server)
        titlefull = params.get("title")+sc2+'[I] ['+lang_audio+'] [/I]'+ec2+sc5+'[I] ['+server+'][/I]  '+ec5+sc+'[I]'+quality+'[/I]'+ec
        ############### Tiene Redirección ###########################
        if 'enlacen' in url_capi:
            plugintools.addPeli(action="seriesblanco_liker2",title=titlefull,url=url_capi,info_labels=datamovie,thumbnail=url_img,fanart=fanart,folder=False,isPlayable=True)
        #############################################################    
        else:
            plugintools.addPeli(action=server,title=titlefull,url=url_capi,info_labels=datamovie,thumbnail=url_img,fanart=fanart,folder=False,isPlayable=True)

def seriesblanco_liker2(params):
    plugintools.log('[%s %s] Linker SeriesBlanco %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    url = 'http://seriesblanco.com'+url
    data = cloudflare.request(url)
    #referer = url
    #data = gethttp_referer_headers(url,referer)
    # onclick='window.open("http://allmyvideos.net/lh18cer7ut8r")
    url_final = plugintools.find_single_match(data, "onclick='window.open(.*?);'/>")
    url_final = url_final.replace('("', "").replace('")', "")
    params['url']=url_final; server_analyzer(params)
    
############################################# @ By PalcoTv Team #################################################
