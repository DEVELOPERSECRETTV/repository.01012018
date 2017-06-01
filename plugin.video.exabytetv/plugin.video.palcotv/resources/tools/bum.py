# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Buscador Unificado de Magnets para PalcoTV
# Version 0.2 (03.11.2015)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------


from __main__ import *
import ssl
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

class MyAdapter(HTTPAdapter):
 def init_poolmanager(self,connections,maxsize,block=False):
  self.poolmanager=PoolManager(num_pools=connections,maxsize=maxsize,block=block,ssl_version=ssl.PROTOCOL_TLSv1)
  
s=requests.Session();s.mount('https://',MyAdapter());s.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0'};

import os
import sys
import urllib
import urllib2
import re
import shutil
import zipfile
import time

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

from resources.lib.client import *
from resources.lib.cache import *
from resources.lib.cloudflare import *

import re,urllib,urllib2,sys
import plugintools,requests

from __main__ import *
from resources.tools.media_analyzer import launch_torrent
from resources.tools.media_analyzer import launch_magnet

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))
s=requests.Session();s.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Language':'es-ES,es;q=0.8,ro;q=0.6,en;q=0.4,gl;q=0.2','Accept-Encoding':'gzip, deflate, sdch','Connection':'keep-alive','Upgrade-Insecure-Requests':'1'};

thumbnail = 'http://static.myce.com/images_posts/2011/04/kickasstorrents-logo.jpg'
fanart = 'https://yuq.me/users/19/529/lcqO6hj0XK.png'
#fanart = 'http://2.bp.blogspot.com/_NP40rzexJsc/TMGWrixybJI/AAAAAAAAHCU/ij1--_DQEZo/s1600/Keep_Seeding____by_Carudo.jpg' 
show_bum = plugintools.get_setting("bum_id")

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

kurl=plugintools.get_setting("kurl")
bsurl=plugintools.get_setting("bsurl")
tdurl=plugintools.get_setting("tdurl")
lmurl=plugintools.get_setting("lmurl")
ihurl=plugintools.get_setting("ihurl")
tzurl=plugintools.get_setting("tzurl")
eturl=plugintools.get_setting("eturl")
#min_seeds=plugintools.get_setting("bum_seeds")

# Thumbnails
th_kat = 'https://lh5.ggpht.com/NAwFW7MJD2iYWAhH5si9BNhwy29P3_Lf6Le9cQGSTRkez_PR2DFKuumcTtGwiyOtXe0=w300'
th_torrentz = 'http://www.listoid.com/image/15/list_2_15_20101105_035751_725.gif'
th_bitsnoop = 'http://shoutmetech.com/wp-content/uploads/2014/11/bitsnoop_logo-150x150.png'
th_isohunt = 'http://news.softpedia.com/images/news2/IsoHunt-Tries-to-Go-Lite-and-Avoid-Takedown-2.jpg'
th_td = 'https://s5.mzstatic.com/us/r30/Purple30/v4/48/11/92/481192b4-c3ee-a49b-53ba-3682def8f5eb/icon128x128.jpeg'
th_tordls = 'http://www.royalranking.net/sites/default/files/styles/escala440x440/public/fotosranking/logotd.png?itok=VLooCSOA'
th_lime='https://torrentfreak.com/images/limetorrents.jpg'

def bum_multiparser(params):
    plugintools.log('[%s %s] Iniciando BUM+ ... %s' % (addonName, addonVersion, repr(params)))
    
    # Archivo de control de resultados
    bumfile = temp + 'bum.dat'
    if not os.path.isfile(bumfile):  # Si no existe el archivo de control, se crea y se anotan resultados de la búsqueda
        controlbum = open(bumfile, "wb")
        controlbum.close()    

    texto = parser_title(params.get("title"))
    texto = texto.replace("[Multiparser]", "").replace("[/COLOR]", "").replace("[I]", "").replace("[/I]", "").replace("[COLOR white]", "").replace("[COLOR lightyellow]", "").strip()
    lang = plugintools.get_setting("bum_lang")
    if lang == '0':
        lang = ""            
    elif lang == '1':
        lang = 'spanish'
    elif lang == '2':
        lang = 'english'
    elif lang == '3':
        lang = 'french'
    elif lang == '4':
        lang = 'german'
    elif lang == '5':
        lang = 'latino'

    if lang != "": texto = texto+' ' + lang
    else: texto=texto.strip()
    
    plugintools.set_setting("bum_search",texto)
    params["plot"]=parser_title(texto)
    texto = texto.lower().strip()
    texto = texto.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ", "n")
    if texto == "": errormsg = plugintools.message("PalcoTV","Por favor, introduzca el canal a buscar")
    else:
        url = kurl+'usearch/'+texto+'/'  # Kickass
        params["url"]=url            
        url = params.get("url")
        referer = 'http://www.kat.cr'
        kickass1_bum(params)
        url = bsurl+'search/all/'+texto+'/c/d/1/'  # BitSnoop
        params["url"]=url            
        url = params.get("url")
        referer = 'http://www.bitsnoop.com'
        bitsnoop1_bum(params)
        url = ihurl+'torrents/?ihq='+texto.replace(" ", "+").strip()+'&Torrent_sort=-seeders'  # Isohunt
        params["url"]=url            
        url = params.get("url")
        referer = 'https://isohunt.to'
        isohunt1_bum(params)        
        url = lmurl+'search/all/'+texto.replace(" ", "+").strip()+'/seeds/1/'
        params["url"]=url
        limetorrents1(params)
        
    controlbum = open(bumfile, "r")
    num_items = len(controlbum.readlines())
    fanart = 'http://wallpapercave.com/wp/hxV464E.png'

    i = -1
    controlbum.seek(0)
    while i <= num_items:        
        data = controlbum.readline()
        if data.startswith("EOF") == True:
            break
        elif data.startswith("Title") == True:
            title=data.replace("Title: ", "")
            url=controlbum.readline();url=url.replace("URL: ","")
            thumbnail=controlbum.readline();thumbnail=thumbnail.replace("Thumbnail: ", "").strip()
            seeds=controlbum.readline();seeds=seeds.replace("Seeds: ", "").replace(",", "").replace(".", "").strip()
            size=controlbum.readline();size=size.replace("Size: ", "").strip()
            seeds_min=plugintools.get_setting("bum_seeds");seeds_min=int(seeds_min)
            if seeds >= seeds_min:
                if thumbnail == "":
                    thumbnail = art + 'bum.png'                
                if title.find("[Kickass][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="launch_magnet", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    continue
                elif title.find("[BitSnoop][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="bitsnoop2_bum", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    continue
                elif title.find("[IsoHunt][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="isohunt2_bum", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    continue
                elif title.find("[LimeTorrents][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="limetorrents1", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    continue            
        else:
            i=i+1
            continue

    controlbum.close()
    xbmcplugin.addSortMethod(int(sys.argv[1]), 2)
    plugintools.setview(show_bum)

    # Eliminamos archivo de registro
    try:
        if os.path.exists(bumfile):
            os.remove(bumfile)
    except: pass
    
    #xbmc.executebuiltin("Container.SetViewMode(51)")


def bum_linker(params):
    plugintools.log('[%s %s] Iniciando BUM+ ... %s' % (addonName, addonVersion, repr(params)))

    texto=params.get("extra").split("_")[0].replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ", "n")    
    plugintools.set_setting("bum_search",texto)
    params["plot"]=texto
    url = kurl+'usearch/'+texto+'/'  # Kickass
    params["url"]=url.replace("https", "http")            
    url = params.get("url")
    referer = 'http://www.kat.cr'

    try:
        if plugintools.get_setting("bum_servers") == "true":  # Kickass
            if plugintools.get_setting("bum_kickass") == "true":
                plugintools.log("Ejecutando Kickass...")
                kickass1_bum(params)
        else: kickass1_bum(params)
    except: pass
    
    url = ihurl+'torrents/?ihq='+texto.replace(" ", "+")+'&Torrent_sort=-seeders'.strip()  # Isohunt
    params["url"]=url

    try:
      if plugintools.get_setting("bum_servers") == "true":
          if plugintools.get_setting("bum_isohunt") == "true":
              isohunt1_bum(params)
      else: isohunt1_bum(params)
    except: pass    
    
    
    url = lmurl+'search/all/'+texto.replace(" ", "+").strip()+'/seeds/1/'  #Limetorrents
    params["url"]=url
    
    try:
      if plugintools.get_setting("bum_servers") == "true":
        if plugintools.get_setting("bum_lime") == "true":
          limetorrents1(params)
      else: limetorrents1(params)
    except: pass    
    
    
    url = tdurl+'search/?search='+texto.replace(" ", "+").strip()  # Torrent Downloads
    params["url"]=url
    
    try:
        if plugintools.get_setting("bum_servers") == "true":
            if plugintools.get_setting("bum_tordls") == "true":
                tordls0(params)
        else: tordls0(params)
    except: pass        
        
    url = tzurl+'search?f='+texto.replace(" ", "+").strip()  #Torrentz.eu
    params["url"]=url
    
    try:
        if plugintools.get_setting("bum_servers") == "true":
            if plugintools.get_setting("bum_torrentz") == "true":
                torrentz0(params)
        else: torrentz0(params)
    except: pass

    texto=texto.split("_")[0].replace(" ", "+").strip()
    url = bsurl+'search/all/'+texto+'/c/d/1/'  # BitSnoop
    params["url"]=url

    try:
        if plugintools.get_setting("bum_servers") == "true":
            if plugintools.get_setting("bum_bitsnoop") == "true":
                bitsnoop1_bum(params)
        else: bitsnoop1_bum(params)
    except: pass
    
    texto=texto.split("_")[0].replace(" ", "+").strip()
    url = eturl+'busqueda/'+texto  # Elitetorrent
    params["url"]=url
    bumsv = plugintools.get_setting("bum_servers")
        
    if plugintools.get_setting("bum_servers") == "true":
        if plugintools.get_setting("bum_et") == "true":
            elite0_bum(params)
    else: elite0_bum(params)
    
    texto=texto.split("_")[0].replace(" ", "+").strip()
    url = "http://www.newpct1.com/index.php?page=buscar&q=%27" + texto + "%27&ordenar=Fecha&inon=Descendente"  # Newpct1
    params["url"]=url
    
    if plugintools.get_setting("bum_servers") == "true":
        if plugintools.get_setting("bum_newpct") == "true":
            newpct0_bum(params)
    else: newpct0_bum(params)

    xbmc.executebuiltin("Container.SetViewMode(51)")
    xbmcplugin.addSortMethod(int(sys.argv[1]), 2)

            
'''
    burl = 'http://www.elitetorrent.net/buscar.php?' + 'buscar='+texto+'&x=0&y=0'
    params["url"]=url
    params["extra"]=texto
    elite0_bum(params)
      
    controlbum = open(bumfile, "r")
    num_items = len(controlbum.readlines())
    fanart = 'http://wallpapercave.com/wp/hxV464E.png'

    i = -1
    controlbum.seek(0)
    while i <= num_items:        
        data = controlbum.readline()
        if data.startswith("EOF") == True:
            break
        elif data.startswith("Title") == True:
            title=data.replace("Title: ", "")
            url=controlbum.readline();url=url.replace("URL: ","")
            thumbnail=controlbum.readline();thumbnail=thumbnail.replace("Thumbnail: ", "").strip()
            seeds=controlbum.readline();seeds=seeds.replace("Seeds: ", "").replace(",", "").replace(".", "").strip()
            size=controlbum.readline();size=size.replace("Size: ", "").strip()
            seeds_min=plugintools.get_setting("bum_seeds");seeds_min=int(seeds_min)
            if seeds >= seeds_min:
                if thumbnail == "":
                    thumbnail = art + 'bum.png'                
                if title.find("[Kickass][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="launch_magnet", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    continue
                elif title.find("[BitSnoop][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="bitsnoop2_bum", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    continue
                elif title.find("[IsoHunt][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="isohunt2_bum", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    continue
                elif title.find("[LimeTorrents][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="limetorrents1", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    continue
                elif title.find("[Torrent Downloads][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="tordls1", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=True)
                    i=i+1
                    continue
                elif title.find("[Torrentz][/I][/COLOR]") >= 0:
                    plugintools.add_item(action="torrentz1", title=title, url=url, thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
                    i=i+1
                    continue                 
            else:
                i=i+1
                continue

    controlbum.close()

'''    




def kickass0_bum(params):
    plugintools.log('[%s %s] [BUM+] Kickass... %s' % (addonName, addonVersion, repr(params)))

    plugintools.setview(show_bum)    

    try:
        texto = params.get("plot");texto=parser_title(texto)        
        if texto == "":
            errormsg = plugintools.message("PalcoTV","Por favor, introduzca el canal a buscar")
        else:           
            texto = texto.lower().strip()
            url = kurl+'usearch/'+texto+'/'
            plugintools.log("URL Kickass= "+url)
            params["url"]=url            
            url = params.get("url")
            referer = 'http://www.kat.cr/'            
    except:
         pass      

    # Archivo de control de resultados (evita la recarga del cuadro de diálogo de búsqueda tras cierto tiempo)
    bumfile = temp + 'bum.dat'
    if not os.path.isfile(bumfile):  # Si no existe el archivo de control, se crea y se registra la búsqueda
        controlbum = open(bumfile, "a")
        controlbum.close()
        ahora = datetime.now()
        anno_actual = ahora.year
        mes_actual = ahora.month
        hora_actual = ahora.hour
        min_actual = ahora.minute
        seg_actual = ahora.second
        hoy = ahora.day
        # Si el día o mes está entre el 1 y 9, nos devuelve un sólo dígito, así que añadimos un 0 (cero) delante:
        if hoy <= 9:
            hoy = "0" + str(hoy)
        if mes_actual <= 9:
            mes_actual = "0" + str(ahora.month)
        timestamp = str(ahora.year) + str(mes_actual) + str(hoy) + str(hora_actual) + str(min_actual) + str(seg_actual)
        controlbum = open(temp + 'bum.dat', "a")
        controlbum.seek(0)
        controlbum.write(timestamp+":"+texto)
        controlbum.close()
    else:
        controlbum = open(temp + 'bum.dat', "r")
        controlbum.seek(0)
        data = controlbum.readline()
        controlbum.close()        
        plugintools.log("BUM+= "+data)           
        plugintools.log("Control de BUM+ activado. Analizamos timestamp...")
        data = data.split(":")
        timestamp = data[0]
        term_search = data[1]
        ahora = datetime.now()
        anno_actual = ahora.year
        mes_actual = ahora.month
        hora_actual = ahora.hour
        min_actual = ahora.minute
        seg_actual = ahora.second
        hoy = ahora.day
        # Si el día o mes está entre el 1 y 9, nos devuelve un sólo dígito, así que añadimos un 0 (cero) delante:
        if hoy <= 9:
            hoy = "0" + str(hoy)
        if mes_actual <= 9:
            mes_actual = "0" + str(ahora.month)
        timenow = str(ahora.year) + str(mes_actual) + str(hoy) + str(hora_actual) + str(min_actual) + str(seg_actual)
        # Comparamos valores (hora actual y el timestamp del archivo de control)
        if term_search == texto:
            result = int(timenow) - int(timestamp)
            if result > 90:  # Control fijado en 90 segundos; esto significa que una misma búsqueda no podremos realizarla en menos de 90 segundos, y en ese tiempo debe reproducirse el torrent
                # Borramos registro actual y guardamos el nuevo (crear una función que haga esto y no repetir!)
                ahora = datetime.now()
                anno_actual = ahora.year
                mes_actual = ahora.month
                hora_actual = ahora.hour
                min_actual = ahora.minute
                seg_actual = ahora.second
                hoy = ahora.day
                # Si el día o mes está entre el 1 y 9, nos devuelve un sólo dígito, así que añadimos un 0 (cero) delante:
                if hoy <= 9:
                    hoy = "0" + str(hoy)
                if mes_actual <= 9:
                    mes_actual = "0" + str(ahora.month)
                timestamp = str(ahora.year) + str(mes_actual) + str(hoy) + str(hora_actual) + str(min_actual) + str(seg_actual)
                controlbum = open(temp + 'bum.dat', "a")
                controlbum.seek(0)
                controlbum.write(timestamp+":"+texto)
                controlbum.close()                
                kickass_results(params)
            else:
                kickass_results(params)
        else:
            # Borramos registro actual y guardamos el nuevo (crear una función que haga esto y no repetir!)
            ahora = datetime.now()
            anno_actual = ahora.year
            mes_actual = ahora.month
            hora_actual = ahora.hour
            min_actual = ahora.minute
            seg_actual = ahora.second
            hoy = ahora.day
            # Si el día o mes está entre el 1 y 9, nos devuelve un sólo dígito, así que añadimos un 0 (cero) delante:
            if hoy <= 9:
                hoy = "0" + str(hoy)
            if mes_actual <= 9:
                mes_actual = "0" + str(ahora.month)
            timestamp = str(ahora.year) + str(mes_actual) + str(hoy) + str(hora_actual) + str(min_actual) + str(seg_actual)
            controlbum = open(temp + 'bum.dat', "a")
            controlbum.seek(0)
            controlbum.write(timestamp+":"+texto)
            controlbum.close()                
            kickass1_bum(params)

    #xbmc.executebuiltin("Container.SetViewMode(518)")
                
                
                
def kickass1_bum(params):
    plugintools.log('[%s %s] [BUM+] Kickass results... %s' % (addonName, addonVersion, repr(params)))

    url=params.get("url")
    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31", "Referer": kurl}    
    r=requests.get(url, headers=headers);data=r.content
    #thumbnail = 'http:'+plugintools.find_single_match(data, '<img src="([^"]+)')
    match_num_results = plugintools.find_single_match(data, '<div><h2>(.*?)</a></h2>')
    num_results = plugintools.find_single_match(match_num_results, '<span>(.*?)</span>')
    num_results = num_results.replace("from", "de").replace("results", "Resultados:").strip()
    results = plugintools.find_single_match(data, '<table width="100%" cellspacing="0" cellpadding="0" class="doublecelltable" id="mainSearchTable">(.*?)</table>')
    matches = plugintools.find_multiple_matches(results, '<div class="torrentname">(.*?)<a data-download')
    for entry in matches:
        match_title = plugintools.find_single_match(entry, 'class="cellMainLink">(.*?)</a>')
        match_title = match_title.replace("</strong>", "").replace("<strong>", "").replace('<strong class="red">', "").strip()
        magnet_match = 'magnet:'+plugintools.find_single_match(entry, "magnet:([^']+)").strip()
        size = plugintools.find_single_match(entry, 'class=\"nobr center\">(.*?)</td>')
        size = size.replace("<span>","").replace("</span>","").strip()
        seeds = plugintools.find_single_match(entry, '<td class="green center">(.*?)</td>').replace(",", "").replace(".", "")
        leechs = plugintools.find_single_match(entry, '<td class="red lasttd center">(.*?)</td>')
        title_fixed='[COLOR gold][I]['+seeds+'/'+leechs+'][/I][/COLOR] [COLOR white] '+match_title+' [I]['+size + '] [/COLOR][COLOR orange][Kickass][/I][/COLOR]'
        try: min_seeds=params.get("extra").split("_")[1];min_seeds=int(min_seeds)
        except: min_seeds=plugintools.get_setting("bum_seeds")
        if min_seeds == "":
            min_seeds=plugintools.get_setting("bum_seeds")         
        if match_title!= "" and size!="" and int(seeds)>=int(min_seeds):
            plugintools.addShow(action="launch_magnet", title=title_fixed, url=magnet_match, thumbnail=th_kat, fanart=fanart, folder=False, isPlayable=True)
        
                            

def bitsnoop0_bum(params):
    plugintools.log('[%s %s] [BUM+] BitSnoop... %s' % (addonName, addonVersion, repr(params)))

    plugintools.setview(show_bum)    

    try:
        texto = "";
        texto='riddick'
        texto = plugintools.keyboard_input(texto)
        plugintools.set_setting("alluc_search",texto)
        params["plot"]=texto
        texto = texto.lower()
        if texto == "":
            errormsg = plugintools.message("PalcoTV","Por favor, introduzca el canal a buscar")
            #return errormsg
        else:
            texto = texto.lower().strip()
            texto = texto.replace(" ", "+")
            
            # http://bitsnoop.com/search/all/the+strain+spanish/c/d/1/
            url = 'http://bitsnoop.com/search/all/'+texto+'/s/d/1/'
            params["url"]=url            
            url = params.get("url")
            referer = 'http://www.bitsnoop.com'
            bitsnoop1_bum(params)
    except:
         pass

def bitsnoop1_bum(params):
    plugintools.log('[%s %s] [BUM+] BitSnoop results... %s' % (addonName, addonVersion, repr(params)))
 
    thumbnail = 'http://upload.wikimedia.org/wikipedia/commons/9/97/Bitsnoop.com_logo.png'
    fanart = 'http://wallpoper.com/images/00/41/86/68/piracy_00418668.jpg'

    plugintools.setview(show_bum)
    url = params.get("url")
    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31", "Referer": "https://bitsnoop.com/"}
    r=requests.get(url, headers=headers);data=r.content
    results = plugintools.find_single_match(data, '<ol id="torrents" start="1">(.*?)</ol>')
    matches = plugintools.find_multiple_matches(results, '<span class="icon cat_(.*?)</div></td>')
    for entry in matches:
        page_url = plugintools.find_single_match(entry, 'a href="([^"]+)')
        title_url = plugintools.find_single_match(entry, 'a href="(.*?)</a>')
        title_url = title_url.replace(page_url, "").replace("<span class=srchHL>", "").replace('">', "").replace("<b class=srchHL>", "[COLOR white]").replace("</b>", "[/COLOR]").strip()
        page_url = 'http://bitsnoop.com'+page_url
        seeders = plugintools.find_single_match(entry, 'title="Seeders">(.*?)</span>').replace(",", "").replace(".", "")
        leechers = plugintools.find_single_match(entry, 'title="Leechers">(.*?)</span>')
        size = plugintools.find_single_match(entry, '<tr><td align="right" valign="middle" nowrap="nowrap">(.*?)<div class="nfiles">')
        if seeders == "": seeders = "0"
        if leechers == "": leechers = "0"            
        stats = '[COLOR gold][I]['+seeders+'/'+leechers+'][/I][/COLOR]'
        title_fixed=stats+'  [COLOR white]'+title_url+' [I]['+size+'] [/COLOR][COLOR red][BitSnoop][/I][/COLOR]'
        try:
            min_seeds=params.get("extra").split("_")[1];min_seeds=int(min_seeds)
            if min_seeds == "": min_seeds=plugintools.get_setting("bum_seeds")
        except: min_seeds=plugintools.get_setting("bum_seeds")      
        if title_url!= "" and size!="" and int(seeders)>=int(min_seeds):
            plugintools.addShow(action="bitsnoop2_bum", title=title_fixed, url=page_url, thumbnail=th_bitsnoop, fanart=fanart, folder=False, isPlayable=True)


def bitsnoop2_bum(params):
    plugintools.log('[%s %s] [BUM+] BitSnoop getlink... %s' % (addonName, addonVersion, repr(params)))
  
    url = params.get("url");r=requests.get(url);data=r.content
    magnet_match = 'magnet'+plugintools.find_single_match(data, '<a href="magnet([^"]+)').strip()
    plugintools.log("URL Magnet= "+magnet_match)
    params["url"]=magnet_match;launch_magnet(params)
   

def isohunt0_bum(params):
    plugintools.log('[%s %s] [BUM+] Isohunt... %s' % (addonName, addonVersion, repr(params)))

    thumbnail = 'http://www.userlogos.org/files/logos/dfordesmond/isohunt%201.png'
    fanart = 'http://2.bp.blogspot.com/_NP40rzexJsc/TMGWrixybJI/AAAAAAAAHCU/ij1--_DQEZo/s1600/Keep_Seeding____by_Carudo.jpg'    
   
    try:
        texto = "";
        texto='riddick'
        texto = plugintools.keyboard_input(texto)
        plugintools.set_setting("alluc_search",texto)
        params["plot"]=texto
        texto = texto.lower()
        if texto == "":
            errormsg = plugintools.message("PalcoTV","Por favor, introduzca el canal a buscar")
        else:
            texto = texto.lower().strip()
            texto = texto.replace(" ", "+")
            
            # https://isohunt.to/torrents/?ihq=the+strain+spanish
            url = 'https://isohunt.to/torrents/?ihq='+texto+'&Torrent_sort=seeders.desc'
            params["url"]=url            
            url = params.get("url")
            referer = 'https://isohunt.to'
            isohunt1_bum(params)
    except: pass

def isohunt1_bum(params):
    plugintools.log('[%s %s] [BUM+] Isohunt results... %s' % (addonName, addonVersion, repr(params)))
    plugintools.setview(show_bum)
    thumbnail = 'http://www.userlogos.org/files/logos/dfordesmond/isohunt%201.png'   

    # Abrimos archivo de registro
    url = params.get("url")
    data = cloudflare.request(url);#plugintools.log("data_cloudflare= "+data)    
    #headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31", "Referer": "https://isohunt.to/"}
    #r=requests.get(url, headers=headers);data=r.content
    matches = plugintools.find_multiple_matches(data, '<tr data-key="(.*?)</td></tr>')    
    for entry in matches:
        plugintools.log("entry= "+entry)
        page_url = plugintools.find_single_match(entry, '<a href="/([^"]+)')
        page_url = ihurl+page_url;plugintools.log("page_url="+page_url)
        title_url = plugintools.find_single_match(entry, '<span>(.*?)</span>').replace("\n", "").strip();plugintools.log("title_url="+title_url)
        size = plugintools.find_single_match(entry, '<td class="size-row">(.*?)</td>');plugintools.log("size="+size)
        seeds = plugintools.find_single_match(entry, '<td class="sy">(.*?)</td>').replace(",", "").replace(".", "");leechs = '?'
        plugintools.log("seeds="+seeds)
        if seeds == "": seeds = "0"
        category = plugintools.find_single_match(entry, 'title="([^"]+)')
        title_fixed='[COLOR gold][I]['+seeds+'/'+leechs+'][/I][/COLOR] [COLOR white] '+title_url+' [I]['+size+'] [/COLOR][COLOR lightblue][IsoHunt][/I][/COLOR]'
        try: min_seeds=params.get("extra").split("_")[1];min_seeds=int(min_seeds)
        except: min_seeds=plugintools.get_setting("bum_seeds")
        if min_seeds == "": min_seeds=plugintools.get_setting("bum_seeds");plugintools.log("min_seeds= "+min_seeds)
        else: plugintools.log("min_seeds= "+str(min_seeds))
        if title_url!= "" and size!="" and int(seeds)>=int(min_seeds):
            plugintools.addShow(action="isohunt2_bum", title=title_fixed, url=page_url, thumbnail=th_isohunt, folder=False, isPlayable=True)
        
def isohunt2_bum(params):
    plugintools.log('[%s %s] [BUM+] Isohunt getlink... %s' % (addonName, addonVersion, repr(params)))    
    plugintools.setview(show_bum)  
    url = params.get("url")
    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31", "Referer": "https://isohunt.to/"}
    r=requests.get(url, headers=headers);data=r.content
    magnet_match = plugintools.find_single_match(data, '<a href="magnet([^"]+)')
    magnet_match = 'magnet'+magnet_match.strip()
    params["url"]=magnet_match
    launch_magnet(params)

def monova0_bum(params):
    plugintools.log('[%s %s] [BUM+] Monova... %s' % (addonName, addonVersion, repr(params)))
    plugintools.setview(show)    
    thumbnail = 'http://upload.wikimedia.org/wikipedia/en/f/f4/Monova.jpg'
    fanart = 'http://www.gadgethelpline.com/wp-content/uploads/2013/10/Digital-Piracy.png'    
    plugintools.setview(show)
    
    try:
        texto = "";
        texto='the strain spanish'
        texto = plugintools.keyboard_input(texto)
        plugintools.set_setting("alluc_search",texto)
        params["plot"]=texto
        texto = texto.lower()
        if texto == "":
            errormsg = plugintools.message("PalcoTV","Por favor, introduzca el término a buscar")
            #return errormsg
        else:
            texto = texto.lower().strip()
            texto = texto.replace(" ", "+")
            
            # https://isohunt.to/torrents/?ihq=the+strain+spanish
            url = 'https://www.monova.org/search.php?sort=5&term='+texto+'&verified=1'
            params["url"]=url            
            url = params.get("url")
            referer = 'https://monova.org'
            monova1_bum(params)
    except: pass

def monova1_bum(params):
    plugintools.log('[%s %s] [BUM+] Monova results... %s' % (addonName, addonVersion, repr(params)))

    plugintools.setview(show_bum)    
    url = params.get("url")
    thumbnail = 'http://upload.wikimedia.org/wikipedia/en/f/f4/Monova.jpg'
    fanart = 'http://www.gadgethelpline.com/wp-content/uploads/2013/10/Digital-Piracy.png'    
    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31", "Referer": "https://www.monova.org/"}
    r=requests.get(url, headers=headers);data=r.content
    block_matches = plugintools.find_single_match(data, '<table id="resultsTable"(.*?)<div id="hh"></div>')
    plugintools.log("block_matches= "+block_matches)
    matches = plugintools.find_multiple_matches(block_matches, '<div class="torrentname(.*?)</div></td></tr>')
    for entry in matches:
        if entry.find("Direct Download") >= 0:  # Descartamos resultados publicitarios 'Direct Download' que descargan un .exe
            plugintools.log("Direct Download = Yes")
        else:
            plugintools.log("Direct Download = No")
            page_url = plugintools.find_single_match(entry, 'a href="([^"]+)')
            title_url = plugintools.find_single_match(entry, 'title="([^"]+)')
            size_url = plugintools.find_single_match(entry, '<div class="td-div-right pt1">(.*?)</div>')
            seeds = plugintools.find_single_match(entry, '<td class="d">(.*?)<td align="right" id="encoded-').replace(",", "").replace(".", "")
            seeds = seeds.replace("</td>", "")
            seeds = seeds.split('<td class="d">')
            #seeds = seeds.replace('<td align="right" id="encoded-10"', "")
            #seeds = seeds.replace('<td id="encoded-10" align="right"', "")
            try:
                if len(seeds) >= 2:
                    semillas = '[COLOR gold][I]['+seeds[0]+'/'+seeds[1]+'][/I][/COLOR]'
            except:
                pass        

            plugintools.add_item(action="monova2_bum", title = semillas+'  '+title_url+' [COLOR lightgreen][I][ '+size_url+'][/I][/COLOR] ', url = page_url , thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = True)

    #xbmc.executebuiltin("Container.SetViewMode(518)")
            
            

def monova2_bum(params):
    plugintools.log('[%s %s] [BUM+] Monova getlink... %s' % (addonName, addonVersion, repr(params)))
    plugintools.setview(show_bum) 
    url = params.get("url")    
    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31", "Referer": "https://www.monova.org/"}
    r=requests.get(url, headers=headers);data=r.content    
    magnet_match = plugintools.find_single_match(data, '<a href="magnet([^"]+)')
    magnet_match = 'magnet'+magnet_match
    params["url"]=magnet_match
    launch_magnet(params)
    #xbmc.executebuiltin("Container.SetViewMode(518)")
    

def limetorrents0_bum(params):
    plugintools.log('[%s %s] [BUM+] Monova... %s' % (addonName, addonVersion, repr(params)))
    thumbnail = 'http://upload.wikimedia.org/wikipedia/en/f/f4/Monova.jpg'
    fanart = 'http://www.gadgethelpline.com/wp-content/uploads/2013/10/Digital-Piracy.png'    
    
    try:
        texto = "";
        texto='the strain spanish'
        texto = plugintools.keyboard_input(texto)
        plugintools.set_setting("alluc_search",texto)
        params["plot"]=texto
        texto = texto.lower()
        if texto == "":
            errormsg = plugintools.message("PalcoTV","Por favor, introduzca el término a buscar")
            #return errormsg
        else:
            texto = texto.lower().strip()
            texto = texto.replace(" ", "+")
            
            # https://isohunt.to/torrents/?ihq=the+strain+spanish
            url = 'https://www.limetorrents.cc/search/all/'+texto.replace(" ", "+").strip()+'/seeds/1/'
            params["url"]=url            
            limetorrents1_bum(params)
    except:
         pass
    #xbmc.executebuiltin("Container.SetViewMode(518)")

def limetorrents1(params):
    plugintools.log('[%s %s] [BUM+] LimeTorrents loading... %s' % (addonName, addonVersion, repr(params)))
    url=params.get("url").replace("https", "http");plugintools.log("url= "+url)
    lmurl=plugintools.get_setting("lmurl")
    s=requests.Session();s.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0','Referer': lmurl, 'CF-RAY': '2e2fe16361375492-MAD'};
    b=s.get(lmurl.replace("https", "http"), headers=s.headers, allow_redirects=False);data=b.text;plugintools.log("data_prev= "+data)
    cookies=s.cookies;data=b.text;plugintools.log("data= "+data)
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0', 'Referer': lmurl}
    for cook in cookies:
        plugintools.log("cook= "+str(cook))
        s.headers.update({cook.name:cook.value})        
    r=requests.get(url, headers=headers, allow_redirects=False);data=r.text;plugintools.log("data= "+data)
    results = plugintools.find_single_match(data, 'Search results for(.*?)</ol>');plugintools.log("results= "+results)
    matches = plugintools.find_multiple_matches(results, '<span class="icon cat_video"(.*?)</div></li>')
    for entry in matches:
        plugintools.log("entry= "+entry)
        if entry.find("Verified") >= 0:
            page_url = burl + plugintools.find_single_match(entry, '<a href="([^"]+)')
            match_title = plugintools.find_single_match(entry, '.html">([^<]+)')
            seeds = plugintools.find_single_match(entry, '<span class="seeders" title="Seeders">(.*?)</span>').replace(",", "").replace(".", "");plugintools.log("seeds= "+seeds)
            leechs = plugintools.find_single_match(entry, '<td class="tdleech">(.*?)</td>').replace(",", "").replace(".", "")
            size = plugintools.find_single_match(entry, '</a></td><td class="tdnormal">(.*?)B</td>')+'B'            
            title_fixed='[COLOR gold][I]['+seeds+'/'+leechs+'][/I][/COLOR] [COLOR white] '+match_title+' [I]['+size + '] [/COLOR][COLOR lime][LimeTorrents][/I][/COLOR]'
            plugintools.addShow(action="tordls1", title=title_fixed, url=page_url, thumbnail=th_lime, folder=False, isPlayable=True)   
 

def pbay0(params):
    plugintools.log('[%s %s] [BUM+] Pirate Bay... %s' % (addonName, addonVersion, repr(params)))
    thumbnail=params['thumbnail'];fanart=params.get("fanart");cookie=''
    url='https://thepiratebay.cr/search/Super%20Rugby/0/7/0'
    s=requests.Session();s.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0', 'Referer': "https://thepiratebay.cr/"}
    b=s.get(url, verify=False)
    resp=b.text;heads=b.headers;cook=b.cookies;print cook
    for cookies in cook:cookie+=cookies.name+'='+cookies.value+'; ';
    s.headers.update({'Cookie':cookie})
    print cookie
    if cookie:
        print resp.encode('utf-8','ignore')

def tordls0(params):
    plugintools.log('[%s %s] [BUM+] Torrent Downloads... %s' % (addonName, addonVersion, repr(params)))
    thumbnail=params['thumbnail'];fanart=params.get("fanart");
    burl_tordls = params.get("url").replace("https://", "http://")
    data = cloudflare.request(burl_tordls);plugintools.log("data_cloudflare= "+data)    
    
    data=resp.encode('utf-8','ignore');plugintools.log("data= "+data)
    items=plugintools.find_multiple_matches(data, '<div class="grey_bar3"><p>(.*?)</span></div>')
    for entry in items:
        page_url = tdurl + plugintools.find_single_match(entry, 'href="([^"]+)')
        title=plugintools.find_single_match(entry, 'title="View torrent info :(.*?)">')
        thumbnail='http://www.spainjapanyear.com/templates/new/images/logo.png'
        try:
            seeds=plugintools.find_multiple_matches(entry, '<span>(.*?)</span>')[1].replace("&nbsp;", "").strip()
            leechs=plugintools.find_multiple_matches(entry, '<span>(.*?)</span>')[0].replace("&nbsp;", "").strip()
            size=plugintools.find_multiple_matches(entry, '<span>(.*?)</span>')[2].replace("&nbsp;", "").strip()
        except: seeds="0";leechs="0";size="0"
        if title!= "":
            title_fixed=title+" "+seeds+"/"+leechs+" ("+size+")"
            title_fixed='[COLOR gold][I]['+seeds+'/'+leechs+'][/I][/COLOR] [COLOR white] '+title+' [I]['+size + '] [/COLOR][COLOR lightgreen][Torrent Downloads][/I][/COLOR]'
            try: min_seeds=params.get("extra").split("_")[1];min_seeds=int(min_seeds)
            except: min_seeds=plugintools.get_setting("bum_seeds")
            if min_seeds == "":
                min_seeds=plugintools.get_setting("bum_seeds")
            if title!= "" and size!="" and int(seeds)>=int(min_seeds):
                plugintools.addShow(action="tordls1", title=title_fixed, url=page_url, thumbnail=th_tordls, folder=False, isPlayable=True)   

def tordls1(params):
    plugintools.log('[%s %s] [BUM+] Torrent Downloads... %s' % (addonName, addonVersion, repr(params)))

    url=params.get("url")
    data = cloudflare.request(url);#plugintools.log("data_cloudflare= "+data)    
    c=requests.Session();c.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0', 'Referer': "https://www.torrentdownloads.me/"}
    b=c.get(url, headers=c.headers, allow_redirects=False);cookie=''
    resp=b.text;heads=b.headers;cook=b.cookies;print cook
    for cookies in cook:
        cookie+=cookies.name+'='+cookies.value+'; ';c.headers.update({'Cookie':cookie});print cookie
    if cookie:
        data=resp.encode('utf-8','ignore');print data
        bloque_url=plugintools.find_single_match(data, '<span>Magnet:(.*?)</a></p></div>');url=plugintools.find_single_match(bloque_url, 'href="([^"]+)').strip()
        plugintools.log("URL Magnet= "+url)
        params["url"]=url
        launch_magnet(params)


def torrentz0(params):
    plugintools.log('[%s %s] [BUM+] Torrentz.eu... %s' % (addonName, addonVersion, repr(params)))
    thumbnail=params['thumbnail'];fanart=params.get("fanart");headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0', 'Referer': tzurl}
    url = params.get("url")
    data = cloudflare.request(url);#plugintools.log("data_cloudflare= "+data)    
   
    '''
    r=requests.get(url, headers=headers, allow_redirects=False);resp=r.content;data=resp.encode('utf-8','ignore');cook=s.cookies;plugintools.log("data= "+data)
    for cookies in cook:
        cookie+=cookies.name+'='+cookies.value+'; ';s.headers.update({'Cookie':cookie});print cookie
    '''
    items=plugintools.find_multiple_matches(data, '<dl>(.*?)</dl>')
    for entry in items:
        #plugintools.log("entry= "+entry)
        page_url = tzurl + plugintools.find_single_match(entry, 'href=\/([^>]+)')
        plugintools.log("page_url= "+page_url)
        title=plugintools.find_single_match(entry, '<a href[^>]+>(.*?)</dt>').replace("<b>", "").replace("</b>", "").replace("<strong>", "").replace("</strong>", "").replace("<a>", "").replace("</a>", "").split("&#187;")[0].strip()
        #plugintools.log("title= "+title)
        try:
            pattern=entry.split("<dd")[1]
            stats=plugintools.find_multiple_matches(pattern, '<span>(.*?)</span>')
            size=stats[1];seeds=stats[2].replace(",", "").strip();leechs=stats[3] 
        except: seeds="0";leechs="0";size="0"
        try: min_seeds=params.get("extra").split("_")[1];min_seeds=int(min_seeds)
        except: min_seeds=plugintools.get_setting("bum_seeds")
        if min_seeds == "":
            min_seeds=plugintools.get_setting("bum_seeds")  
        #plugintools.log("size= "+size)
        #plugintools.log("seeds= "+str(seeds))
        #plugintools.log("min_seeds= "+str(min_seeds))
        if title!= "" and size!="" and int(seeds)>=int(min_seeds):
            title_fixed=title+" "+seeds+"/"+leechs+" ("+size+")"
            title_fixed='[COLOR gold][I]['+str(seeds).strip()+'/'+leechs+'][/I][/COLOR] [COLOR white] '+title+' [I]['+size+'] [/COLOR][COLOR yellow][Torrentz][/I][/COLOR]'
            if seeds > 0:
                plugintools.addDir(action="torrentz1", title=title_fixed, url=page_url, thumbnail=th_torrentz, folder=True, isPlayable=False)  

              
def torrentz1(params):
    plugintools.log('[%s %s] [BUM+] Torrentz.eu... %s' % (addonName, addonVersion, repr(params)))    
    url=params.get("url")
    data = cloudflare.request(url);#plugintools.log("data_cloudflare= "+data)    
    title,dls=plugintools.find_single_match(data, '<h2><span>(.*?)</span>(.*?)</h2>')
    plugintools.log("title= "+title)
    plugintools.log("dls= "+dls)
    results=plugintools.find_single_match(data, '<div class=download>(.*?)</p></div>')
    items=plugintools.find_multiple_matches(results, '<dl><dt>(.*?)</span></dd></dl>')
    #plugintools.add_item(action="", title='[COLOR white]'+title+' [/COLOR]', thumbnail=th_torrentz, folder=False, isPlayable=False)
    plugintools.add_item(action="", title='[COLOR lightgreen][I]'+dls.strip()+'[/I][/COLOR]', thumbnail=th_torrentz, folder=False, isPlayable=False) 
    for item in items:
        url_item= plugintools.find_single_match(item, 'href="([^"]+)').replace(" ", "+").strip()
        server= plugintools.find_single_match(item, '<span class=u([^<]+)').replace(">", "").strip();server=' [COLOR lightyellow][I]['+server+'][/I][/COLOR]'
        added =  plugintools.find_single_match(item, '<span title="([^\n]+)').split(">")[1];plugintools.log("url_item= "+url_item)
        if url_item.find("bitsnoop") >= 0:
            server=' [COLOR lightyellow][I][BitSnoop][/I][/COLOR]'
            action='bitsnoop2_bum'
            thumb=th_bitsnoop
        elif url_item.find("kat.cr") >= 0:
            server=' [COLOR lightyellow][I][KickAss][/I][/COLOR]'
            action='kickass2'
            thumb=th_kat
        elif url_item.find("isohunt") >= 0:
            server=' [COLOR lightyellow][I][IsoHunt][/I][/COLOR]'
            action='isohunt2_bum'
            thumb=th_isohunt
        elif url_item.find("torrentdownloads") >= 0:
            server=' [COLOR lightyellow][I][TorrentDownloads][/I][/COLOR]'
            action='tordls1'
            thumb=th_td
        elif url_item.find("torrentproject") >= 0:
            server=' [COLOR lightyellow][I][TorrentProject][/I][/COLOR]'
            action='torproject0'
            thumb='https://www.tvaddons.ag/kodi-addons/cache/images/b6d53416393beec63377eaeacbaf54_icon.png'
        elif url_item.find("limetorrents") >= 0:
            server=' [COLOR lightyellow][I][LimeTorrents][/I][/COLOR]'
            action='torproject0'
            thumb='http://www.synoboost.com/images/logolimetorrents.png'
        elif url_item.find("extratorrent") >= 0:
            server=' [COLOR lightyellow][I][ExtraTorrent][/I][/COLOR]'
            action='torproject0'
            thumb='https://addons.cdn.mozilla.net/user-media/addon_icons/50/50378-64.png?modified=1353802944'            
        elif url_item.find("torlock") >= 0:
            server=' [COLOR lightyellow][I][Torlock][/I][/COLOR]'
            action='kickass2'
            thumb='https://www.tvaddons.ag/kodi-addons/cache/images/003f0c4fe18bce6b2483e430368d3f_icon.png'
        elif url_item.find("rarbg") >= 0:
            server=' [COLOR lightyellow][I][RARBG][/I][/COLOR]'
            action='torproject0'
            thumb='http://bgtorrentz.net/wp-content/uploads/2015/04/rarbg.png'            
        elif url_item.find("torrentreactor") >= 0:
            server=' [COLOR lightyellow][I][TorrentReactor][/I][/COLOR]'
            action='kickass2'
            thumb='http://globaldownloadlinks.com/wp-content/uploads/2013/10/TorrentReactor-Logo.png'
        else:
            action='torproject0'
            if server.find("monova") >= 0: thumb="http://fileplenty.com/custom_templates/monovva/img/logo.png"
            elif server.find("idope") >= 0: thumb="https://d2.alternativeto.net/dist/icons/torlock_90325.png?width=64&height=64&mode=crop&upscale=false"
            elif server.find("torrentfunk") >= 0: thumb="http://d2.alternativeto.net/dist/icons/torrentfunk_90327.png?width=64&height=64&mode=crop&upscale=false"
            elif server.find("rarbg") >= 0: thumb="http://ftp.acc.umu.se/mirror/addons.superrepo.org/v7/addons/plugin.video.rarbg.tv/icon.png"
            elif server.find("rutracker") >= 0: thumb="https://lh3.googleusercontent.com/qKLAeN2NeG_DKdzn_aPVqyq28p8Y8Weh3gK3hevwply4VGLAHnBhsksOwGrg13jnqw=w170"
            else: thumb='http://www.apkcube.com/wp-content/uploads/2015/02/EZ-Downloader-Torrent-apk-images-logo-150x150.png'            

        if server != "" and action!="":
            plugintools.add_item(action=action, title='[COLOR white]'+title+'[/COLOR]'+server, url=url_item.replace("https", "http"), thumbnail=thumb, page=server, fanart='http://wallpaperswa.com/thumbnails/detail/20120405/minimalistic%20text%20humor%20yotsuba%20torrent%20crying%20anime%20girls%201920x1080%20wallpaper_www.wallpaperwa.com_16.jpg', folder=False, isPlayable=True)
                                          
    xbmc.executebuiltin("Container.SetViewMode(51)")
    #bloque_url=plugintools.find_single_match(data, '<span>Magnet:(.*?)</a></p></div>');url=plugintools.find_single_match(bloque_url, 'href="([^"]+)').strip()
    #plugintools.log("URL Magnet= "+url)
    #params["url"]=url
    #launch_magnet(params)        

def kickass2(params):
    plugintools.log('[%s %s] [BUM+] Torrentz > Kickass/Torlock ... %s' % (addonName, addonVersion, repr(params)))
    
    url=params.get("url").replace("https://", "http://")
    request_headers=[]
    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31", "Referer": kurl}
    r=requests.get(url, headers=headers);data=r.content;plugintools.log("data= "+data)
    url = 'magnet:'+plugintools.find_single_match(data, 'magnet:([^"]+)').strip()
    plugintools.log("URL Magnet= "+url)
    params["url"]=url
    launch_magnet(params)

def torproject0(params):
    plugintools.log('[%s %s] [BUM+] Torrentz > TorrentProject ... %s' % (addonName, addonVersion, repr(params)))
    url=params.get("url");server=params.get("page");plugintools.log("server= "+server)
    url=url.replace("https://", "http://").strip();url=url.replace(" ", "+").strip()
    data = cloudflare.request(url);#plugintools.log("data_cloudflare= "+data)
    if server.find("idope") >= 0 or server.find("torrentcore") >= 0 or server.find("btstor") >= 0 or server.find("monova") >= 0 or server.find("rutracker") >= 0:
      url = 'magnet:'+plugintools.find_single_match(data, 'magnet:([^"]+)').replace("amp;", "")
    else: url = 'magnet:'+plugintools.find_single_match(data, "magnet:([^']+)").replace("amp;", "")
    
    if server.find("unknown") >= 0:
      url=urllib.quote_plus(url).strip()
    plugintools.log("URL Magnet= "+url)
    params["url"]=url
    launch_magnet(params)    

    
def elite0_bum(params):
    plugintools.log("[%s %s] Elitetorrent búsquedas %s " % (addonName, addonVersion, repr(params)))
    url = params.get("url");#plugintools.log("Elitetorrent búsqueda= "+url)
    headers = {"Referer": 'http://www.elitetorrent.net/', "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0", "Connection": "keep-alive"}
    data = {"buscar": params.get("extra"), "x": '0', "y": '0'}
    r=requests.post(url, data=data);data=r.content
    results = plugintools.find_multiple_matches(data, '<li>(.*?)</li>')
    for entry in results:
        if entry.find("loco-bingo-1.html") >= 0:
            pass
        else:                
            title_torrent = plugintools.find_single_match(entry, 'title="([^"]+)')
            url_torrent = plugintools.find_single_match(entry, '<a href="([^"]+)')
            url_torrent = 'http://www.elitetorrent.net'+url_torrent
            age = plugintools.find_single_match(entry, '<span class="fecha">(.*?)</span>')
            nota = plugintools.find_single_match(entry, 'title="Valoracion media">([^<]+)')
            quality = plugintools.find_single_match(entry, '<span class="voto2"[^>]+>([^<]+)')
            thumb = 'http://www.elitetorrent.net/'+plugintools.find_single_match(entry, 'src="([^"]+)')
            if nota == "": nota = "N/D"
            if quality == "": quality = "N/D"
            title_fixed='[COLOR gold][I][0/0][/I][/COLOR] [COLOR white] '+title_torrent+' [I]['+quality+'] [/COLOR][COLOR yellow][Elitetorrent][/I][/COLOR]'
            plugintools.addPeli(action="elite2", title=title_fixed,url=url_torrent,thumbnail=thumb,fanart=fanart,folder=False, isPlayable=True)           

def newpct0_bum(params):
    plugintools.log("[%s %s] Newpct búsquedas %s " % (addonName, addonVersion, repr(params)))
    url=params.get("url")
    #plugintools.log("url= "+url)
    data=requests.get(url).content;#plugintools.log("data= "+data)
    contador = plugintools.find_single_match(data, "\( (.*?) \)")
    bloque = plugintools.find_single_match(data, '<ul class="buscar-list">(.*?)</ul>')
    lista = plugintools.find_multiple_matches(bloque, '<li>(.*?)</li>')
    for item in lista:
      #plugintools.log("item= "+item)
      enlace = plugintools.find_single_match(item, '<a href="(.*?)"')
      poster = plugintools.find_single_match(item,'<img src="(.*?)"')
      titulot = plugintools.find_single_match(item,'<h2 style="padding:0;">(.*?)</h2>').decode('unicode_escape').encode('utf8')
      titulo = cleantags(titulot)
      try: quality="["+titulo.split("[")[1]
      except: quality=""
      title_fixed='[COLOR gold][I][0/0][/I][/COLOR] [COLOR white] '+titulo+' [I]'+quality+' [/COLOR][COLOR green][Newpct][/I][/COLOR]'
      #plugintools.log("title_fixed= "+title_fixed)
      #plugintools.log("enlace= "+enlace)
      if enlace.startswith("http://www.newpct1.com/pelicula/") == True or enlace.startswith("http://www.newpct1.com/peliculas/") == True:
        plugintools.addPeli(action="newpct1_peli_torrent", title=title_fixed, url=enlace, thumbnail=poster, fanart='http://i.imgur.com/2N0hWm4.jpg', folder=False, isPlayable=True)

# Funciones auxiliares para dar un formato homogéneo 
def screenTitle(nombre, logo, fondo): plugintools.add_item(action="", title=h1(nombre), url="", thumbnail=logo, fanart=fondo, folder=False, isPlayable=False)

def formatext(texto,color,tipo):
	if tipo == "italic" : texto = "[I]"+texto+"[/I]"
	elif tipo == "bold" : texto = "[B]"+texto+"[/B]"
	if color != "" : texto = "[COLOR "+color.lower()+"]"+texto+"[/COLOR]"
	return texto

def cleantext(txt):
	z=0;ZMAX=20;ni=txt.find("[");nf=txt.find("]")
	while (ni!=-1 and nf!=-1) and z<ZMAX :
		txt = txt[:ni]+txt[nf+1:]
		#plugintools.log(">>>Iteración ("+str(z)+") [Ni:Nf] = ["+str(ni)+":"+str(nf)+"] Texto:"+txt)
		ni=txt.find("[");nf=txt.find("]");z+=1
	return txt.strip()

def cleantags(txt):
	z=0;ZMAX=20;ni=txt.find("<");nf=txt.find(">")
	while (ni!=-1 and nf!=-1) and z<ZMAX :
		txt = txt[:ni]+txt[nf+1:]
		#plugintools.log(">>>Iteración ("+str(z)+") [Ni:Nf] = ["+str(ni)+":"+str(nf)+"] Texto:"+txt)
		ni=txt.find("<");nf=txt.find(">");z+=1
	return txt.strip()

def h1(texto): return formatext(texto, "yellow", "bold")      #título de pantalla
def h2(texto): return formatext(texto, "lightblue", "bold")   #categorías
def h3(texto): return formatext(texto, "lightblue", "")       #películas
def h4(texto): return formatext(texto, "darkseagreen", "")     #series
def h5(texto): return formatext(texto, "deepskyblue", "")     
def h6(texto): return formatext(texto, "steelblue", "")       #calidad #idioma pelis
def h7(texto): return formatext(texto, "red", "")     #warning
def h8(texto): return formatext(texto, "steelblue", "italic") #links de paginación
def h9(texto): return formatext(texto, "gray", "italic")      #firma
	
