# -*- coding: utf-8 -*-
#-------------------------------------------------------------------
# PalcoTV - Kodi Add-on by Juarrox (juarrox@gmail.com)
# Version 0.3.6 (23.09.2016)
#-------------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#-------------------------------------------------------------------
# Gracias a la librerías y tutoriales de Jesús (mimediacenter.info)
# Gracias a Reig, Aquilesserr, V1k1ng0, Madquark y Quequino
#-------------------------------------------------------------------

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

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

art = xbmc.translatePath(os.path.join(addonPath+'/art', ''))
temp = xbmc.translatePath(os.path.join('special://home/userdata/playlists/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/userdata/playlists', ''))
cbx_pages = xbmc.translatePath(os.path.join(addonPath+'/art/cbx', ''))
addons = xbmc.translatePath(os.path.join('special://home/addons/', ''))
libdir = xbmc.translatePath(os.path.join('special://xbmc/system/players/dvdplayer/', ''))
tools = xbmc.translatePath(os.path.join(addonPath+'/resources/tools', ''))
resources = xbmc.translatePath(os.path.join(addonPath+'/resources', ''))
icons = xbmc.translatePath(os.path.join(addonPath+'/art/icons', ''))
libs = xbmc.translatePath(os.path.join(addonPath+'/resources/lib', ''))
ruta_llamadas = xbmc.translatePath(os.path.join('special://home/userdata/'+addonId+'/llamadas/', ''))
biblio = xbmc.translatePath(os.path.join('special://userdata/addon_data/'+addonId+'/library', ''))
biblio_cine = xbmc.translatePath(os.path.join(biblio+'/CINE', ''))
biblio_series = xbmc.translatePath(os.path.join(biblio+'/SERIES', ''))
sys.path.append (libs)

profile=xbmcaddon.Addon().getAddonInfo('profile').decode('utf-8')
cookiefile=profile+'cookies.dat'
for i in ('resources','tools','libs','playlists','temp','art'): sys.path.append(os.path.join(addonId,i))

selfAddon = xbmcaddon.Addon()

import plugintools
import png
import locale
import time
import random

# Scraper eldorado
try: from xbmcswift2 import Plugin
except: pass

icon = art + 'icon.png'
fanart = 'fanart.jpg'

#------------------------------------------------------------
# PalcoTV
#------------------------------------------------------------

# Regex de canales
from resources.regex.vaughnlive import *
from resources.regex.ninestream import *
from resources.regex.vercosas import *
from resources.regex.castalba import *
from resources.regex.castdos import *
from resources.regex.directwatch import *
from resources.regex.freetvcast import *
from resources.regex.freebroadcast import *
from resources.regex.sawlive import *
from resources.regex.broadcastlive import *
from resources.regex.businessapp import *
from resources.regex.rdmcast import *
from resources.regex.dinozap import *
from resources.regex.streamingfreetv import *
from resources.regex.byetv import *
from resources.regex.ezcast import *
from resources.regex.ucaster import *
from resources.regex.iguide import *
from resources.regex.miplayernet import *

# Regex de pelis y series
from resources.linkers.seriesblanco_linker import *
from resources.linkers.seriesflv_linker import *
from resources.linkers.seriesadicto_linker import *
from resources.linkers.seriesyonkis_linker import *
from resources.linkers.seriesmu_linker import *
from resources.linkers.oranline_linker import *
from resources.linkers.cineclasico_linker import *
from resources.linkers.pordede_linker import *
from resources.linkers.pelisadicto_linker import *
from resources.linkers.tvvip_linker import *
from resources.linkers.hdfull_linker import *
from resources.linkers.danko_linker import *
from resources.linkers.inkapelis_linker import *
from resources.linkers.peliculasdk_linker import *
from resources.linkers.jkanime_linker import *
from resources.linkers.animeflv_linker import *
from resources.linkers.reyanime_linker import *

# Herramientas
from framescrape import *
from resources.tools.oranline import *
from resources.tools.telefivegb import *
from resources.tools.ondacadiz import *
from resources.tools.arena_dmax import *
from resources.tools.tumarcador import *
from resources.tools.canalcocina import *
from resources.tools.epg_miguiatv import *
from resources.tools.epg_arenasport import *
from resources.tools.epg_formulatv import *
from resources.tools.epg_elmundo import *
from resources.tools.epg_verahora import *
from resources.tools.epg_entutele import *
from resources.tools.dailymotion import *
from resources.tools.yt_playlist import *
from resources.tools.goear import *
from resources.tools.mundoplus import *
from resources.tools.bers_sy import *
from resources.tools.server_rtmp import *
from resources.tools.txt_reader import *
from resources.tools.loadtxt_ftv import *
from resources.tools.epg_txt import *
from resources.tools.agendatv import *
from resources.tools.futbolenlatv import *
from resources.tools.context import *
from resources.tools.livesoccertv import *
from resources.tools.msg import *
from resources.tools.nstream import *
from resources.tools.net import *
from resources.tools.scraperx import *
from resources.tools.logreader import *
from resources.tools.fpa import *
from resources.tools.library_manager import *
from resources.tools.ivoox import *

#
from resources.tools.multilink import *
from resources.tools.media_analyzer import *
from resources.tools.skinutils import *
from resources.tools.resolvers import *
from resources.tools.bum import *
from resources.tools.updater import *



# Punto de entrada
def run():
    plugintools.log('[%s %s] Running %s... ' % (addonName, addonVersion, addonName))

    # Obteniendo parámetros...
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        url = params.get("url")
        exec action+"(params)"
    
    if not os.path.exists(playlists) :
        os.makedirs(playlists)

    if not os.path.exists(temp) :
        os.makedirs(temp)

    if not os.path.exists(biblio) :
        os.makedirs(biblio)
        
    if not os.path.exists(biblio_cine):
        os.makedirs(biblio_cine)
        
    if not os.path.exists(biblio_series):
        os.makedirs(biblio_series)            

    if not os.path.exists(ruta_llamadas) :
        os.makedirs(ruta_llamadas)

    plugintools.close_item_list()           
        

# Main menu
def main_list(params):
    plugintools.log('[%s %s].main_list %s' % (addonName, addonVersion, repr(params)))

    # Control del skin de PalcoTV
    load_skin=params.get("extra")
    if load_skin != "load_skin":
        mastermenu = xml_skin()
    else:
        mastermenu = params.get("url")
    plugintools.log("XML menu: "+mastermenu)
    try:
        data = plugintools.read(mastermenu)
    except:
        mastermenu = 'http://pastebin.com/raw.php?i=ydUjKXnN'
        data = plugintools.read(mastermenu)
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "XML no reconocido...", 3 , art+'icon.png'))

    matches = plugintools.find_multiple_matches(data,'<menu_info>(.*?)</menu_info>')
    datamovie={}
    for entry in matches:
        title = plugintools.find_single_match(entry,'<title>(.*?)</title>')
        date = plugintools.find_single_match(entry,'<date>(.*?)</date>')
        thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
        fanart = plugintools.find_single_match(entry,'<fanart>(.*?)</fanart>')
        datamovie["Plot"] = plugintools.find_single_match(entry,'<info>(.*?)</info>')
        plugintools.add_item( action="" , title = title + date , fanart = fanart , info_labels=datamovie, thumbnail=thumbnail , folder = False , isPlayable = False )

    data = plugintools.read(mastermenu);datamovie = {}
    matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</channel>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
        thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
        fanart = plugintools.find_single_match(entry,'<fanart>(.*?)</fanart>')
        action = plugintools.find_single_match(entry,'<action>(.*?)</action>')
        datamovie["plot"] = plugintools.find_single_match(entry,'<desc>(.*?)</desc>')
        url = plugintools.find_single_match(entry,'<url>(.*?)</url>')
        selex = plugintools.find_single_match(entry,'<selector>(.*?)</url>')  # Ojo! Si es un selector de opciones hay que ponerlo antes de <url>...</url>
        adult_mode = plugintools.get_setting("adult_mode")  # Control paternal
        if selex == "yes": 
            plugintools.add_item( action="xml_selec" , title='[COLOR white]' + title + '[/COLOR]' , url=url , thumbnail=thumbnail , info_labels=datamovie, fanart=fanart , folder = False , isPlayable = False )                    

        elif adult_mode == "false" :        
            if title.find("Adultos") >= 0 :
                plugintools.log("Activando control paternal...")
            else:        
                fixed = title
                plugintools.log("fixed= "+fixed)
                if url.startswith("plugin") == True:
                    plugintools.addDir( action = action , plot = fixed , title = '[COLOR lightblue]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , info_labels = datamovie, url = url , folder = False , isPlayable = False )            
                elif url.startswith("pvr://") == True:
                    plugintools.add_item( action="runPlugin" , title=title+" pvr" , url=url , thumbnail=thumbnail , fanart=fanart , folder = False , isPlayable = False )
                elif parser_title(fixed) == "Actualizaciones":
                    # Ejecutando actualizador...
                    plugintools.log("Ejecutando actualizador...")
                    updater = plugintools.get_params();updater["thumbnail"]=thumbnail;updater["fanart"]=fanart;updater["url"]=url;updater["plot"]=fixed;updater["action"]=action;updater["title"]=title;check_update(updater)
                    #plugintools.addDir( action = action , plot = fixed , title = '[COLOR lightblue]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , info_labels = datamovie, url = url , folder = True , isPlayable = False )
                elif fixed == 'Agenda TV':
                    plugintools.addDir( action = action , plot = fixed , title = '[COLOR lightblue]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , info_labels = datamovie, folder = True , isPlayable = False )
                else:
                    plugintools.addDir( action = action , plot = fixed , title = '[COLOR white]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , info_labels = datamovie, folder = True , isPlayable = False )
        else:
            fixed = title
            if url.startswith("plugin") == True:
                plugintools.addDir( action = action , plot = fixed , title = '[COLOR lightblue]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , info_labels = datamovie, url = url , folder = False , isPlayable = False )
            elif url.startswith("pvr://") == True:
                plugintools.add_item( action="runPlugin" , title=title+" pvr" , url=url , thumbnail=thumbnail , fanart=fanart , folder = False , isPlayable = False )                
            elif parser_title(fixed) == "Actualizaciones":
                # Ejecutando actualizador...
                try:
                    plugintools.log("Ejecutando actualizador...")
                    updater = plugintools.get_params();updater["thumbnail"]=thumbnail;updater["fanart"]=fanart;updater["url"]=url;updater["plot"]=fixed;updater["action"]=action;updater["title"]=title;check_update(updater)
                except: pass
            elif fixed == "Agenda TV":
                plugintools.addDir( action = action , plot = fixed , title = '[COLOR lightblue]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , info_labels = datamovie, folder = True , isPlayable = False )
            else:
                plugintools.addDir( action = action , plot = fixed , title = '[COLOR white]' + fixed + '[/COLOR]' , fanart = fanart , thumbnail = thumbnail , url = url , info_labels = datamovie, folder = True , isPlayable = False )


def play(params):
    plugintools.log('[%s %s].play %s' % (addonName, addonVersion, repr(params)))
    url = params.get("url")
    plugintools.log("URL= "+url)
    plugintools.play_resolved_url(url)


def runPlugin(params):
    plugintools.log('[%s %s] runPlugin %s' % (addonName, addonVersion, repr(params)))
    
    url = params.get("url")
    if url.startswith("pvr://") == True:
        #url = "pvr://channels/tv/Todos los canales/pvr.demo_2.pvr"
        builtin = "PlayMedia(%s)" %url
        xbmc.executebuiltin(builtin)     
    elif url.startswith("plugin://plugin.video.live.streamspro/") == True:        
        builtin = 'Container.Update(%s)' %url
        xbmc.executebuiltin(builtin)
    elif url.startswith("plugin://plugin.video.phstreams") == True:        
        plugintools.runAddon(url)   
    elif url.startswith("plugin://plugin.video.live.plexus-streams") == True:        
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)      
    elif url.startswith("plugin://plugin") == False:
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    elif url.startswith("plugin://plugin.video.youtube") == True:
        xbmc.executebuiltin('XBMC.RunPlugin('+url+')')
    else:
        builtin = 'RunPlugin(%s)' %url
        xbmc.executebuiltin(builtin)   
    


def live_items_withlink(params):
    plugintools.log('[%s %s].live_items_withlink %s' % (addonName, addonVersion, repr(params)))
    data = plugintools.read(params.get("url"))

    # ToDo: Agregar función lectura de cabecera (fanart, thumbnail, título, últ. actualización)
    header_xml(params)

    fanart = plugintools.find_single_match(data, '<fanart>(.*?)</fanart>')  # Localizamos fanart de la lista
    if fanart == "":
        fanart = art + 'fanart.jpg'

    author = plugintools.find_single_match(data, '<poster>(.*?)</poster>')  # Localizamos autor de la lista (encabezado)

    matches = plugintools.find_multiple_matches(data,'<item>(.*?)</item>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<title>(.*?)</title>')
        title = title.replace("<![CDATA[", "")
        title = title.replace("]]>", "")
        thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
        url = plugintools.find_single_match(entry,'<link>(.*?)</link>')
        url = url.replace("<![CDATA[", "")
        url = url.replace("]]>", "")
        plugintools.add_item(action = "play" , title = title , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

def xml_selec(params):
    data = plugintools.read( params.get("url") )
    title_selex = params.get("title")
    name_channel = parser_title(title_selex)
    data = plugintools.find_single_match(data, '<name>'+name_channel+'(.*?)</channel>');plugintools.log("data= "+data)
    options = plugintools.find_multiple_matches(data, '<option>(.*?)</option>')
    selex_options=[];selex_urls=[];selex_actions=[]
    for entry in options:
        #plugintools.log("entry= "+entry)        
        title = plugintools.find_single_match(entry, '<name>([^<]+)</name>');selex_options.append(title)
        action = plugintools.find_single_match(entry, '<action>([^<]+)</action>');selex_actions.append(action)
        url = plugintools.find_single_match(entry, '<url>([^<]+)');selex_urls.append(url)
        
    selectorxml(title_selex, selex_options, selex_urls, selex_actions) 
    

def xml_lists(params):
    plugintools.log('[%s %s].xml_lists %s' % (addonName, addonVersion, repr(params)))
    data = plugintools.read( params.get("url") )
    name_channel = params.get("title")
    name_channel = parser_title(name_channel)
    data = plugintools.find_single_match(data, '<name>'+name_channel+'(.*?)</channel>')
    thumbnail=params.get("thumbnail");fanart=params.get("fanart")
    plugintools.add_item(action="" , title='[B][COLOR yellow]'+name_channel+'[/B][/COLOR]' , thumbnail= thumbnail , fanart = fanart , folder = False , isPlayable = False )

    datamovie = {}
    adult_mode = plugintools.get_setting("adult_mode")  # Control paternal
    subchannel = plugintools.find_multiple_matches(data, '<subchannel>(.*?)</subchannel>')
    for entry in subchannel:
        #plugintools.log("entry= "+entry)        
        title = plugintools.find_single_match(entry, '<name>([^<]+)')
        url = plugintools.find_single_match(entry, '<url>([^<]+)')
        thumbnail = plugintools.find_single_match(entry, '<thumbnail>([^<]+)')
        fanart = plugintools.find_single_match(entry, '<fanart>([^<]+)')
        action = plugintools.find_single_match(entry, '<action>([^<]+)')
        action = plugintools.find_single_match(entry, '<action>([^<]+)</action>')
        datamovie["Plot"] = plugintools.find_single_match(entry, '<desc>(.*?)</desc>')    
        selex = plugintools.find_single_match(entry,'<selector>(.*?)</selector>')
        if selex == "yes":
            plugintools.add_item( action="xml_selec" , title='[COLOR white]' + title + '[/COLOR]' , url=url , thumbnail=thumbnail , info_labels=datamovie, fanart=fanart , folder = False , isPlayable = False )               
    
        elif adult_mode == "true" :  # Modo adultos ON
            if action == "runPlugin":
                plugintools.add_item( action = action , title = title , url= url , thumbnail = thumbnail , fanart = fanart , info_labels = datamovie, extra = url , page = url , folder = True , isPlayable = False )
            else:
                plugintools.addDir( action = action , title = title , url= url , thumbnail = thumbnail , fanart = fanart , info_labels = datamovie, extra = url , page = url , folder = True , isPlayable = False )
        else:
            if title.find("XXX") >= 0 :
                plugintools.log("Control parental: "+title)
            else:
                if action == "runPlugin":
                    plugintools.add_item( action = action , title = title , url= url , thumbnail = thumbnail , fanart = fanart , info_labels = datamovie, extra = url , page = url , folder = True , isPlayable = False )
                else:
                    plugintools.addDir( action = action , title = title , url= url , thumbnail = thumbnail , fanart = fanart , info_labels = datamovie, extra = url , page = url , folder = True , isPlayable = False )

def getstreams_now(params):
    plugintools.log('[%s %s].getstreams_now %s' % (addonName, addonVersion, repr(params)))

    data = plugintools.read( params.get("url") )
    poster = plugintools.find_single_match(data, '<poster>(.*?)</poster>')
    plugintools.add_item(action="" , title='[COLOR blue][B]'+poster+'[/B][/COLOR]', url="", folder =False, isPlayable=False)
    matches = plugintools.find_multiple_matches(data,'<title>(.*?)</link>')

    for entry in matches:
        title = plugintools.find_single_match(entry,'(.*?)</title>')
        url = plugintools.find_single_match(entry,'<link> ([^<]+)')
        plugintools.add_item( action="play" , title=title , url=url , folder = False , isPlayable = True )



# Soporte de listas de canales por categorías (Livestreams, XBMC México, Motor SportsTV, etc.).

def livestreams_channels(params):
    plugintools.log('[%s %s].livestreams_channels %s' % (addonName, addonVersion, repr(params)))
    data = plugintools.read( params.get("url") )

    # Extract directory list
    thumbnail = params.get("thumbnail")

    if thumbnail == "":
        thumbnail = 'icon.jpg'
        plugintools.log(thumbnail)
    else:
        plugintools.log(thumbnail)

    if thumbnail == art + 'icon.png':
        matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</items>')
        for entry in matches:
            title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
            thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
            fanart = plugintools.find_single_match(entry,'<fanart>(.*?)</fanart>')
            plugintools.add_item( action="livestreams_subchannels" , title=title , url=params.get("url") , thumbnail=thumbnail , fanart=fanart , folder = True , isPlayable = False )

    else:
        matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</items>')
        for entry in matches:
            title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
            thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
            fanart = plugintools.find_single_match(entry,'<fanart>(.*?)</fanart>')
            plugintools.add_item( action="livestreams_items" , title=title , url=params.get("url") , fanart=fanart , thumbnail=thumbnail , folder = True , isPlayable = False )


def livestreams_subchannels(params):
    plugintools.log('[%s %s].livestreams_subchannels %s' % (addonName, addonVersion, repr(params)))

    data = plugintools.read( params.get("url") )
    # title_channel = params.get("title")
    title_channel = params.get("title")
    name_subchannel = '<name>'+title_channel+'</name>'
    data = plugintools.find_single_match(data, name_subchannel+'(.*?)</channel>')
    info = plugintools.find_single_match(data, '<info>(.*?)</info>')
    title = params.get("title")
    plugintools.add_item( action="" , title='[B]'+title+'[/B] [COLOR yellow]'+info+'[/COLOR]' , folder = False , isPlayable = False )

    subchannel = plugintools.find_multiple_matches(data , '<name>(.*?)</name>')
    for entry in subchannel:
        plugintools.add_item( action="livestreams_subitems" , title=entry , url=params.get("url") , thumbnail=art+'motorsports-xbmc.jpg' , folder = True , isPlayable = False )


# Pendiente de cargar thumbnail personalizado y fanart...
def livestreams_subitems(params):
    plugintools.log('[%s %s].livestreams_subitems %s' % (addonName, addonVersion, repr(params)))

    title_subchannel = params.get("title")
    data = plugintools.read( params.get("url") )
    source = plugintools.find_single_match(data , title_subchannel+'(.*?)<subchannel>')

    titles = re.compile('<title>([^<]+)</title>([^<]+)<link>([^<]+)</link>').findall(source)
    url = params.get("url")
    title = params.get("title")
    thumbnail = params.get("thumbnail")

    for entry, quirry, winy in titles:
        winy = winy.replace("amp;","")
        plugintools.add_item( action="play" , title = entry , url = winy , thumbnail = thumbnail , folder = False , isPlayable = True )


def livestreams_items(params):
    plugintools.log('[%s %s].livestreams_items %s' % (addonName, addonVersion, repr(params)))

    title_subchannel = params.get("title")
    title_subchannel_fixed = title_subchannel.replace("Ã±", "ñ")
    title_subchannel_fixed = title_subchannel_fixed.replace("\\xc3\\xb1", "ñ")
    title_subchannel_fixed = plugintools.find_single_match(title_subchannel_fixed, '([^[]+)')
    title_subchannel_fixed = title_subchannel_fixed.encode('utf-8', 'ignore')
    plugintools.log("subcanal= "+title_subchannel_fixed)
    if title_subchannel_fixed.find("+") >= 0:
        title_subchannel_fixed = title_subchannel_fixed.split("+")
        title_subchannel_fixed = title_subchannel_fixed[1]
        title_subchannel_fixxed = title_subchannel_fixed[0]
        if title_subchannel_fixed == "":
            title_subchannel_fixed = title_subchannel_fixxed

    data = plugintools.read( params.get("url") )
    source = plugintools.find_single_match(data , title_subchannel_fixed+'(.*?)</channel>')
    plugintools.log("source= "+source)
    fanart_channel = plugintools.find_single_match(source, '<fanart>(.*?)</fanart>')
    titles = re.compile('<title>([^<]+)</title>([^<]+)<link>([^<]+)</link>([^<]+)<thumbnail>([^<]+)</thumbnail>').findall(source)

    url = params.get("url")
    title = params.get("title")
    thumbnail = params.get("thumbnail")

    for entry, quirry, winy, xiry, miry in titles:
        winy = winy.replace("amp;","")
        plugintools.add_item( action="play" , title = entry , url = winy , thumbnail = miry , fanart = fanart_channel , folder = False , isPlayable = True )


def xml_items(params):
    plugintools.log('[%s %s].xml_items %s' % (addonName, addonVersion, repr(params)))
    data = plugintools.read( params.get("url") )
    thumbnail = params.get("thumbnail")

    #Todo: Implementar una variable que permita seleccionar qué tipo de parseo hacer
    if thumbnail == "title_link.png":
        matches = plugintools.find_multiple_matches(data,'<item>(.*?)</item>')
        for entry in matches:
            title = plugintools.find_single_match(entry,'<title>(.*?)</title>')
            thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
            url = plugintools.find_single_match(entry,'<link>([^<]+)</link>')
            fanart = plugintools.find_single_match(entry,'<fanart>([^<]+)</fanart>')
            plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )

    if thumbnail == "name_rtmp.png":
        matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</channel>')
        for entry in matches:
            title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
            url = plugintools.find_single_match(entry,'<rtmp>([^<]+)</rtmp>')
            plugintools.add_item( action = "play" , title = title , url = url , fanart = art + 'fanart.jpg' , plot = title , folder = False , isPlayable = True )


def m3u_reader(params):
    plugintools.log('[%s %s] M3U Reader: %s' % (addonName, addonVersion, repr(params)))

    title_pager = params.get("title");plot_pager = params.get("plot")  # Paginación M3U: minitem; Primer elemento a mostrar, maxm3u = Intervalo de paginación
    trailer_id = "";pitems=0;maxm3u=0;interval=0

    # Paginación de listas M3U
    if plugintools.get_setting("pager_m3u") == "true":
        minitem=params.get("page");maxm3u=plugintools.get_setting("maxm3u")
        if params.get("ext") == "pag":
            minitem=params.get("page")
        else: minitem=0            
    else: minitem=0;maxm3u=9999 # A definir más adelante minitem, maxm3u
    plugintools.log('Aplicando paginación limitada a un máximo de %s entradas desde el elemento %s ' % (str(maxm3u), str(minitem)))
    
    saving_url = 0  # Interruptor para scraper de pelis
    datamovie = {}  # Creamos lista de datos película
    filtros_on = plugintools.get_setting("fpa_on")  # Filtros activos?
    
    logo = ""; background = ""; contents=""; imdb_id = ""

    # Obtenemos fanart y thumbnail del diccionario
    thumbnail = params.get("thumbnail")
    if thumbnail == "" :
        thumbnail = art + 'icon.png'

    # Parche para solucionar un bug por el cuál el diccionario params no retorna la variable fanart
    fanart = params.get("extra")
    if fanart == " " :
        fanart = params.get("fanart")
        if fanart == " " :
            fanart = art + 'fanart.png'
        
    title = params.get("plot")
    texto= params.get("texto")
    busqueda = ""
    if title == 'search':
        title = title + '.txt'        
    else:
        title = title + '.m3u'

    title = parser_title(params.get("title")).strip()
    ext = params.get("ext")
    title_plot = params.get("plot")
    if title_plot == "":
        filename = title + "." + ext
        plugintools.log("filename no title_plot= "+filename)
    elif int(maxm3u)!="":
        filename = params.get("plot").strip()+'.m3u'
        plugintools.log("filename in page= "+filename)        
    elif ext is None:
        filename = title
        plugintools.log("filename no ext= "+filename)
    else:
        filename = title + "." + ext          
    
    file = open(playlists + filename, "r")
    file.seek(0)
    v = file.readlines()
    file.seek(0)
    data = file.readline().decode('unicode_escape').encode('utf8')
    data=data.replace("\xef", "").replace("\xbb", "").replace("\xbf", "").replace("\n", "")
	
    while data == "":  # Fixed by DMO: Para dar compatibilidad con algunas listas m3u que tienen 1 o mas de 1 líneas en blanco al comienzo, antes del "EXTM3U"
        file.seek(0)
        data = file.readline()	
    
    if data.find("EXTM3U") >= 0:  # Control modo de vista
        data = data.split(",")
        for item in data:
            if item.startswith("contents") == True:
                contents = item.replace("contents:", "")
                plugintools.log("CONTENTS= "+contents)
            if "background" in item:
                background = item.replace("background=", "").replace('"',"").strip()
                plugintools.log("background= "+background)
                if background: fanart = background
            if "logo" in item:
                logo = item.replace("logo=", "").replace('"',"").strip()
                plugintools.log("logo= "+logo)
                if logo != "": thumbnail = logo
            
    if data == "":
        data = file.readline()        
    else:
        file.seek(0)
        num_items = len(file.readlines())
        plugintools.log("num_items= "+str(num_items))
        no_head = plugintools.get_setting("no_head")
        if no_head == "false":
            plugintools.add_item(action="" , title = '[COLOR lightyellow][B][I]playlists / '+ filename + '[/B][/I][/COLOR]' , url = playlists + title , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = False)
            
    cat = ""  # Control para evitar error en búsquedas (cat is null)   
    plot = " "   # Control canal sin EPG (plot is null)
    file.seek(0)
    data = file.readline()
            
    i = 0
    while i <= num_items:
        if minitem == 0:
            if int(pitems)<=int(maxm3u): interval=1
        else:
            interval=0
            if int(pitems)>=int(minitem): interval=1  # Interruptor para mostrar elementos en Kodi            
       
        if int(maxm3u)+int(minitem) <= int(pitems):  # Se rompe bucle al hallar el último elemento del intervalo
            plugintools.addDir(action="m3u_reader", title="[COLOR lightyellow][I]Siguiente[/I][/COLOR]", url=params.get("url"), plot=filename.replace(".m3u", "").strip(), thumbnail=params.get("thumbnail"), fanart=params.get("fanart"), page=str(int(minitem)+int(maxm3u)), ext="pag", folder=True, isPlayable=False);break
           
        if data == "\n":
            data=file.readline()            
        if data.replace(" ","").startswith("#EXTINF:-1") == True or data.replace(" ","").startswith("#EXTINF:1") == True or data.replace(" ","").startswith("#EXTINF:0") == True :  # Fixed by DMO: Soporte de listas con cualquier dígito tras #EXTINF y sin coma
            pitems+=1
            title = data.replace("#EXTINF:-1", "").replace("#EXTINF:1", "").replace("#EXTINF:0", "").replace("-AZBOX *", "").replace("-AZBOX-*", "").replace("tvg-shift=0", "").replace("tvg-shift=-5", "").strip()
            if title.startswith(",$") == True:  # Control para lanzar scraper IMDB
                title = title.replace("$","")
                images = m3u_items(title)
                title_fixed = images[3]
                datamovie = {}
                datamovie = scraperfilm(title_fixed)
                save_title(title_fixed, datamovie, filename)
                getdatafilm = 1  # Control para cargar datos de película
                saving_url = 1  # Control para guardar URL
                if datamovie == {}:
                    title = '[COLOR lightyellow][B]'+title+' - [/B][I][COLOR orange][IMDB: [B]'+datamovie["rating"]+'[/B]][/I][/COLOR] '
                    thumbnail = datamovie["poster"]
                    if datamovie["fanart"] != "":
                        fanart = datamovie["fanart"]

            images = m3u_items(title)
            thumbnail = images[0]
            if images[1] != "":
                fanart = images[1]
            cat = images[2]
            title = images[3]
            # Recopilamos datos de película en diccionario
            datamovie["rating"] = images[6]  # Ranking IMDB
            datamovie["duration"] = images[7]  # Duración
            datamovie["year"] = images[8]  # Año
            datamovie["director"] = images[9]  # Director
            datamovie["writer"]=images[10]  # Escritor(es)
            datamovie["genre"]=images[11]  # Géneros
            datamovie["votes"]=images[12]  # Votos
            datamovie["plot"]=images[13]  # Plot (sinopsis)
            datamovie["trailer_id"]=images[15]  # ID Youtube Trailer
            datamovie["imdb_id"]=images[16]  # ID IMDB
            datamovie["photoset"]=images[17]  # Photoset
            datamovie["tagline"]=images[14]  # Cast
            datamovie["cast"]=images[14].split(", ")  # Cast
            total_cast=images[14]  
            typemedia=images[15]
            try: trailer_id=images[15]
            except: trailer_id = ""
            try: imdb_id=images[16]
            except: imdb_id = ""            
            origen = title.split(",")                
            title = title.strip()
            data = file.readline()

            # Control para thumbnail y fanart global (logo y background)
            if logo != "":  # Existe logo global
                if thumbnail == art + 'icon.png':
                    thumbnail = logo
                else:
                    thumbnail = images[0]
                    
            if images[1] != "fanart.jpg":
                if images[1] != "":
                    fanart = images[1]                    
            elif background != "":
                plugintools.log("fanart= "+fanart)
                fanart = background  # Existe background global
            else:
                fanart = 'fanart.jpg'

            # Analizando título...
            plugintools.log("TÍTULO= "+title)
            if title.startswith("##") == True:  # Control para el canal #0
                title=title.replace("##", "#")
            elif title.startswith("#@#") == True:  # Control para el canal #0 con EPG
                title=title.replace("#@#", "@#")
            elif title.startswith("#") == True:  # Control para comentarios
                title = title.replace("#", "");plugintools.log("print titulo= "+title)
                plugintools.addDir(action="", title = title , url = "", thumbnail = thumbnail , info_labels = datamovie, fanart = fanart , folder = False , isPlayable = False)
                continue

            if title.startswith("@") == True:  # Control para lanzar EPG
                if plugintools.get_setting("epg_no") == "true":
                    title = title.replace("@","")                    
                    plugintools.log('[%s %s] EPG desactivado ' % (addonName, addonVersion))
                else:
                    title = title.replace("@","")
                    epg_channel = []
                    epg_source = plugintools.get_setting("epg_source")                    
                    if epg_source == "0":  # MiguíaTV
                        epg_channel = epg_now(title)
                        try:
                            title = title + " [COLOR orange][I][B] " + epg_channel[0] + "[/B] " + epg_channel[1] + "[/I][/COLOR] "
                            plot = "[COLOR white][I]" + epg_channel[2].strip() + " " + epg_channel[3].strip() + "[CR]"+ epg_channel[4].strip() + " " + epg_channel[5].strip()+"[CR]"+ epg_channel[6].strip() + " " + epg_channel[7].strip()+"[CR]"+ epg_channel[8].strip() + " " + epg_channel[9].strip()+"[/I][/COLOR] "
                            datamovie["plot"]=plot
                        except: plot = ""
                    elif epg_source == "6":  # P2P Sports
                        epg_channel = epg_arena(title)
                        try:
                            title = title + " [COLOR orange][I][B] " + epg_channel[0] + "[/B] " + epg_channel[1] + "[/I][/COLOR] "
                            if len(epg_channel)==4: plot = "[COLOR white][I]" + epg_channel[2].strip() + " " + epg_channel[3].strip() + "[CR]"+ epg_channel[4].strip() + " " + epg_channel[5].strip()+"[/I][/COLOR] "
                            if len(epg_channel)==6: plot = "[COLOR white][I]" + epg_channel[2].strip() + " " + epg_channel[3].strip() + "[CR]"+ epg_channel[4].strip() + " " + epg_channel[5].strip()+"[/I][/COLOR] "
                            datamovie["plot"]=plot
                            plugintools.log("epg_channel= "+epg_channel[0])
                            plugintools.log("epg_channel= "+epg_channel[1])
                        except: plot = ""                                                                              
                    else:  # FórmulaTV General | FTV Movistar+ | FTV Telecable | FTV Ono | FTV Jazztel
                        epg_channel = epg_ftv(title)                        
                        if epg_channel != "":
                            try:
                                ejemplo = epg_channel[0]
                                title = title + " [COLOR orange][I][B] " + epg_channel[0] + "[/B] " + epg_channel[1] + "[/I][/COLOR] "
                                plot = "[COLOR white]" + epg_channel[2].strip() + " " + epg_channel[4].strip() + " [/COLOR][COLOR lightyellow][I]("+epg_channel[3].strip() + ")[/I][/COLOR][CR]" + epg_channel[5].strip()+" "+ epg_channel[6].strip()
                                datamovie["plot"]=plot
                            except: plot = ""
                    
            if title.startswith(' $ExtFilter="') == True:  # Control para determinadas listas de decos sat
                title = title.replace('$ExtFilter="', "")
                category = title.split('"')
                tipo = category[0]
                tipo = tipo.strip()
                title = category[1]
                title = title.strip()
                data = file.readline()

            if cat!="": title='[COLOR red][I]' + cat + ' /  [/I][/COLOR][COLOR white]'+title+'[/COLOR]'  # Con categoría de canales (listas M3U)
                    
            if data != "":  # Iniciamos análisis de la URL...
                url = data.strip();plugintools.log("Analizando URL... "+url)
                if url.startswith("llamada") == True:  # Fixed by DMO: Soporte de sintaxis simplificada para listas con llamadas a otros addons
                    url_analyzer(title, datamovie, thumbnail, fanart, plot, url)
                    data = file.readline();i = i + 1;continue 
                    
                if url == "#multi" or url == "#multilink":
                    photoset=datamovie["photoset"].split("$")
                    capturas=len(photoset)
                    if capturas==4:
                        photoa=photoset[0];photob=photoset[1];photoc=photoset[2];photod=photoset[3];datamovie["photod"]=photod
                    elif capturas==3:
                        photoa=photoset[0];photob=photoset[1];photoc=photoset[2];photod="http://bichosrunners.com/wp-content/uploads/2014/12/no-photo.png"
                    elif capturas==2:
                        photoa=photoset[0];photob=photoset[1];photoc="http://bichosrunners.com/wp-content/uploads/2014/12/no-photo.png";photod="http://bichosrunners.com/wp-content/uploads/2014/12/no-photo.png"
                    elif capturas==1:
                        photoa=photoset[0];photob="http://bichosrunners.com/wp-content/uploads/2014/12/no-photo.png";photoc="http://bichosrunners.com/wp-content/uploads/2014/12/no-photo.png";photod="http://bichosrunners.com/wp-content/uploads/2014/12/no-photo.png"
                    else: photoa="http://bichosrunners.com/wp-content/uploads/2014/12/no-photo.png";photob=photoa;photoc=photoa;photod=photoa
                    if filtros_on == "true" and params.get("extra") == "1":
                        view = plugintools.setcontents(contents)
                        params["title"]=title;params["thumbnail"]=thumbnail;params["fanart"]=fanart;title = filtros0(params, datamovie)
                        if title:
                            url = params.get("url");genre = datamovie["genre"];genre=genre.strip();genre=genre.replace("Ciencia ficción", "Ciencia-Ficción");genre=genre.replace(" ", ", ")
                            datamovie["plot"]='[B]'+datamovie["year"]+'[/B][COLOR lightgreen][I] '+datamovie["duration"]+'  [/I][/COLOR][COLOR white][B][COLOR lightyellow]'+datamovie["rating"]+'[/B][/COLOR] [I]('+genre+')[/I] [B][COLOR lightyellow]Cast:[/B][/COLOR] '+images[14]+' [B][COLOR lightyellow]Dir:[/B][/COLOR] '+datamovie["director"]+'[CR]'+datamovie["plot"]
                            if plugintools.get_setting("pager_m3u") == "true" and interval==1:
                                plugintools.addPeli( action = "multilink" , show = total_cast , extra = filename , title = '[COLOR white]' + title + ' [COLOR lightyellow][I][Multi][/I][/COLOR]', url = url , photoa=photoa, photob=photob, photoc=photoc, photod=photod, imdb = imdb_id, page = trailer_id, thumbnail = thumbnail, info_labels = datamovie, fanart = fanart , folder = True , isPlayable = False )                                
                            else:
                                plugintools.addPeli( action = "multilink" , show = total_cast , extra = filename , title = '[COLOR white]' + title + ' [COLOR lightyellow][I][Multi][/I][/COLOR]', url = url , photoa=photoa, photob=photob, photoc=photoc, photod=photod, imdb = imdb_id, page = trailer_id, thumbnail = thumbnail, info_labels = datamovie, fanart = fanart , folder = True , isPlayable = False )
                            i = i + 1;data=file.readline();continue                                
                                
                    else:                    
                        if data.startswith("desc") == True:                        
                            plot = data.replace("desc=", "").replace('"',"");
                        if plot == "": plot = datamovie["plot"]  # Si no hay descripción, utilizaremos la sinopsis del diccionario datamovie
                        #if cat != "": title = title + ' [COLOR purple][I][Multi][/I][/COLOR]'
                        if contents == "movies":  # Control para listas de películas
                            genre = datamovie["genre"];genre=genre.strip();genre=genre.replace("Ciencia ficción", "Ciencia-Ficción");#genre=genre.replace(" ", ", ");print genre                            
                            dataplot = plugintools.get_setting("dataplot")  # Mostrar metadatos en plot para vista "tvshows"
                            if dataplot == "true":
                                try: datamovie["plot"]='[B]('+datamovie["year"]+')[/B][COLOR lightgreen][I] '+str(int(datamovie["duration"])/60)+" min"+' [/I][/COLOR][B][COLOR lightyellow] IMDB: [COLOR gold][B]'+datamovie["rating"]+'[/COLOR][/B][COLOR white][I]/'+datamovie["votes"]+'[/I][/COLOR][CR][COLOR white]'+datamovie["plot"]+'[/COLOR]'
                                except: datamovie["plot"]='[B]('+str(datamovie["year"])+')[/B][COLOR lightgreen][I] '+datamovie["duration"]+' [/I][/COLOR][B][COLOR lightyellow]IMDB: [COLOR gold]'+str(datamovie["rating"])+'[/COLOR][/B][COLOR white][I]/'+str(datamovie["votes"])+'[/I][/COLOR][CR][COLOR white]'+datamovie["plot"]+'[/COLOR]'
                                if plugintools.get_setting("pager_m3u") == "true":
                                    if interval==1:                                
                                        plugintools.addPeli( action = "multilink" , show = total_cast , extra = filename , title = '[COLOR white]' + title + ' [COLOR lightyellow][I][Multi][/I][/COLOR]', url = url , photoa=photoa, photob=photob, photoc=photoc, photod=photod, imdb = imdb_id, page = trailer_id, thumbnail = thumbnail, info_labels = datamovie, fanart = fanart , folder = True , isPlayable = False )
                                else:
                                    plugintools.addPeli( action = "multilink" , show = total_cast , extra = filename , title = '[COLOR white]' + title + ' [COLOR lightyellow][I][Multi][/I][/COLOR]', url = url , photoa=photoa, photob=photob, photoc=photoc, photod=photod, imdb = imdb_id, page = trailer_id, thumbnail = thumbnail, info_labels = datamovie, fanart = fanart , folder = True , isPlayable = False )
                            else:
                                if plugintools.get_setting("pager_m3u") == "true":
                                    if interval==1:
                                        plugintools.addPeli( action = "multilink" , show = total_cast , extra = filename , title = '[COLOR white]' + title + ' [COLOR lightyellow][I][Multi][/I][/COLOR]', url = url , photoa=photoa, photob=photob, photoc=photoc, photod=photod, imdb = imdb_id, page = trailer_id, thumbnail = thumbnail, info_labels = datamovie, fanart = fanart , folder = True , isPlayable = False )
                                else:                                    
                                    plugintools.addPeli( action = "multilink" , show = total_cast , extra = filename , title = '[COLOR white]' + title + ' [COLOR lightyellow][I][Multi][/I][/COLOR]', url = url , photoa=photoa, photob=photob, photoc=photoc, photod=photod, imdb = imdb_id, page = trailer_id, thumbnail = thumbnail, info_labels = datamovie, fanart = fanart , folder = True , isPlayable = False )     
                        else:
                            if plugintools.get_setting("pager_m3u") == "true":
                                if interval==1:
                                    plugintools.add_item( action = "multilink" , plot = datamovie["plot"] , show = total_cast, extra = filename , title = '[COLOR white]' + title + ' [COLOR lightyellow][I][Multi][/I][/COLOR]', url = url , thumbnail = thumbnail, info_labels = datamovie, fanart = fanart , folder = True , isPlayable = False )
                            else: plugintools.add_item( action = "multilink" , plot = datamovie["plot"] , show = total_cast, extra = filename , title = '[COLOR white]' + title + ' [COLOR lightyellow][I][Multi][/I][/COLOR]', url = url , thumbnail = thumbnail, info_labels = datamovie, fanart = fanart , folder = True , isPlayable = False )
                                
                        if saving_url == 1:
                            save_multilink(url, filename)
                            while url != "":
                                url = file.readline().strip()
                                save_multilink(url, filename)
                                i = i + 1
                            saving_url = 0                            
                        plot = ""

                elif url == "#multi":                    
                    if data.startswith("desc") == True:                        
                        plot = data.replace("desc=", "").replace('"',"");plot=parser_title(plot)
                        
                    if filtros_on == "true" and params.get("extra") == "1":
                        params["title"]=title;params["thumbnail"]=thumbnail;params["fanart"]=fanart;title = filtros0(params, datamovie)
                        if title:
                            url = params.get("url");genre = datamovie["genre"];genre=genre.strip();genre=genre.replace("Ciencia ficción", "Ciencia-Ficción");genre=genre.replace(" ", ", ")
                            datamovie["plot"]='[B]'+datamovie["year"]+'[/B][COLOR lightgreen][I] '+datamovie["duration"]+'  [/I][/COLOR][COLOR white][B][COLOR lightyellow]'+datamovie["rating"]+'[/B][/COLOR] [I]('+genre+')[/I] [B][COLOR lightyellow]Cast:[/B][/COLOR] '+images[14]+' [B][COLOR lightyellow]Dir:[/B][/COLOR] '+datamovie["director"]+'[CR]'+datamovie["plot"]
                            if plugintools.get_setting("pager_m3u") == "true":
                                if interval == 1:
                                    plugintools.add_item( action = "multilink" , plot = plot , show = total_cast, extra = filename , title = title, url = url ,  thumbnail = thumbnail, info_labels = datamovie, fanart = fanart , folder = True , isPlayable = False )
                            else:
                                plugintools.add_item( action = "multilink" , plot = plot , show = total_cast, extra = filename , title = title, url = url ,  thumbnail = thumbnail, info_labels = datamovie, fanart = fanart , folder = True , isPlayable = False )
                            i = i + 1;continue

                    else:
                        #Storage information
                        information = plugin.get_storage('information')
                        information.clear();information.sync()                        
                        if data.startswith("desc") == True:                        
                            plot = data.replace("desc=", "").replace('"',"")
                            plugintools.log("sinopsis= "+data)
                        if cat == "":
                            if plugintools.get_setting("pager_m3u") == "true":
                                if interval == 1:
                                    plugintools.add_item( action = "multilink" , plot = datamovie["plot"] , extra = filename , title = title + ' [COLOR lightyellow][I][Multi][/I][/COLOR]', url = url ,  thumbnail = thumbnail, info_labels = datamovie, fanart = fanart , folder = True , isPlayable = False )
                            else:
                                plugintools.add_item( action = "multilink" , plot = datamovie["plot"] , extra = filename , title = title + ' [COLOR lightyellow][I][Multi][/I][/COLOR]', url = url ,  thumbnail = thumbnail, info_labels = datamovie, fanart = fanart , folder = True , isPlayable = False )
                            if saving_url == 1:
                                save_multiparser(url, filename)
                                while url != "":
                                    url = file.readline().strip()
                                    save_multiparser(url, filename)
                                    i = i + 1
                                saving_url = 0                            
                            plot = ""
                        else:
                            if plugintools.get_setting("pager_m3u") == "true":
                                if interval == 1:
                                    plugintools.add_item( action = "multilink" , plot = datamovie["plot"] , extra = filename , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR purple][I][Multi][/I][/COLOR]' , url = url , info_labels = datamovie , thumbnail = thumbnail, fanart = fanart , folder = True , isPlayable = False )
                            else:
                                plugintools.add_item( action = "multilink" , plot = datamovie["plot"] , extra = filename , title = '[COLOR red][I]' + cat + ' / [/I][/COLOR][COLOR white] ' + title + ' [COLOR purple][I][Multi][/I][/COLOR]' , url = url , info_labels = datamovie , thumbnail = thumbnail, fanart = fanart , folder = True , isPlayable = False )
                   
                else:
                    url_analyzer(title, datamovie, thumbnail, fanart, plot=datamovie["plot"], url=data.strip())
                    data = file.readline();i = i + 1;continue

        else:
            data = file.readline();i = i + 1

    file.close()

    # Control para EPG de Fórmula TV (elimina archivo backup)
    try:
        if os.path.exists(tmp + 'backup_ftv.txt'):
            os.remove(tmp + 'backup_ftv.txt')
    except: pass
    
    # Definimos el contenido y modo de vista de la lista. Note: contents: files, songs, artists, albums, movies, tvshows, episodes, musicvideos
    unblockview = plugintools.get_setting("unblockview")  # Opcionalmente el usuario podrá fijar modos de vista
    plugintools.log("unblockview= "+unblockview)
    if unblockview == "true":
        view = plugintools.setcontents(contents)
        view = plugintools.get_setting("default_view")
        
    plugintools.close_item_list()
    
    

def myplaylists_m3u(params):  # Mis listas M3U
    plugintools.log('[%s %s].myplaylist_m3u %s' % (addonName, addonVersion, repr(params)))
    thumbnail = params.get("thumbnail")
    #plugintools.add_item(action="play" , title = "[COLOR lightyellow]Cómo importar listas M3U a mi biblioteca [/COLOR][COLOR lightblue][I][Youtube][/I][/COLOR]" , thumbnail = art + "icon.png" , url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=8i0KouM-4-U" , folder = False , isPlayable = True )
    plugintools.add_item(action="my_albums" , title = "[COLOR gold][B]Mis álbumes[/B][/COLOR][COLOR lightblue][I] (CBR/CBZ)[/I][/COLOR]" , thumbnail = art + "search.png" , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
    plugintools.add_item(action="search_channel" , title = "[COLOR lightyellow]Buscador[/COLOR]" , thumbnail = art + "search.png" , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
    plugintools.add_item(action="url_tester" , title = "[COLOR lightyellow]Probar URL![/COLOR]" , thumbnail = art + "logo.png" , fanart ='http://4.bp.blogspot.com/-XHrjQMGVG_k/UNIj-CQSCfI/AAAAAAAAAhk/xdcoPKssrXs/s1600/LiveStreaming_Banner.jpg' , folder = True , isPlayable = False )

    # Agregamos listas online privadas del usuario
    url_pl1 = plugintools.get_setting("url_pl1")
    url_pl2 = plugintools.get_setting("url_pl2")
    url_pl3 = plugintools.get_setting("url_pl3")

    # Sintaxis de la lista online. Acciones por defecto (M3U)
    action_pl1 = "getfile_http"
    action_pl2 = "getfile_http"
    action_pl3 = "getfile_http"

    tipo_pl1 = plugintools.get_setting('tipo_pl1')
    tipo_pl2 = plugintools.get_setting('tipo_pl2')
    tipo_pl3 = plugintools.get_setting('tipo_pl3')

    if tipo_pl1 == '0':
        action_pl1 = 'getfile_http'

    if tipo_pl1 == '1':
        action_pl1 = 'plx_items'

    if tipo_pl2 == '0':
        action_pl2 = 'getfile_http'

    if tipo_pl2 == '1':
        action_pl2 = 'plx_items'

    if tipo_pl3 == '0':
        action_pl3 = 'getfile_http'

    if tipo_pl3 == '1':
        action_pl3 = 'plx_items'

    title_pl1 = plugintools.get_setting("title_pl1")
    title_pl2 = plugintools.get_setting("title_pl2")
    title_pl3 = plugintools.get_setting("title_pl3")

    plugintools.add_item(action="", title='[COLOR lightyellow]Listas online:[/COLOR]', url="", folder=False, isPlayable=False)

    if url_pl1 != "":
        if title_pl1 == "":
            title_pl1 = "[COLOR lightyellow]Lista online 1[/COLOR]"
        plugintools.add_item(action=action_pl1, title='  '+title_pl1, url=url_pl1, folder=True, isPlayable=False)

    if url_pl2 != "":
        if title_pl2 == "":
            title_pl2 = "[COLOR lightyellow]Lista online 2[/COLOR]"
        plugintools.add_item(action=action_pl2, title='  '+title_pl2, url=url_pl2, folder=True, isPlayable=False)

    if url_pl3 != "":
        if title_pl3 == "":
            title_pl3 == "[COLOR lightyellow]Lista online 3[/COLOR]"
        plugintools.add_item(action=action_pl3, title='  '+title_pl3, url=url_pl3, folder=True, isPlayable=False)

    ficheros = os.listdir(playlists)  # Lectura de archivos en carpeta /playlists. Cuidado con las barras inclinadas en Windows

    # Control paternal
    adult_mode = plugintools.get_setting("adult_mode")

    for entry in ficheros:
        plot = entry.split(".")[0]
        if adult_mode == "false" :
            if entry.find("XXX") >= 0 :
                plugintools.log("Activando control paternal...")

            else:
                if entry.endswith("plx") == True:  # Control para según qué extensión del archivo se elija thumbnail y función a ejecutar
                    entry = entry.replace(".plx", "")
                    plugintools.add_item(action="plx_items" , plot = plot , title = '[COLOR white]' + entry + '[/COLOR][COLOR green][B][I].plx[/I][/B][/COLOR]' , url = playlists + entry , thumbnail = art + 'plx.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("p2p") == True:
                    entry = entry.replace(".p2p", "")
                    plugintools.add_item(action="p2p_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR blue][B][I].p2p[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'p2p.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("m3u") == True:
                    entry = entry.replace(".m3u", "")
                    plugintools.add_item(action="m3u_reader" , plot = plot , title = '[COLOR white]' + entry + '[COLOR red][B][I].m3u[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'm3u7.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("jsn") == True:
                    entry = entry.replace(".jsn", "")
                    plugintools.add_item(action="json_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR yellow][B][I].jsn[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'm3u7.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

        else:

                if entry.endswith("plx") == True:  # Control para según qué extensión del archivo se elija thumbnail y función a ejecutar
                    entry = entry.replace(".plx", "")
                    plugintools.add_item(action="plx_items" , plot = plot , title = '[COLOR white]' + entry + '[/COLOR][COLOR green][B][I].plx[/I][/B][/COLOR]' , url = playlists + entry , thumbnail = art + 'plx.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("p2p") == True:
                    entry = entry.replace(".p2p", "")
                    plugintools.add_item(action="p2p_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR blue][B][I].p2p[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'p2p.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("m3u") == True:
                    entry = entry.replace(".m3u", "")
                    plugintools.add_item(action="m3u_reader" , plot = plot , title = '[COLOR white]' + entry + '[COLOR red][B][I].m3u[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'm3u7.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

                elif entry.endswith("jsn") == True:
                    entry = entry.replace(".jsn", "")
                    plugintools.add_item(action="json_items" , plot = plot , title = '[COLOR white]' + entry + '[COLOR yellow][B][I].jsn[/I][/B][/COLOR]', url = playlists + entry , thumbnail = art + 'm3u7.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )


def my_albums(params):  # Mis listas M3U
    plugintools.log('[%s %s].my_albums %s' % (addonName, addonVersion, repr(params)))
    thumbnail = params.get("thumbnail")

    #plugintools.add_item(action="" , title = "[COLOR gold][B]Mis álbumes[/B][/COLOR][COLOR lightblue][I] (CBR/CBZ)[/I][/COLOR]" , thumbnail = art + "albums_icon.png" , fanart = art + 'my_albums.jpg' , folder = False , isPlayable = False )
    plugintools.add_item(action="show_cbx", title="[COLOR orange][B]Ayuda:[/B] [/COLOR][COLOR white]Atajos de teclado[/COLOR]", url=art+'help_cbx.png', thumbnail = art+'cbr.png', fanart = art + 'my_albums.jpg', folder=False, isPlayable=False)    
    ficheros = os.listdir(temp)  # Lectura de archivos en carpeta /temp. Cuidado con las barras inclinadas en Windows

    # Control paternal
    adult_mode = plugintools.get_setting("adult_mode")

    for entry in ficheros:
        plot = entry.split(".")
        plot = plot[0]
        plugintools.log("entry= "+entry)

        portada = playlists + entry.replace(".cbr", "").replace(".cbz", "") + ".png";
        if os.path.exists(portada) is None:
            portada = art+'cbr.png'
        print portada            

        if adult_mode == "false" :
            if entry.find("XXX") >= 0 :
                plugintools.log("Activando control paternal...")
            else:
                if entry.endswith("cbr") == True:  # Control para según qué extensión del archivo se elija thumbnail y función a ejecutar
                    entry = entry.replace(".cbr", "")
                    plugintools.addDir(action="cbx_reader" , plot = plot , title = '[COLOR white]' + entry + '[/COLOR][COLOR green][B][I].cbr[/I][/B][/COLOR]' , extra = "my_albums", url = playlists + entry , thumbnail = portada , fanart = portada , folder = True , isPlayable = False )
                elif entry.endswith("cbz") == True:
                    entry = entry.replace(".cbz", "")                   
                    plugintools.addDir(action="cbx_reader" , plot = plot , title = '[COLOR white]' + entry + '[COLOR blue][B][I].cbz[/I][/B][/COLOR]', extra = "my_albums" , url = playlists + entry , thumbnail = portada , fanart = portada , folder = True , isPlayable = False )

        else:

                if entry.endswith("cbr") == True:  # Control para según qué extensión del archivo se elija thumbnail y función a ejecutar
                    entry = entry.replace(".cbr", "")                  
                    plugintools.addDir(action="cbx_reader" , plot = plot , title = '[COLOR white]' + entry + '[/COLOR][COLOR green][B][I].cbr[/I][/B][/COLOR]' , extra = "my_albums" , url = playlists + entry , thumbnail = portada , fanart = portada , folder = True , isPlayable = False )

                elif entry.endswith("cbz") == True:
                    entry = entry.replace(".cbz", "")                  
                    plugintools.addDir(action="cbx_reader" , plot = plot , title = '[COLOR white]' + entry + '[COLOR blue][B][I].cbz[/I][/B][/COLOR]', extra = "my_albums" , url = playlists + entry , thumbnail = portada , fanart = portada , folder = True , isPlayable = False )



def playlists_m3u(params):  # Biblioteca online
    plugintools.log('[%s %s].playlist_m3u %s' % (addonName, addonVersion, repr(params)))

    data = plugintools.read( params.get("url") )
    name_channel = params.get("plot")
    pattern = '<name>'+name_channel+'(.*?)</channel>'
    data = plugintools.find_single_match(data, pattern)
    online = '[COLOR yellowgreen][I][Auto][/I][/COLOR]'
    params["ext"] = 'm3u'
    plugintools.add_item( action="" , title='[B][COLOR yellow]'+name_channel+'[/B][/COLOR] - [B][I][COLOR lightyellow]juarrox@gmail.com [/COLOR][/B][/I]' , thumbnail= art + 'icon.png' , folder = False , isPlayable = False )
    subchannel = re.compile('<subchannel>([^<]+)<name>([^<]+)</name>([^<]+)<thumbnail>([^<]+)</thumbnail>([^<]+)<url>([^<]+)</url>([^<]+)</subchannel>').findall(data)
    # Sustituir por una lista!!!
    for biny, ciny, diny, winy, pixy, dixy, boxy in subchannel:
        if ciny == "Vcx7 IPTV":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            params["ext"] = "m3u"
            title = ciny
            params["title"]=title
        elif ciny == "Largo Barbate M3U":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "XBMC Mexico":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "allSat":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "AND Wonder":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        elif ciny == "FenixTV":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            params["title"]=title
        else:
            plot = ciny.split("[")
            plot = plot[0]
            plugintools.addDir( action="getfile_http" , plot = plot , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )



    plugintools.log('[%s %s].playlist_m3u %s' % (addonName, addonVersion, repr(params)))    



def getfile_http(params):  # Descarga de lista M3U + llamada a m3u_reader para que liste los items
    plugintools.log('[%s %s].getfile_http %s' % (addonName, addonVersion, repr(params)))
    
    url = params.get("url")
    if url.endswith("m3u") == True:
        params["ext"] = "m3u"
        getfile_url(params)        
        m3u_reader(params)
    elif url.endswith("plx") == True or params.get("plot") == "PLX":
        params["ext"] = "plx"
        getfile_url(params)
        plx_items(params)
    else:
        params["ext"] = "m3u"
        getfile_url(params)        
        m3u_reader(params)

def parse_url(url):
    if url != "": url = url.replace("rtmp://$OPT:rtmp-raw=", "").strip()
    return url

def getfile_url(params):
    plugintools.log('[%s %s].getfile_url %s' % (addonName, addonVersion, repr(params)))
    ext = params.get("ext")
    title = params.get("title")
    plugintools.log("ext= "+ext)

    if ext == 'plx':
        filename = parser_title(title).strip()
        params["plot"]=filename.strip()
        filename = title.strip() + ".plx"  # El título del archivo con extensión (m3u, p2p, plx)
    elif ext == 'm3u':
        filename = params.get("plot").strip()
        # Vamos a quitar el formato al texto para que sea el nombre del archivo
        filename = parser_title(title).strip()
        filename = filename + ".m3u"  # El título del archivo con extensión (m3u, p2p, plx)
    else:
        ext == 'p2p'
        filename = parser_title(title)
        filename = filename + ".p2p"  # El título del archivo con extensión (m3u, p2p, plx)

    if filename.endswith("plx") == True: filename = parser_title(filename).strip()
    if filename.endswith(" .plx") == True: filename=filename.replace(" .plx", ".plx").strip()

    url = params.get("url")
    plugintools.log("filename= "+filename)    
    plugintools.log("url= "+url)

    try:
        response = urllib2.urlopen(url)
        body = response.read()
    except:
        request_headers=[]  # Control si la lista está en el cuerpo del HTTP
        request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
        body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)

    fh = open(playlists + filename, "wb")
    fh.write(body)
    fh.close()

    file = open(playlists + filename, "r")
    file.seek(0)
    data = file.readline()
    data = data.strip()

    lista_items = {'linea': data}
    file.seek(0)
    lista_items = {'plot': data}
    file.seek(0)


def header_xml(params):
    plugintools.log('[%s %s].header_xml %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    params.get("title")
    data = plugintools.read(url)
    # plugintools.log("data= "+data)
    author = plugintools.find_single_match(data, '<poster>(.*?)</poster>')
    author = author.strip()
    fanart = plugintools.find_single_match(data, '<fanart>(.*?)</fanart>')
    message = plugintools.find_single_match(data, '<message>(.*?)</message>')
    desc = plugintools.find_single_match(data, '<description>(.*?)</description>')
    thumbnail = plugintools.find_single_match(data, '<thumbnail>(.*?)</thumbnail>')

    if author != "":
        if message != "":
            plugintools.add_item(action="" , plot = author , title = '[COLOR green][B]' + author + '[/B][/COLOR][I] ' + message + '[/I]', url = "" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )
            return fanart
        else:
            plugintools.add_item(action="" , plot = author , title = '[COLOR green][B]' + author + '[/B][/COLOR]', url = "" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )
            return fanart
    else:
        if desc != "":
            plugintools.add_item(action="" , plot = author , title = '[COLOR green][B]' + desc + '[/B][/COLOR]', url = "" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )
            return fanart
        else:
            return fanart


def search_channel(params):
    plugintools.log('[%s %s].search_channel %s' % (addonName, addonVersion, repr(params)))

    buscar = params.get("plot")
    if buscar == "":
        last_search = plugintools.get_setting("last_search")
        texto = plugintools.keyboard_input(last_search)
        plugintools.set_setting("last_search",texto)
        params["texto"]=texto
        texto = texto.lower()
        cat = ""
        if texto == "":
            errormsg = plugintools.message("PalcoTV","Por favor, introduzca el canal a buscar")
            return errormsg

    else:
        texto = buscar
        texto = texto.lower()
        plugintools.log("texto a buscar= "+texto)
        cat = ""

    results = open(temp + 'search.txt', "wb")
    results.seek(0)
    results.close()

    # Listamos archivos de la biblioteca local
    ficheros = os.listdir(playlists)  # Lectura de archivos en carpeta /playlists. Cuidado con las barras inclinadas en Windows

    for entry in ficheros:
        if entry.endswith("m3u") == True:
            plot = entry.split(".")
            plot = plot[0]  # plot es la variable que recoge el nombre del archivo (sin extensión txt)
            # Abrimos el primer archivo
            filename = plot + '.m3u'
            plugintools.log("Archivo M3U: "+filename)
            arch = open(playlists + filename, "r")
            num_items = len(arch.readlines())
            i = 0  # Controlamos que no se salga del bucle while antes de que lea el último registro de la lista
            arch.seek(0)
            data = arch.readline()
            data = data.strip()
            plugintools.log("data linea= "+data)
            texto = texto.strip()
            plugintools.log("data_antes= "+data)
            plugintools.log("texto a buscar= "+texto)

            data = arch.readline()
            data = data.strip()
            i = i + 1
            while i <= num_items :
                if data.startswith('#EXTINF:-1') == True:
                    data = data.replace('#EXTINF:-1,', "")  # Ignoramos la primera parte de la línea
                    data = data.replace(",", "")
                    title = data.strip()  # Ya tenemos el título

                    if data.find('$ExtFilter="') >= 0:
                        data = data.replace('$ExtFilter="', "")

                    if data.find(' $ExtFilter="') >= 0:
                        data = data.replace('$ExtFilter="', "")

                    title = title.replace("-AZBOX*", "")
                    title = title.replace("AZBOX *", "")

                    images = m3u_items(title)
                    thumbnail = images[0]
                    fanart = images[1]
                    cat = images[2]
                    title = images[3]
                    minus = title.lower()
                    data = arch.readline()
                    data = data.strip()
                    i = i + 1

                    if minus.find(texto) >= 0:
                    # if re.match(texto, title, re.IGNORECASE):
                        # plugintools.log("Concidencia hallada. Obtenemos url del canal: " + texto)
                        if data.startswith("http") == True:
                            url = data.strip()
                            if cat != "":  # Controlamos el caso de subcategoría de canales
                                results = open(temp + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                continue
                            else:
                                results = open(temp + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                continue
                        if data.startswith("rtmp") == True:
                            url = data
                            url = parse_url(url)
                            if cat != "":   # Controlamos el caso de subcategoría de canales
                                results = open(temp + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                continue
                            else:
                                results = open(temp + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                continue
                        if data.startswith("yt") == True:
                            url = data
                            results = open(temp + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                            results.write(url + '\n\n')
                            results.close()
                            data = arch.readline()
                            i = i + 1
                            continue


                else:
                    data = arch.readline()
                    data = data.strip()
                    plugintools.log("data_buscando_title= "+data)
                    i = i + 1

            else:
                data = arch.readline()
                data = data.strip()
                plugintools.log("data_final_while= "+data)
                i = i + 1
                continue



    # Listamos archivos de la biblioteca local
    ficheros = os.listdir(playlists)  # Lectura de archivos en carpeta /playlist. Cuidado con las barras inclinadas en Windows

    for entry in ficheros:
        if entry.endswith('p2p') == True:
            plot = entry.split(".")
            plot = plot[0]  # plot es la variable que recoge el nombre del archivo (sin extensión txt)
            # Abrimos el primer archivo
            plugintools.log("texto a buscar= "+texto)
            filename = plot + '.p2p'
            arch = open(playlists + filename, "r")
            num_items = len(arch.readlines())
            plugintools.log("archivo= "+filename)
            i = 0  # Controlamos que no se salga del bucle while antes de que lea el último registro de la lista
            arch.seek(0)
            while i <= num_items:
                data = arch.readline()
                data = data.strip()
                title = data
                texto = texto.strip()
                plugintools.log("linea a buscar title= "+data)
                i = i + 1

                if data.startswith("#") == True:
                    data = arch.readline()
                    data = data.strip()
                    i = i + 1
                    continue

                if data.startswith("default=") == True:
                    data = arch.readline()
                    data = data.strip()
                    i = i + 1
                    continue

                if data.startswith("art=") == True:
                    data = arch.readline()
                    data = data.strip()
                    i = i + 1
                    continue

                if data != "":
                    title = data.strip()  # Ya tenemos el título
                    minus = title.lower()
                    if minus.find(texto) >= 0:
                        data = arch.readline()
                        i = i + 1
                        plugintools.log("linea a comprobar url= "+data)
                        if data.startswith("sop") == True:
                            # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
                            title_fixed= urllib_quote_plus(title)
                            title_fixed=parser_title(title);title_fixed=title_fixed.replace(" ", "+").strip()
                            url=data.split(":3912/")[1];url=url.strip();url='sop://'+url
                            url = p2p_builder_url(url, title_fixed, p2p="sop")
                            results = open(temp + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '"' + filename + '\n')  # Hay que cambiar esto! No puede agregar #EXTINF:-1, si no es una lista m3u
                            results.write(url + '\n\n')
                            results.close()
                            data = arch.readline()
                            i = i + 1
                            continue

                        elif data.startswith("magnet") == True:
                            # magnet:?xt=urn:btih:6CE983D676F2643430B177E2430042E4E65427...
                            title_fixed = title.split('"')
                            title = title_fixed[0]
                            plugintools.log("title magnet= "+title)
                            url = data
                            plugintools.log("url magnet= "+url)
                            results = open(temp + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                            results.write(url + '\n\n')
                            results.close()
                            data = arch.readline()
                            i = i + 1
                            continue

                        elif data.find("://") == -1:
                            # plugin://plugin.video.p2p-streams/?url=a55f96dd386b7722380802b6afffc97ff98903ac&mode=1&name=Sky+Sports+title
                            title_fixed = title.split('"')
                            title = title_fixed[0]
                            title_fixed = title.replace(" " , "+")
                            url = p2p_builder_url(data, title_fixed, p2p="ace")
                            results = open(temp + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '"' + filename + '\n')  # Hay que cambiar esto! No puede agregar #EXTINF:-1, si no es una lista m3u
                            results.write(url + '\n\n')
                            results.close()
                            data = arch.readline()
                            i = i + 1
                            continue

                    else:
                        plugintools.log("no coinciden titulo y texto a buscar")


    for entry in ficheros:
        if entry.endswith('plx') == True:
            plot = entry.split(".")
            plot = plot[0]  # plot es la variable que recoge el nombre del archivo (sin extensión)
            # Abrimos el primer archivo
            plugintools.log("texto a buscar= "+texto)
            filename = plot + '.plx'
            plugintools.log("archivo PLX: "+filename)
            arch = open(playlists + filename, "r")
            num_items = len(arch.readlines())
            print num_items
            i = 0
            arch.seek(0)
            while i <= num_items:
                data = arch.readline()
                data = data.strip()
                i = i + 1
                print i

                if data.startswith("#") == True:
                    continue

                if (data == 'type=video') or (data == 'type=audio') == True:
                    data = arch.readline()
                    i = i + 1
                    print i
                    data = data.replace("name=", "")
                    data = data.strip()
                    title = data
                    minus = title.lower()
                    if minus.find(texto) >= 0:
                        plugintools.log("Título coincidente= "+title)
                        data = arch.readline()
                        plugintools.log("Siguiente linea= "+data)
                        i = i + 1
                        print i
                        print "Analizamos..."
                        while data <> "" :
                            if data.startswith("thumb") == True:
                                data = arch.readline()
                                plugintools.log("data_plx= "+data)
                                i = i + 1
                                print i
                                continue

                            if data.startswith("date") == True:
                                data = arch.readline()
                                plugintools.log("data_plx= "+data)
                                i = i + 1
                                print i
                                continue

                            if data.startswith("background") == True:
                                data = arch.readline()
                                plugintools.log("data_plx= "+data)
                                i = i + 1
                                print i
                                continue

                            if data.startswith("URL") == True:
                                data = data.replace("URL=", "")
                                data = data.strip()
                                url = data
                                parse_url(url)
                                plugintools.log("URL= "+url)
                                results = open(temp + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                break




    arch.close()
    results.close()
    params["plot"] = 'search'  # Pasamos a la lista de variables (params) el valor del archivo de resultados para que lo abra la función m3u_reader
    params['texto']= texto  # Agregamos al diccionario una nueva variable que contiene el texto a buscar
    m3u_reader(params)



def encode_string(url):


    d = {    '\xc1':'A',
            '\xc9':'E',
            '\xcd':'I',
            '\xd3':'O',
            '\xda':'U',
            '\xdc':'U',
            '\xd1':'N',
            '\xc7':'C',
            '\xed':'i',
            '\xf3':'o',
            '\xf1':'n',
            '\xe7':'c',
            '\xba':'',
            '\xb0':'',
            '\x3a':'',
            '\xe1':'a',
            '\xe2':'a',
            '\xe3':'a',
            '\xe4':'a',
            '\xe5':'a',
            '\xe8':'e',
            '\xe9':'e',
            '\xea':'e',
            '\xeb':'e',
            '\xec':'i',
            '\xed':'i',
            '\xee':'i',
            '\xef':'i',
            '\xf2':'o',
            '\xf3':'o',
            '\xf4':'o',
            '\xf5':'o',
            '\xf0':'o',
            '\xf9':'u',
            '\xfa':'u',
            '\xfb':'u',
            '\xfc':'u',
            '\xe5':'a'
    }

    nueva_cadena = url
    for c in d.keys():
        plugintools.log("caracter= "+c)
        nueva_cadena = nueva_cadena.replace(c,d[c])

    auxiliar = nueva_cadena.encode('utf-8')
    url = nueva_cadena
    return nueva_cadena



def plx_items(params):
    plugintools.log('[%s %s].plx_items %s' % (addonName, addonVersion, repr(params)))

    fanart = "";background = art+'livestream.jpg';logo = "";thumbnail = "";datamovie = {};plot="";name="";url="";
    
    # Control para elegir el título (plot, si formateamos el título / title , si no existe plot)
    if params.get("plot") == "":
        title = params.get("title").strip() + '.plx';title = parser_title(title).strip();filename = title;params["plot"]=filename;params["ext"] = 'plx';getfile_url(params);title = params.get("title")
    else: title = params.get("plot").strip();title = parser_title(title)        

    title = title.replace(" .plx", ".plx").strip()
    file = open(playlists + parser_title(title) + '.plx', "r");file.seek(0);data=file.readline();num_items = len(file.readlines());file.seek(0)

    # Control de listas privadas de Navix
    content=file.read();plugintools.log("CONTENIDO PLX: "+content)
    
    # Lectura del título y fanart de la lista
    data = file.readline();#background = art + 'fanart.jpg';logo = art + 'plx.png'    
    while data <> "":
        plugintools.log("data= "+data)
        if data.startswith("version=") == True:
            data = file.readline();continue

        elif data.startswith("description") == True:
            desc = data.replace("description=", "").strip()
            data=file.readline().strip()
            while data.endswith("/description") == False:
                desc=desc+"[CR]"+data;plugintools.log("desc= "+desc)
                data=file.readline().strip()
            datamovie["plot"]=desc;continue            
        
        elif data.startswith("background=") == True:
            data = data.replace("background=", "");background = data.strip()
            if background == "": background = params.get("extra")
            if background == "": background = art + 'fanart.jpg'
            data = file.readline();continue

        elif data.startswith("title=") == True or data.startswith("name=") == True:
            name = data.replace("title=", "").replace("name=", "").strip()
            if name == "Select sort order for this list": name = "Seleccione criterio para ordenar esta lista... "
            data = file.readline();continue

        elif data.startswith("logo=") == True:
            data = data.replace("logo=", "");logo = data.strip();title = parser_title(title)
            if thumbnail == "": thumbnail = art + 'plx.png'

        else: data=file.readline().strip();continue

    if plugintools.get_setting("nolabel") == "false": plugintools.add_item(action="" , title = '[COLOR lightyellow][B][I]playlists / '+ title + '[/B][/I][/COLOR]', url = playlists + title , thumbnail = logo , fanart = background , folder = False , isPlayable = False)
    else: plugintools.add_item(action="" , title = '[COLOR lightblue][I][B]' + name + '[/B][/I][/COLOR]' , url = "" , thumbnail = logo , fanart = background , folder = False , isPlayable = False)
    
    try:
        data = file.readline()
        if data.startswith("background=") == True:
            data = data.replace("background=", "").strip();fanart = data;background = fanart
        else:
            if data.startswith("background=") == True:            
                data = data.replace("background=", "");fanart = data.strip();background = fanart
            else:
                if data.startswith("title=") == True:
                    name = data.replace("title=", "").strip()

    except: plugintools.log("ERROR: Unable to load PLX file")

    data = file.readline()
    try:
        if data.startswith("title=") == True:
            data = data.replace("title=", "");name = data.strip()
            plugintools.add_item(action="" , title = '[COLOR lightyellow][B][I]playlists / '+ title +'[/I][/B][/COLOR]' , url = playlists + title , thumbnail = logo , fanart = fanart , folder = False , isPlayable = False)
            plugintools.add_item(action="" , title = '[I][B]' + name + '[/B][/I]' , url = "" , thumbnail = art + "icon.png" , fanart = fanart , folder = False , isPlayable = False)
    except:
        plugintools.log("Unable to read PLX title")

    if content.find("# cached") >= 0:
        plugintools.add_item(action="", title="Lista vacía", folder=False, isPlayable=False)
    elif content.find("Access Denied") >= 0:
        plugintools.add_item(action="", title="[COLOR red]Acceso denegado[/COLOR]", thumbnail=art+'denied.png', fanart=background, folder=False, isPlayable=False)
        plugintools.add_item(action="", title="[COLOR white]Esta es una lista privada con acceso restringido por el usuario.[/COLOR]", thumbnail=art+'denied.png', fanart=background, folder=False, isPlayable=False)        

    # Lectura de items
    i = 0;file.seek(0);url=""
    while i <= num_items:
        data = file.readline().strip();i = i + 1
        if data.startswith("#") == True: continue
        elif data.startswith("rating") == True: continue
        elif data.startswith("description") == True: continue
        if (data == 'type=comment') == True:
            data = file.readline();i = i + 1;plugintools.log("Comment data= "+data)
            
            while data <> "" :
                if data.startswith("#") == True:
                    data = file.readline().strip();i = i + 1;continue
                    
                elif data.startswith("name") == True:
                    title = data.replace("name=", "");data = file.readline().strip();i = i + 1;continue

                elif data.startswith("thumb") == True:
                    thumbnail = data.replace("thumb=", "").strip()
                    if thumbnail == "": thumbnail = logo
                    data = file.readline().strip();i = i + 1;continue

                elif data.startswith("background") == True:
                    fanart = data.replace("background=", "").strip()
                    if fanart == "": fanart = background
                    data = file.readline().strip();i = i + 1;continue

                else: data=file.readline().strip();continue

            plugintools.add_item(action="", title = title , url = "", thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)

        if (data == 'type=video') or (data == 'type=audio') == True or (data == 'type=text') == True:
            data = file.readline();i = i + 1;plugintools.log("data video= "+data)
            while data <> "" :
                plugintools.log("data= "+data)
                if data.startswith("#") == True:
                    data = file.readline().strip();i = i + 1;continue
                elif data.startswith("description") == True:
                    desc = data.replace("description=", "").strip();plugintools.log("desc= "+desc)
                    while desc.endswith("/description") == False:
                        desc=desc+"[CR]"+data;data=file.readline().strip();i = i + 1                        
                    datamovie["plot"]=desc.replace("/description", "").strip();plugintools.log("plot definitivo= "+desc);data=file.readline().strip();i = i + 1;continue                    
                elif data.startswith("rating") == True:
                    data = file.readline().strip();i = i + 1;continue
                elif data.startswith("name") == True:
                    title = data.replace("name=", "").strip();plugintools.log("Video name= "+title)
                    if title == "[COLOR=FF00FF00]by user-assigned order[/COLOR]" : title = "Seleccione criterio para ordenar ésta lista... "
                    if title == "by user-assigned order" : title = "Según se han agregado en la lista"
                    if title == "by date added, oldest first" : title = "Por fecha de agregación, las más antiguas primero"
                    if title == "by date added, newest first" : title = "Por fecha de agregación, las más nuevas primero"
                    data = file.readline().strip();i = i + 1                    
                elif data.startswith("thumb") == True:
                    thumbnail = data.replace("thumb=", "").strip();plugintools.log("Video thumbnail= "+thumbnail)
                    if thumbnail == "": thumbnail = logo
                    data = file.readline().strip();i = i + 1;continue
                elif data.startswith("date") == True:
                    data = file.readline();i = i + 1;continue
                elif data.startswith("background") == True:
                    fanart = data.replace("background=", "").strip()
                    if fanart == "": fanart = background
                    data = file.readline().strip();i = i + 1;continue
                elif data.startswith("URL") == True:
                    # Control para el caso de que no se haya definido fanart en cada entrada de la lista => Se usa el background general
                    if fanart == "": fanart = background
                    url = data.replace("URL=", "").strip();parse_url(url);plugintools.log("Video URL= "+url);url_analyzer(title, datamovie, thumbnail, fanart, plot, url);data = file.readline().strip();i = i + 1;continue
                elif data.startswith("processor") == True: data = file.readline().strip();i = i + 1; continue;
                elif data == "" or data.startswith("#") == True: url_analyzer(title, datamovie, thumbnail, fanart, plot, url);data = file.readline().strip();i = i + 1;break;
                else: data = file.readline().strip();i = i + 1

        if (data == 'type=playlist') == True:
            if fanart == "": fanart = background  # Control si no se definió fanart en cada entrada de la lista => Se usa fanart global de la lista            
            while data <> "" :
                data = file.readline().strip();i = i + 1;
                if data.startswith("#") == True: continue
                elif data.startswith("name") == True :
                    title = data.replace("name=", "").strip()
                    if title == '>>>' :
                        title = title.replace(">>>", "[I][COLOR lightyellow]Siguiente[/I][/COLOR]");thumbnail=art+'plx.png';continue

                    elif title == '<<<' :
                        title = title.replace("<<<", "[I][COLOR lightyellow]Anterior[/I][/COLOR]");thumbnail=art+'plx.png';continue

                    elif title.find("Sorted by user-assigned order") >= 0:
                        title = "[I][COLOR lightyellow]Ordenar listas por...[/I][/COLOR]";continue

                    elif title.find("Sorted A-Z") >= 0:
                        title = "[I][COLOR lightyellow][COLOR lightyellow]De la A a la Z[/I][/COLOR]";continue
                        
                    elif title.find("Sorted Z-A") >= 0:
                        title = "[I][COLOR lightyellow]De la Z a la A[/I][/COLOR]";continue

                    elif title.find("Sorted by date added, newest first") >= 0:
                        title = "Ordenado por: Las + recientes primero...";continue

                    elif title.find("Sorted by date added, oldest first") >= 0:
                        title = "Ordenado por: Las + antiguas primero...";continue

                    elif title.find("by user-assigned order") >= 0:
                        title = "[COLOR lightyellow]Ordenar listas por...[/COLOR]";continue

                    elif title.find("by date added, newest first") >= 0 :
                        title = "Las + recientes primero...";continue
                        
                    elif title.find("by date added, oldest first") >= 0 :
                        title = "Las + antiguas primero...";continue

                    else: continue
                        
                elif data.startswith("thumb") == True:
                    thumbnail = data.replace("thumb=", "").strip();continue

                elif data.startswith("URL") == True:
                    url = data.replace("URL=", "").strip();continue

                elif data.startswith("-=") == True or data.startswith("date=") == True: continue

                elif data.startswith("description") == True:
                    desc = data.replace("description=", "").strip()
                    while data.endswith("/description") == False:
                        desc=desc+"[CR]"+data;plugintools.log("data= "+data)
                        data=file.readline().strip();i = i + 1
                    datamovie["plot"]=desc;continue

                elif data.startswith("player") == True or data.startswith("rating") == True: continue

                elif data == "": url_analyzer(title, datamovie, thumbnail, fanart, plot, url);fanart="";thumbnail="";datamovie["plot"]="";break
                else: continue

        else: data = file.readline().strip();i = i + 1;continue

    file.close()


    # Purga de listas erróneas creadas al abrir listas PLX (por los playlist de ordenación que crea Navixtreme)

    if os.path.isfile(playlists + 'Siguiente.plx'):
        os.remove(playlists + 'Siguiente.plx')
        print "Correcto!"
    else:
        pass

    if os.path.isfile(playlists + 'Ordenar listas por....plx'):
        os.remove(playlists + 'Ordenar listas por....plx')
        print "Ordenar listas por....plx eliminado!"
        print "Correcto!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'A-Z.plx'):
        os.remove(playlists + 'A-Z.plx')
        print "A-Z.plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'De la A a la Z.plx'):
        os.remove(playlists + 'De la A a la Z.plx')
        print "De la A a la Z.plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'Z-A.plx'):
        os.remove(playlists + 'Z-A.plx')
        print "Z-A.plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'De la Z a la A.plx'):
        os.remove(playlists + 'De la Z a la A.plx')
        print "De la Z a la A.plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'Las + antiguas primero....plx'):
        os.remove(playlists + 'Las + antiguas primero....plx')
        print "Las más antiguas primero....plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'by date added, oldest first.plx'):
        os.remove(playlists + 'by date added, oldest first.plx')
        print "by date added, oldest first.plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'Las + recientes primero....plx'):
        os.remove(playlists + 'Las + recientes primero....plx')
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'by date added, newest first.plx'):
        os.remove(playlists + 'by date added, newest first.plx')
        print "by date added, newest first.plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'Sorted by user-assigned order.plx'):
        os.remove(playlists + 'Sorted by user-assigned order.plx')
        print "Sorted by user-assigned order.plx eliminado!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'Ordenado por.plx'):
        os.remove(playlists + 'Ordenado por.plx')
        print "Correcto!"
    else:
        print "No es posible!"
        pass

    if os.path.isfile(playlists + 'Ordenado por'):
        os.remove(playlists + 'Ordenado por')
        print "Correcto!"
    else:
        print "No es posible!"
        pass


def encode_string(txt):
    plugintools.log('[%s %s].encode_string %s' % (addonName, addonVersion, txt))

    txt = txt.replace("&#231;", "ç")
    txt = txt.replace('&#233;', 'é')
    txt = txt.replace('&#225;', 'á')
    txt = txt.replace('&#233;', 'é')
    txt = txt.replace('&#225;', 'á')
    txt = txt.replace('&#241;', 'ñ')
    txt = txt.replace('&#250;', 'ú')
    txt = txt.replace('&#237;', 'í')
    txt = txt.replace('&#243;', 'ó')
    txt = txt.replace('&#39;', "'")
    txt = txt.replace("&nbsp;", "")
    txt = txt.replace("&nbsp;", "")
    txt = txt.replace('&#39;', "'")
    return txt



def splive_items(params):
    plugintools.log('[%s %s].splive_items %s' % (addonName, addonVersion, repr(params)))
    data = plugintools.read( params.get("url") )

    channel = plugintools.find_multiple_matches(data,'<channel>(.*?)</channel>')

    for entry in channel:
        # plugintools.log("channel= "+channel)
        title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
        category = plugintools.find_single_match(entry,'<category>(.*?)</category>')
        thumbnail = plugintools.find_single_match(entry,'<link_logo>(.*?)</link_logo>')
        rtmp = plugintools.find_single_match(entry,'<rtmp>([^<]+)</rtmp>')
        isIliveTo = plugintools.find_single_match(entry,'<isIliveTo>([^<]+)</isIliveTo>')
        rtmp = rtmp.strip()
        pageurl = plugintools.find_single_match(entry,'<url_html>([^<]+)</url_html>')
        link_logo = plugintools.find_single_match(entry,'<link_logo>([^<]+)</link_logo>')

        if pageurl == "SinProgramacion":
            pageurl = ""

        playpath = plugintools.find_single_match(entry, '<playpath>([^<]+)</playpath>')
        playpath = playpath.replace("Referer: ", "")
        token = plugintools.find_single_match(entry, '<token>([^<]+)</token>')

        iliveto = 'rtmp://188.122.91.73/edge'

        if isIliveTo == "0":
            if token == "0":
                url = rtmp
                url = url.replace("&amp;", "&")
                parse_url(url)
                plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )
                plugintools.log("url= "+url)
            else:
                url = rtmp + " pageUrl=" + pageurl + " " + 'token=' + token + playpath + " live=1"
                parse_url(url)
                plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )
                plugintools.log("url= "+url)

        if isIliveTo == "1":
            if token == "1":
                url = iliveto + " pageUrl=" + pageurl + " " + 'token=' + token + playpath + " live=1"
                url = url.replace("&amp;", "&")
                parse_url(url)
                plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )
                plugintools.log("url= "+url)

            else:
                url = iliveto + ' swfUrl=' + rtmp +  " playpath=" + playpath + " pageUrl=" + pageurl
                url = url.replace("&amp;", "&")
                parse_url(url)
                plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )
                plugintools.log("url= "+url)


def p2p_items(params):
    plugintools.log('[%s %s].p2p_items %s' % (addonName, addonVersion, repr(params)))

    # Vamos a localizar el título
    title = params.get("plot")
    if title == "":
        title = params.get("title")

    data = plugintools.read("http://pastebin.com/raw.php?i=ydUjKXnN")
    subcanal = plugintools.find_single_match(data,'<name>' + title + '(.*?)</subchannel>')
    thumbnail = plugintools.find_single_match(subcanal, '<thumbnail>(.*?)</thumbnail>')
    fanart = plugintools.find_single_match(subcanal, '<fanart>(.*?)</fanart>')
    plugintools.log("thumbnail= "+thumbnail)


    # Controlamos el caso en que no haya thumbnail en el menú de PalcoTV
    if thumbnail == "":
        thumbnail = art + 'p2p.png'
    elif thumbnail == 'name_rtmp.png':
        thumbnail = art + 'p2p.png'

    if fanart == "":
        fanart = art + 'p2p.png'

    # Comprobamos si la lista ha sido descargada o no
    plot = params.get("plot")

    if plot == "":
        title = params.get("title")
        title = parser_title(title)
        filename = title + '.p2p'
        getfile_url(params)
    else:
        print "Lista ya descargada (plot no vacío)"
        filename = params.get("plot")
        params["ext"] = 'p2p'
        params["plot"]=filename
        filename = filename + '.p2p'
        plugintools.log("Lectura del archivo P2P")

    plugintools.add_item(action="" , title='[COLOR lightyellow][I][B]' + title + '[/B][/I][/COLOR]' , thumbnail=thumbnail , fanart=fanart , folder=False, isPlayable=False)

    # Abrimos el archivo P2P y calculamos número de líneas
    file = open(playlists + filename, "r")
    file.seek(0)
    data = file.readline()
    num_items = len(file.readlines())
    print num_items
    file.seek(0)
    data = file.readline()
    if data.startswith("default") == True:
        data = data.replace("default=", "")
        data = data.split(",")
        thumbnail = data[0]
        fanart = data[1]
        plugintools.log("fanart= "+fanart)

    # Leemos entradas
    i = 0
    file.seek(0)
    data = file.readline()
    data = data.strip()
    while i <= num_items:
        if data == "":
            data = file.readline()
            data = data.strip()
            # plugintools.log("linea vacia= "+data)
            i = i + 1
            #print i
            continue

        elif data.startswith("default") == True:
            data = file.readline()
            data = data.strip()
            i = i + 1
            #print i
            continue

        elif data.startswith("#") == True:
            title = data.replace("#", "")
            plugintools.log("title comentario= "+title)
            plugintools.add_item(action="play" , title = title , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
            data = file.readline()
            data = data.strip()
            i = i + 1
            continue

        else:
            title = data
            title = title.strip()
            data = file.readline()
            data = data.strip()
            i = i + 1
            #print i
            plugintools.log("linea URL= "+data)
            if data.startswith("sop") == True:
                print "empieza el sopcast..."
                # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
                title = parser_title(title);title_fixed=title.replace(" ", "+").strip()
                url = p2p_builder_url(url, title_fixed, p2p="sop")
                plugintools.add_item(action="play" , title = title + ' [COLOR lightgreen][Sopcast][/COLOR]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                data = file.readline()
                data = data.strip()
                i = i + 1
                #print i
                continue

            elif data.startswith("magnet") == True:
                url = urllib.quote_plus(data)
                title = parser_title(title);title_fixed=title.replace(" ", "+").strip()
                url = p2p_builder_url(url, title_fixed, p2p="magnet")
                plugintools.add_item(action="play" , title = title + ' [COLOR orangered][Torrent][/COLOR]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                data = file.readline()
                data = data.strip()
                i = i + 1
                continue

            else:
                # plugin://plugin.video.p2p-streams/?url=a55f96dd386b7722380802b6afffc97ff98903ac&mode=1&name=Sky+Sports+title
                title = parser_title(title);title_fixed=title.replace(" ", "+").strip()
                url = p2p_builder_url(data, title_fixed, p2p="ace")
                plugintools.add_item(action="play" , title = title + ' [COLOR lightblue][Acestream][/COLOR]' , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                data = file.readline()
                data = data.strip()
                i = i + 1
                #print i




def contextMenu(params):
    plugintools.log('[%s %s].contextMenu %s' % (addonName, addonVersion, repr(params)))

    dialog = xbmcgui.Dialog()
    plot = params.get("plot")
    canales = plot.split("/")
    len_canales = len(canales)
    print len_canales
    plugintools.log("canales= "+repr(canales))

    if len_canales == 1:
        tv_a = canales[0]
        tv_a = parse_channel(tv_a)
        search_channel(params)
        selector = ""
    else:
        if len_canales == 2:
            print "len_2"
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            selector = dialog.select('PalcoTV', [tv_a, tv_b])

        elif len_canales == 3:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            selector = dialog.select('PalcoTV', [tv_a, tv_b, tv_c])

        elif len_canales == 4:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            tv_d = canales[3]
            tv_d = parse_channel(tv_d)
            selector = dialog.select('PalcoTV', [tv_a, tv_b, tv_c, tv_d])

        elif len_canales == 5:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            tv_d = canales[3]
            tv_d = parse_channel(tv_d)
            tv_e = canales[4]
            tv_e = parse_channel(tv_e)
            selector = dialog.select('PalcoTV', [tv_a, tv_b, tv_c, tv_d, tv_e])

        elif len_canales == 6:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            tv_d = canales[3]
            tv_d = parse_channel(tv_d)
            tv_e = canales[4]
            tv_e = parse_channel(tv_e)
            tv_f = canales[5]
            tv_f = parse_channel(tv_f)
            selector = dialog.select('PalcoTV', [tv_a , tv_b, tv_c, tv_d, tv_e, tv_f])

        elif len_canales == 7:
            tv_a = canales[0]
            tv_a = parse_channel(tv_a)
            tv_b = canales[1]
            tv_b = parse_channel(tv_b)
            tv_c = canales[2]
            tv_c = parse_channel(tv_c)
            tv_d = canales[3]
            tv_d = parse_channel(tv_d)
            tv_e = canales[4]
            tv_e = parse_channel(tv_e)
            tv_f = canales[5]
            tv_f = parse_channel(tv_f)
            tv_g = canales[6]
            tv_g = parse_channel(tv_g)
            selector = dialog.select('PalcoTV', [tv_a , tv_b, tv_c, tv_d, tv_e, tv_f, tv_g])

    if selector == 0:
        print selector
        if tv_a.startswith("Gol") == True:
            tv_a = "Gol"
        params["plot"] = tv_a
        plugintools.log("tv= "+tv_a)
        search_channel(params)
    elif selector == 1:
        print selector
        if tv_b.startswith("Gol") == True:
            tv_b = "Gol"
        params["plot"] = tv_b
        plugintools.log("tv= "+tv_b)
        search_channel(params)
    elif selector == 2:
        print selector
        if tv_c.startswith("Gol") == True:
            tv_c = "Gol"
        params["plot"] = tv_c
        plugintools.log("tv= "+tv_c)
        search_channel(params)
    elif selector == 3:
        print selector
        if tv_d.startswith("Gol") == True:
            tv_d = "Gol"
        params["plot"] = tv_d
        plugintools.log("tv= "+tv_d)
        search_channel(params)
    elif selector == 4:
        print selector
        if tv_e.startswith("Gol") == True:
            tv_e = "Gol"
        params["plot"] = tv_e
        plugintools.log("tv= "+tv_e)
        search_channel(params)
    elif selector == 5:
        print selector
        if tv_f.startswith("Gol") == True:
            tv_f = "Gol"
        params["plot"] = tv_f
        plugintools.log("tv= "+tv_f)
        search_channel(params)
    elif selector == 6:
        print selector
        if tv_g.startswith("Gol") == True:
            tv_g = "Gol"
        params["plot"] = tv_g
        plugintools.log("tv= "+tv_g)
        search_channel(params)
    else:
        pass



def magnet_items(params):
    plugintools.log('[%s %s].magnet_items %s' % (addonName, addonVersion, repr(params)))

    plot = params.get("plot")


    title = params.get("title")
    fanart = ""
    thumbnail = ""

    if plot != "":
        filename = params.get("plot")
        params["ext"] = 'p2p'
        params["plot"]=filename
        title = plot + '.p2p'
    else:
        getfile_url(params)
        title = params.get("title")
        title = title + '.p2p'

    # Abrimos el archivo P2P y calculamos número de líneas
    file = open(playlists + title, "r")
    file.seek(0)
    data = file.readline()
    num_items = len(file.readlines())

    # Leemos entradas
    file.seek(0)
    i = 0
    while i <= num_items:
        data = file.readline()
        i = i + 1
        #print i
        if data != "":
            data = data.strip()
            title = data
            data = file.readline()
            i = i + 1
            #print i
            data = data.strip()
            if data.startswith("magnet:") == True:
                # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
                #title_fixed = title.replace(" " , "+")
                title_fixed=urllib_quote_plus(title)
                url_fixed = urllib.quote_plus(link)
                url = url.strip()
                #url = p2p_builder_url(url, title_fixed, p2p="magnet")
                plugintools.add_item(action="launch_magnet" , title = data + ' [COLOR orangered][Torrent][/COLOR]' , url = url, thumbnail = art + 'p2p.png' , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True)
            else:
                data = file.readline()
                i = i + 1
                #print i
        else:
            data = file.readline()
            i = i + 1
            #print i


def parse_channel(txt):
    plugintools.log('[%s %s].parse_channelñana %s' % (addonName, addonVersion, txt))

    txt = txt.rstrip()
    txt = txt.lstrip()
    return txt


def futbolenlatv_manana(params):
    plugintools.log('[%s %s].futbolenlatv_mañana %s' % (addonName, addonVersion, repr(params)))

    # Fecha de mañana
    import datetime

    today = datetime.date.today()
    manana = today + datetime.timedelta(days=1)
    anno_manana = manana.year
    mes_manana = manana.month
    if mes_manana == 1:
        mes_manana = "enero"
    elif mes_manana == 2:
        mes_manana = "febrero"
    elif mes_manana == 3:
        mes_manana = "marzo"
    elif mes_manana == 4:
        mes_manana = "abril"
    elif mes_manana == 5:
        mes_manana = "mayo"
    elif mes_manana == 6:
        mes_manana = "junio"
    elif mes_manana == 7:
        mes_manana = "julio"
    elif mes_manana == 8:
        mes_manana = "agosto"
    elif mes_manana == 9:
        mes_manana = "septiembre"
    elif mes_manana == 10:
        mes_manana = "octubre"
    elif mes_manana == 11:
        mes_manana = "noviembre"
    elif mes_manana == 12:
        mes_manana = "diciembre"


    dia_manana = manana.day
    plot = str(anno_manana) + "-" + str(mes_manana) + "-" + str(dia_manana)
    print manana

    url = 'http://www.futbolenlatv.com/m/Fecha/' + plot + '/agenda/false/false'
    plugintools.log("URL mañana= "+url)
    params["url"] = url
    params["plot"] = plot
    futbolenlatv(params)


def json_items(params):
    plugintools.log('[%s %s].json_items %s' % (addonName, addonVersion, repr(params)))
    
    filename = params.get("plot")
    if filename != "":
        filename =  filename + '.jsn'
        fjson = open(playlists + filename, "r")
        data = fjson.readlines()
    else:
        data = plugintools.read(params.get("url"))
        
    # Título y autor de la lista
    try:
        match = plugintools.find_single_match(data, '"name"(.*?)"url"')
        match = match.split(",")
        namelist = match[0].strip()
        author = match[1].strip()
        namelist = namelist.replace('"', "")
        namelist = namelist.replace(": ", "")
        author = author.replace('"author":', "")
        author = author.replace('"', "")
        fanart = params.get("extra")
        thumbnail = params.get("thumbnail")
        plugintools.add_item(action="", title = '[B][COLOR lightyellow]' + namelist + '[/B][/COLOR]' , url = "" , thumbnail = thumbnail , fanart = fanart, isPlayable = False , folder = False)
    except:
        pass

    # Items de la lista
    data = plugintools.find_single_match(data, '"stations"(.*?)]')
    matches = plugintools.find_multiple_matches(data, '"name"(.*?)}')
    for entry in matches:
        if entry.find("isHost") <= 0:
            title = plugintools.find_single_match(entry,'(.*?)\n')
            title = title.replace(": ", "")
            title = title.replace('"', "")
            title = title.replace(",", "")
            url = plugintools.find_single_match(entry,'"url":(.*?)\n')
            url = url.replace('"', "")
            url = url.strip()
            params["url"]=url
            server_rtmp(params)
            server = params.get("server")
            thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
            thumbnail = thumbnail.replace('"', "")
            thumbnail = thumbnail.replace(',', "")
            thumbnail = thumbnail.strip()
            plugintools.log("thumbnail= "+thumbnail)
            # Control por si en la lista no aparece el logo en cada entrada
            if thumbnail == "" :
                thumbnail = params.get("thumbnail")

            plugintools.add_item( action="play" , title = '[COLOR white] ' + title + '[COLOR green] ['+ server + '][/COLOR]' , url = params.get("url") , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )

        else:
            title = plugintools.find_single_match(entry,'(.*?)\n')
            title = title.replace(": ", "")
            title = title.replace('"', "")
            title = title.replace(",", "")
            url = plugintools.find_single_match(entry,'"url":(.*?)\n')
            url = url.replace('"', "")
            url = url.strip()

            server = video_analyzer(url)  # Conectores multimedia
            if server != "unknown":
                url = url.replace(",", "")
                fanart = params.get("extra")
                thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                thumbnail = thumbnail.replace('"', "")
                thumbnail = thumbnail.replace(',', "")
                thumbnail = thumbnail.strip()
                plugintools.log("thumbnail= "+thumbnail)
                if thumbnail == "":
                    thumbnail = params.get("thumbnail")

                plugintools.add_item( action=server , title = title + ' [COLOR lightyellow]['+server+'][/COLOR]' , url = url , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

            else:
                # Conectores desconocidos/no reproducibles
                params["url"]=url
                server_rtmp(params)
                server = params.get("server")
                plugintools.add_item( action="play" , title = '[COLOR red] ' + title + ' ['+ server + '][/COLOR]' , url = params.get("url") , fanart = fanart , thumbnail = thumbnail , folder = False , isPlayable = True )

                if title == "":
                    plugintools.log("url= "+url)
                    fanart = params.get("extra")
                    thumbnail = plugintools.find_single_match(entry,'"image":(.*?)\n')
                    thumbnail = thumbnail.replace('"', "")
                    thumbnail = thumbnail.replace(',', "")
                    thumbnail = thumbnail.strip()
                    plugintools.log("thumbnail= "+thumbnail)
                    if thumbnail == "":
                        thumbnail = params.get("thumbnail")


def youtube_playlist(params):
    plugintools.log('[%s %s].youtube_playlist %s' % (addonName, addonVersion, repr(params)))

    data = plugintools.read( params.get("url") )

    pattern = ""
    matches = plugintools.find_multiple_matches(data,"<entry(.*?)</entry>")

    for entry in matches:
        plugintools.log("entry="+entry)

        title = plugintools.find_single_match(entry,"<titl[^>]+>([^<]+)</title>")
        plot = plugintools.find_single_match(entry,"<media\:descriptio[^>]+>([^<]+)</media\:description>")
        thumbnail = plugintools.find_single_match(entry,"<media\:thumbnail url='([^']+)'")
        url = plugintools.find_single_match(entry,"<content type\='application/atom\+xml\;type\=feed' src='([^']+)'/>")
        fanart = art + 'youtube.png'

        plugintools.add_item( action="youtube_videos" , title=title , plot=plot , url=url , thumbnail=thumbnail , fanart=fanart , folder=True )
        plugintools.log("fanart= "+fanart)



# Muestra todos los vídeos del playlist de Youtube
def youtube_videos(params):
    plugintools.log('[%s %s].youtube_videos %s' % (addonName, addonVersion, repr(params)))

    # Fetch video list from YouTube feed
    data = plugintools.read( params.get("url") )
    plugintools.log("data= "+data)

    # Extract items from feed
    pattern = ""
    matches = plugintools.find_multiple_matches(data,"<entry(.*?)</entry>")

    for entry in matches:
        plugintools.log("entry="+entry)

        # Not the better way to parse XML, but clean and easy
        title = plugintools.find_single_match(entry,"<titl[^>]+>([^<]+)</title>")
        title = title.replace("I Love Handball | ","")
        plot = plugintools.find_single_match(entry,"<summa[^>]+>([^<]+)</summa")
        thumbnail = plugintools.find_single_match(entry,"<media\:thumbnail url='([^']+)'")
        fanart = art+'youtube.png'
        video_id = plugintools.find_single_match(entry,"http\://www.youtube.com/watch\?v\=([0-9A-Za-z_-]{11})")
        url = 'plugin://plugin.video.youtube/play/?video_id='+videoid                       

        # Appends a new item to the xbmc item list
        plugintools.runAddon( action="runPlugin" , title=title , plot=plot , url=url , thumbnail=thumbnail , fanart=fanart , isPlayable=True, folder=False )



def peliseries(params):
    plugintools.log('[%s %s].peliseries %s' % (addonName, addonVersion, repr(params)))

    # Abrimos archivo remoto
    url = params.get("url")
    filepelis = urllib2.urlopen(url)

    # Creamos archivo local para pegar las entradas
    plot = params.get("plot")
    plot = parser_title(plot)
    if plot == "":
        title = params.get("title")
        title = parser_title(title)
        filename = title + ".m3u"
        fh = open(playlists + filename, "wb")
    else:
        filename = params.get("plot") + ".m3u"
        fh = open(playlists + filename, "wb")

    plugintools.log("filename= "+filename)
    url = params.get("url")
    plugintools.log("url= "+url)


    #open the file for writing
    fw = open(playlists + filename, "wb")

    #open the file for writing
    fh = open(playlists + 'filepelis.m3u', "wb")
    fh.write(filepelis.read())

    fh.close()

    fw = open(playlists + filename, "wb")
    fr = open(playlists + 'filepelis.m3u', "r")
    fr.seek(0)
    num_items = len(fr.readlines())
    print num_items
    fw.seek(0)
    fr.seek(0)
    data = fr.readline()
    fanart = params.get("extra")
    thumbnail = params.get("thumbnail")
    fw.write('#EXTM3U:"background"='+fanart+',"thumbnail"='+thumbnail)
    fw.write("#EXTINF:-1,[COLOR lightyellow][I]playlists / " + filename + '[/I][/COLOR]' + '\n\n')
    i = 0

    while i <= num_items:

        if data == "":
            data = fr.readline()
            data = data.strip()
            plugintools.log("data= " +data)
            i = i + 1
            print i
            continue

        elif data.find("http") >= 0 :
            data = data.split("http")
            chapter = data[0]
            chapter = chapter.strip()
            url = "http" + data[1]
            url = url.strip()
            plugintools.log("url= "+url)
            fw.write("\n#EXTINF:-1," + chapter + '\n')
            fw.write(url + '\n\n')
            data = fr.readline()
            plugintools.log("data= " +data)
            i = i + 1
            print i
            continue

        else:
            data = fr.readline()
            data = data.strip()
            plugintools.log("data= "+data)
            i = i + 1
            print i
            continue

    fw.close()
    fr.close()
    params["ext"]='m3u'
    filename = filename.replace(".m3u", "")
    params["plot"]=filename
    params["title"]=filename

    # Capturamos de nuevo thumbnail y fanart

    os.remove(playlists + 'filepelis.m3u')
    m3u_reader(params)


def tinyurl(params):
    plugintools.log('[%s %s].tinyurl %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    url_getlink = 'http://www.getlinkinfo.com/info?link=' +url

    plugintools.log("url_fixed= "+url_getlink)

    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    body,response_headers = plugintools.read_body_and_headers(url_getlink, headers=request_headers)
    plugintools.log("data= "+body)

    r = plugintools.find_multiple_matches(body, '<dt class="link-effective-url">Effective URL</dt>(.*?)</a></dd>')
    xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Redireccionando enlace...", 3 , art+'icon.png'))

    for entry in r:
        entry = entry.replace("<dd><a href=", "")
        entry = entry.replace('rel="nofollow">', "")
        entry = entry.split('"')
        entry = entry[1]
        entry = entry.strip()
        plugintools.log("vamos= "+entry)

        if entry.startswith("http"):
            plugintools.play_resolved_url(entry)



# Conexión con el servicio longURL.org para obtener URL original
def longurl(params):
    plugintools.log('[%s %s].longurl %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    url_getlink = 'http://api.longurl.org/v2/expand?url=' +url

    plugintools.log("url_fixed= "+url_getlink)

    try:
        request_headers=[]
        request_headers.append(["User-Agent","Application-Name/3.7"])
        body,response_headers = plugintools.read_body_and_headers(url_getlink, headers=request_headers)
        plugintools.log("data= "+body)

        # <long-url><![CDATA[http://85.25.43.51:8080/DE_skycomedy?u=euorocard:p=besplatna]]></long-url>
        # xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Redireccionando enlace...", 3 , art+'icon.png'))
        longurl = plugintools.find_single_match(body, '<long-url>(.*?)</long-url>')
        longurl = longurl.replace("<![CDATA[", "")
        longurl = longurl.replace("]]>", "")
        plugintools.log("longURL= "+longurl)
        if longurl.startswith("http"):
            plugintools.play_resolved_url(longurl)

    except:
        play(params)




# name and create our window 
class opentxt(xbmcgui.Window): 
    # and define it as self
    def __init__(self):
        # add picture control to our window (self) with a hardcoded path name to picture
        self.addControl(xbmcgui.ControlImage(0,0,720,480, art+ 'logo.png'))
        # store our window as a short variable for easy of use
        W = BlahMainWindow()
        # run our window we created with our background jpeg image
        W.doModal()
        # after the window is closed, Destroy it.
        del W



def encode_url(url):
    url_fixed= urlencode(url)
    print url_fixed



def m3u_items(title):
    #plugintools.log('[%s %s].m3u_items %s' % (addonName, addonVersion, title))
    thumbnail = art + 'icon.png'
    fanart = art + 'fanart.jpg'

    if title.find("tvg-logo") >= 0:
        thumbnail = plugintools.find_single_match(title, 'tvg-logo="([^"]+)')
        if thumbnail == "":
            thumbnail = 'm3u.png'

    if title.find("tvg-wall") >= 0:
        fanart = plugintools.find_single_match(title, 'tvg-wall="([^"]+)')
        if fanart == "":
            fanart = 'fanart.jpg'
    else: fanart = 'fanart.jpg'

    if title.find("imdb") >= 0:
        imdb = plugintools.find_single_match(title, 'imdb="([^"]+)')
    else: imdb = ""

    if title.find("director=") >= 0:
        dir = plugintools.find_single_match(title, 'director="([^"]+)')
    else: dir = ""

    if title.find("reparto=") >= 0:
        cast = plugintools.find_single_match(title, 'reparto="([^"]+)')
    else: cast = ""
        
    if title.find("guion=") >= 0:
        writers = plugintools.find_single_match(title, 'guion="([^"]+)')
    else: writers = ""

    if title.find("sinopsis=") >= 0:
        plot = plugintools.find_single_match(title, 'sinopsis="([^"]+)')
    else: plot = ""    

    if title.find("votes") >= 0:
        num_votes = plugintools.find_single_match(title, 'votes="([^"]+)')
        try:
            num_votes = int(num_votes)
            num_votes = format(num_votes, ',d')
        except: pass
    else: num_votes = ""

    if title.find("genre") >= 0:
        genre = plugintools.find_single_match(title, 'genre="([^"]+)')
    else: genre = ""

    if title.find("duration=") >= 0:
        duration = plugintools.find_single_match(title, 'duration="([^"]+)')
    else: time = ""

    if title.find("year") >= 0:
        year = plugintools.find_single_match(title, 'year="([^"]+)')
    else: year = ""

    if title.find("duration") >= 0:
        duration = plugintools.find_single_match(title, 'duration="([^"]+)')
    else: duration = 1

    if title.find("group-title") >= 0:
        cat = plugintools.find_single_match(title, 'group-title="([^"]+)')
    else:
        cat = ""

    if title.find("tvg-id") >= 0:
        tvgid = plugintools.find_single_match(title, 'tvg-id="([^"]+)')
    else: tvgid = ""

    if title.find("tvg-name") >= 0:
        tvgname = plugintools.find_single_match(title, 'tvg-name="([^"]+)')
    else: tvgname = ""

    if title.find("trailer_id") >= 0:
        trailer_id = plugintools.find_single_match(title, 'trailer_id="([^"]+)')
    else: trailer_id = ""

    if title.find("imdb_id") >= 0:
        imdb_id = plugintools.find_single_match(title, 'imdb_id="([^"]+)')
    else: imdb_id = ""

    if title.find("photoset") >= 0:
        photoset = plugintools.find_single_match(title, 'photoset="([^"]+)')
    else: photoset = ""

    if title.find("imdb_id") >= 0:
        imdb_id = plugintools.find_single_match(title, 'imdb_id="([^"]+)')
    else: imdb_id = ""     
    
    only_title = title.split(",")[1]
    return thumbnail, fanart, cat, only_title, tvgid, tvgname, imdb, duration, year, dir, writers, genre, num_votes, plot, cast, trailer_id, imdb_id, photoset


def add_playlist(params):
    plugintools.log('[%s %s].add_playlist %s' % (addonName, addonVersion, repr(params)))
    url_pl1 = plugintools.get_setting("url_pl1")
    url_pl2 = plugintools.get_setting("url_pl2")
    url_pl3 = plugintools.get_setting("url_pl3")

    # Sintaxis de la lista online. Acciones por defecto (M3U)
    action_pl1 = "getfile_http"
    action_pl2 = "getfile_http"
    action_pl3 = "getfile_http"

    tipo_pl1 = plugintools.get_setting('tipo_pl1')
    tipo_pl2 = plugintools.get_setting('tipo_pl2')
    tipo_pl3 = plugintools.get_setting('tipo_pl3')

    if tipo_pl1 == '0':
        action_pl1 = 'getfile_http'

    if tipo_pl1 == '1':
        action_pl1 = 'plx_items'

    if tipo_pl2 == '0':
        action_pl2 = 'getfile_http'

    if tipo_pl2 == '1':
        action_pl2 = 'plx_items'

    if tipo_pl3 == '0':
        action_pl3 = 'getfile_http'

    if tipo_pl3 == '1':
        action_pl3 = 'plx_items'

    title_pl1 = plugintools.get_setting("title_pl1")
    title_pl2 = plugintools.get_setting("title_pl2")
    title_pl3 = plugintools.get_setting("title_pl3")

    plugintools.add_item(action="", title='[COLOR lightyellow]Listas online:[/COLOR]', url="", folder=False, isPlayable=False)

    if url_pl1 != "":
        if title_pl1 == "":
            title_pl1 = "[COLOR lightyellow]Lista online 1[/COLOR]"
        plugintools.add_item(action=action_pl1, title='  '+title_pl1, url=url_pl1, folder=True, isPlayable=False)

    if url_pl2 != "":
        if title_pl2 == "":
            title_pl2 = "[COLOR lightyellow]Lista online 2[/COLOR]"
        plugintools.add_item(action=action_pl2, title='  '+title_pl2, url=url_pl2, folder=True, isPlayable=False)

    if url_pl3 != "":
        if title_pl3 == "":
            title_pl3 == "[COLOR lightyellow]Lista online 3[/COLOR]"
        plugintools.add_item(action=action_pl3, title='  '+title_pl3, url=url_pl3, folder=True, isPlayable=False)


####### Menú lateral ###############


##################################MENU LATERAL######################
class menulateral(xbmcgui.WindowXMLDialog):

    C_CHANNELS_LIST = 6000

    def __init__( self, *args, **kwargs ):
            xbmcgui.WindowXML.__init__(self)
            #self.finalurl = kwargs[ "finalurl" ]
            #self.siglacanal = kwargs[ "siglacanal" ]
            #self.name = kwargs[ "name" ]
            #self.directo = kwargs[ "directo" ]

    def onInit(self):
        self.updateChannelList()

    def onAction(self, action):
        if action.getId() in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, KEY_NAV_BACK, KEY_CONTEXT_MENU]:
            self.close()
            return

    def onClick(self, controlId):
        if controlId == 4001:
            self.close()
            request_servidores(url,name)

        elif controlId == 40010:
            self.close()
            iniciagravador(self.finalurl,self.siglacanal,self.name,self.directo)

        elif controlId == 203:
            #xbmc.executebuiltin("XBMC.PlayerControl(stop)")
            self.close()

        elif controlId == 6000:
            listControl = self.getControl(self.C_CHANNELS_LIST)
            item = listControl.getSelectedItem()
            nomecanal=item.getProperty('chname')
            self.close()
            request_servidores(url,nomecanal)


        #else:
        #    self.buttonClicked = controlId
        #    self.close()

    def onFocus(self, controlId):
        pass

    def updateChannelList(self):
        idx=-1
        listControl = self.getControl(self.C_CHANNELS_LIST)
        listControl.reset()
        canaison=openfile('canaison')
        canaison=canaison.replace('[','')
        lista=re.compile('B](.+?)/B]').findall(canaison)
        for nomecanal in lista:
            idx=int(idx+1)
            if idx==0: idxaux=' '
            else:
                idxaux='%4s.' % (idx)
                item = xbmcgui.ListItem(idxaux + ' %s' % (nomecanal), iconImage = '')
                item.setProperty('idx', str(idx))
                item.setProperty('chname', '[B]' + nomecanal + '[/B]')
                listControl.addItem(item)

    def updateListItem(self, idx, item):
        channel = self.channelList[idx]
        item.setLabel('%3d. %s' % (idx+1, channel.title))
        item.setProperty('idx', str(idx))

    def swapChannels(self, fromIdx, toIdx):
        if self.swapInProgress: return
        self.swapInProgress = True

        c = self.channelList[fromIdx]
        self.channelList[fromIdx] = self.channelList[toIdx]
        self.channelList[toIdx] = c

        # recalculate weight
        for idx, channel in enumerate(self.channelList):
            channel.weight = idx

        listControl = self.getControl(self.C_CHANNELS_LIST)
        self.updateListItem(fromIdx, listControl.getListItem(fromIdx))
        self.updateListItem(toIdx, listControl.getListItem(toIdx))

        listControl.selectItem(toIdx)
        xbmc.sleep(50)
        self.swapInProgress = False

    def addLink(name,url,iconimage):
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
        try:
            if re.search('HD',name) or re.search('1080P',name) or re.search('720P',name):liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 1280, 'height': 720 } )
            else: liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 600, 'height': 300 } )
        except: pass
        return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

    def addCanal(name,url,mode,iconimage,total,descricao):
        cm=[]
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&thumb="+urllib.quote_plus(iconimage)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "overlay":6 ,"plot":descricao} )
        liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
        try:
            if re.search('HD',name) or re.search('1080P',name) or re.search('720P',name):liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 1280, 'height': 720 } )
            else: liz.addStreamInfo( 'video', { 'Codec': 'h264', 'width': 600, 'height': 300 } )
        except: pass
        #cm.append(('Adicionar stream preferencial', "XBMC.RunPlugin(%s?mode=%s&name=%s&url=%s)")%(sys.argv[0],)
        liz.addContextMenuItems(cm, replaceItems=False)
        return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=total)

    def addDir(name,url,mode,iconimage,total,descricao,pasta):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "overlay":6 ,"plot":descricao} )
        liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
        return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

    def clean(text):
        command={'\r':'','\n':'','\t':'','&nbsp;':''}
        regex = re.compile("|".join(map(re.escape, command.keys())))
        return regex.sub(lambda mo: command[mo.group(0)], text)

    def parseDate(dateString):
        try: return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
        except: return datetime.datetime.today() - datetime.timedelta(days = 1) #force update



# Pruebas EPG flotante en modo reproducción
def testejanela(params):
    d = menulateral("menulateral.xml" , home, "Default")
    while xbmc.getCondVisibility('Window.IsActive(videoosd)') == False:
        xbmc.sleep(1000)
        if xbmc.getCondVisibility('Window.IsActive(videoosd)'):
            d.doModal()
        else:
            pass


def launch_kickass(params):
    plugintools.log('[%s %s].launch_kickass %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    addon_magnet = plugintools.get_setting("addon_magnet")
    if addon_magnet == "0":  # Stream (por defecto)
        url = 'plugin://plugin.video.stream/play/'+url
    elif addon_magnet == "1":  # Pulsar
        url = 'plugin://plugin.video.pulsar/play?uri=' + url

    play(url)


def open_settings(self):  #Open addon settings    
    selfAddon.openSettings()
    params = plugintools.get_params()
    main_list(params)

    

def cbx_reader(params):
    plugintools.log('[%s %s].CBX_reader %s' % (addonName, addonVersion, repr(params)))
    mediafire = 0;fanart = "";thumbnail="";
    url = params.get("url")
    datamovie = {}
    datamovie["plot"] = params.get("plot")
    url_fixed = url.split("/");num_splits = int(len(url_fixed)) - 1
    filename = url_fixed[num_splits].replace("download?e=", "")[0:20]
    print filename
    title = params.get("title")
    title = parser_title(title).strip()
    filename = filename.replace(".cbz","").replace(".cbr", "").replace("?", "").replace("+", "").replace(" ", "_").strip()
    if params.get("extra") == "my_albums":  # Control para abrir álbumes desde "My albums"
        plugintools.log("Extra!")
        dst_folder = temp + title
        mediafire = 0
        if title.endswith("cbr") == True:
            filename = filename.replace(".cbr", "")
        elif title.endswith("cbz") == True:
            filename = filename.replace(".cbz", "")
        dst_folder = playlists + title
        dst_folder = dst_folder.replace(" ", "_").strip()
        print 'dst_folder 6655',dst_folder
        if url.endswith("cbr") == True:
            filename = filename+'.cbr'              
        elif url.endswith("cbz") == True:
            filename = filename+'.cbz'
        print os.path.exists(dst_folder)
        if os.path.exists(dst_folder) == "False":        
            plugintools.log("Creando directorio... "+dst_folder)
            os.mkdir(dst_folder)
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)
        src_cbx = temp + title
        print 'src 6668',src_cbx
        print 'dst 6669',dst_folder
        
    else:  # Control para abrir álbumes desde una lista M3U
        dst_folder = temp + filename
        dst_folder = dst_folder.replace(" ", "_").strip()
        dst_folder = dst_folder.replace("?", "").replace("%", "").replace("download=1", "").strip()
        print 'dst_folder 6675',dst_folder
        if url.endswith("cbr") == True:
            filename = filename+'.cbr'              
        elif url.endswith("cbz") == True:
            filename = filename+'.cbz'
        elif url.find("copy.com") >= 0:
            filename = filename.replace("?", "").replace("download=1", "").replace("%", "").strip()
            if url.find("cbz") >= 0:
                filename = filename+'.cbz'
            elif url.find("cbr") >= 0:
                filename = filename+'.cbr'
        if os.path.exists(dst_folder) == "False":        
            plugintools.log("Creando directorio... "+dst_folder)
            os.mkdir(dst_folder)
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)
        src_cbx = temp + filename
        print 'src 6441',src_cbx
        print 'dst 6442',dst_folder
    
    if url.find("mediafire") >= 0:  # ***************** MEDIAFIRE *****************
        plugintools.log("Iniciando descarga de Mediafire")
        src_cbx = temp + filename+'.cbr'  # ExtensiÃ³n .rar para que no salte iteraciÃ³n posterior de url.endswith("url") == True en linea 6223

        # Solicitud de página web
        mediafire = 1
        url = params.get("url")
        data = plugintools.read(url)

        # Espera un segundo y vuelve a cargar
        percent = 0
        progreso = xbmcgui.DialogProgress()
        progreso.create("PalcoTV", "Iniciando descarga de [I]Mediafire[/I] en [I][B]playlists/tmp[/B][/I]\n")
        msg = "Obteniendo URL de descarga...\n"
        percent = 25
        progreso.update(percent, "", msg, "")        

        time.sleep(1)  # Espera de 1 seg para obtener URL de Mediafire...
        plugintools.log("Iniciando lectura de "+url)
        data = plugintools.read(url)
        url_mediafire = plugintools.find_single_match(data, 'kNO \= "([^"]+)"')
        plugintools.log("URL Mediafire 1= "+url_mediafire)
        if url_mediafire == "":
            time.sleep(1)
            data = plugintools.read(url)
            matches = plugintools.find_multiple_matches(data, 'kNO \= "([^"]+)"')
            for entry in matches:
                plugintools.log("entry= "+entry)
                if entry != "":
                    url_mediafire = entry
                    plugintools.log("URL Mediafire 2= "+url_mediafire)                    
                    msg = "URL Mediafire: [I]"+url_mediafire+"[/I]\n Iniciando descarga..."
                    percent = 50
                    progreso.update(percent, "", msg, "")

        # Comprobamos si no existe el archivo ya descargado e iniciamos descarga...
        if os.path.isfile(src_cbx) is False:
            msg = "Leyendo datos de: [I]"+url_mediafire+"[/I]\n"
            percent = 50
            progreso.update(percent, "", msg, "")            
            response = urllib2.urlopen(url_mediafire)
            body = response.read()
            file_compressed = filename + '.cbr'
            fh = open(temp + file_compressed, "wb")  #open the file for writing
            fh.write(body)  # read from request while writing to file

            # Thumbnail y fanart
            thumbnail = params.get("thumbnail")
            if thumbnail == "":
                thumbnail = dst_folder+'\\00.jpg'
                if thumbnail == "":
                    thumbnail = 'http://ww1.prweb.com/prfiles/2010/07/13/3676844/Slideshow512.png'        
            fanart = dst_folder+'\\00.jpg'
            plugintools.log("fanart1= "+fanart)
            if fanart == "":
                fanart = dst_folder+'\\00.jpg'
                plugintools.log("fanart2= "+fanart)
                if fanart == "":
                    fanart = art+'slideshow.png'
                    plugintools.log("fanart3= "+fanart)
        else:
            msg = "Archivo ya descargado. Abriendo páginas... "
            percent = 75
            progreso.update(percent, "", msg, "")
            mediafire = 1

    elif url.endswith("cbz") == True or url.endswith("cbr") == True or url.find("copy.com") >= 0:  # *** Descarga de archivos CBR y CBZ ***
        plugintools.log("Iniciando descarga de Dropbox/Copy.com")
        if os.path.isfile(src_cbx) is False:
            percent = 0
            progreso = xbmcgui.DialogProgress()
            if url.endswith("cbz") == True:
                progreso.create("PalcoTV", "Descargando archivo CBZ en [I][B]playlists/tmp[/B][/I]")
            elif url.endswith("cbr") == True:
                progreso.create("PalcoTV", "Descargando archivo CBR en [I][B]playlists/tmp[/B][/I]")
            elif url.find("copy.com") >= 0:
                if url.find("cbr") >= 0:
                    progreso.create("PalcoTV", "Descargando archivo CBR de Copy.com en [I][B]playlists/tmp[/B][/I]")
                elif url.find("cbz") >= 0:
                    progreso.create("PalcoTV", "Descargando archivo CBZ de Copy.com en [I][B]playlists/tmp[/B][/I]")
            # response = urllib2.urlopen(url)
            # body = response.read()
            if url.startswith("cbr:") == True:
                url = url.replace("cbr:", "")
                #filename = filename + '.cbr'
                plugintools.log("Iniciando descarga desde..."+url)
            elif url.startswith("cbz:") == True:
                url = url.replace("cbz:", "")
                #filename = filename + '.cbz'
                plugintools.log("Iniciando descarga desde..."+url)            
            h=urllib2.HTTPHandler(debuglevel=0)  # Iniciamos descarga...
            request = urllib2.Request(url)
            opener = urllib2.build_opener(h)
            urllib2.install_opener(opener)

            fh = open(temp + filename, "wb")  #open the file for writing
            size_local = fh.tell()            
            try:
                connected = opener.open(request)
                meta = connected.info()
                filesize = meta.getheaders("Content-Length")[0]
                filesize_mb = str(int(filesize) / 1024000) + " MB"                
                try:
                    while int(size_local) < int(filesize):
                        blocksize = 100*1024
                        bloqueleido = connected.read(blocksize)                        
                        if progreso.iscanceled():
                            progreso.close()
                            fh.close()
                        msg = "[COLOR gold][B]"+filename+"[/B][/COLOR][COLOR lightgreen][I] ("+filesize_mb+")[/I][/COLOR]\n"+str(size_local)+" de "+str(filesize)+" bytes\n"
                        #print filesize
                        #print size_local
                        percent_fixed = float((float(size_local) * 100)/(float(filesize) * 100) * 100)
                        percent = int(percent_fixed)
                        progreso.update(percent, "" , msg, "")
                        fh.write(bloqueleido)  # read from request while writing to file
                        size_local = fh.tell()                        
                except:
                    percent = 100
                    progreso.update(percent)
                    
            except urllib2.HTTPError,e:
                progreso.close()
                fh.close()
                
            fh.close()
            progreso.close()
    
    page = 1
    if src_cbx.endswith("cbz") == True:  # Descompresión archivos CBZ
        #unzipper = ziptools()
        #unzipper.extract(src_cbx, dst_folder, params)
        print src_cbx
        print dst_folder
        xbmc.executebuiltin('XBMC.Extract('+src_cbx+','+dst_folder+')')
        xbmc.sleep(1000)
        thumbnail = params.get("thumbnail")
        if thumbnail == "":
            thumbnail = dst_folder+'\\00.jpg'
            if thumbnail == "":
                thumbnail = 'http://ww1.prweb.com/prfiles/2010/07/13/3676844/Slideshow512.png'        
        fanart = dst_folder+'\\00.jpg'
        plugintools.log("fanart1= "+fanart)
        if fanart == "":
            fanart = dst_folder+'\\00.jpg'
            plugintools.log("fanart2= "+fanart)
            if fanart == "":
                fanart = art+'slideshow.png'
                plugintools.log("fanart3= "+fanart)

    elif src_cbx.endswith("cbr") == True:  # DescompresiÃ³n archivos CBR
        xbmc.executebuiltin('XBMC.Extract('+src_cbx+','+dst_folder+')')
        xbmc.sleep(1000)
        thumbnail = params.get("thumbnail")
        if thumbnail == "":
            thumbnail = dst_folder+'\\00.jpg'
            if thumbnail == "":
                thumbnail = 'http://ww1.prweb.com/prfiles/2010/07/13/3676844/Slideshow512.png'        
        fanart = dst_folder+'\\00.jpg'
        plugintools.log("fanart1= "+fanart)
        if fanart == "":
            fanart = dst_folder+'\\00.jpg'
            plugintools.log("fanart2= "+fanart)
            if fanart == "":
                fanart = art+'slideshow.png'
                plugintools.log("fanart3= "+fanart)
        if mediafire == 1:
            percent = 100
            msg = "Proceso finalizado! ;)"
            progreso.update(percent, "", msg, "")
            fh.close()
            progreso.close()   

    # Abriendo páginas...
    plugintools.add_item(action="show_cbx", title="[COLOR orange][B]Ayuda: [/COLOR][COLOR white]Atajos de teclado[/B][/COLOR]", url=art+'help_cbx.png', info_labels = datamovie , thumbnail = art+'help_cbx.png', fanart = fanart, folder=False, isPlayable=False)    
    plugintools.add_item(action="slide_cbx", title="[COLOR orange][B]Slideshow: [/COLOR][COLOR white]"+title+"[/B][/COLOR]", url=dst_folder, page=str(page), extra=dst_folder , info_labels = datamovie , thumbnail = thumbnail, fanart = fanart, folder=False, isPlayable=False)    
    plugintools.log("dst_folder= "+dst_folder)
    for f in os.listdir(dst_folder):
        file_path = os.path.join(dst_folder, f)
        print dst_folder+f
        if os.path.isfile(file_path):
            thumbnail = cbx_pages+str(page)+'.png'
            plugintools.addShow(action="show_cbx", title="Página "+str(page), url=dst_folder+'\\'+f, page=str(page), extra=dst_folder , info_labels = datamovie , thumbnail = dst_folder+'\\'+f, fanart = dst_folder+'\\'+f , folder=False, isPlayable=False)
            page = page + 1     
                    
    #xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Descompresión fallida", 3 , art+'icon.png'))


    # os.remove(temp + filename)  # Habilitar opciÃ³n en la configuraciÃ³n para borrar el archivo descargado
    # xbmc.executebuiltin("Container.SetViewMode(500)")
    # text = 'plugin://plugin.image.pdfreader/?mode=100&name='+title+'&url='+playlist+filename
    # runPlugin(text)


	
def slide_cbx(params):
    plugintools.log('[%s %s].slide_CBX %s' % (addonName, addonVersion, repr(params)))
    #xbmc.executebuiltin("Container.SetViewMode(500)")
    url = params.get("url")
    dst_folder = params.get("extra")
    page = params.get("page")
    plugintools.log("url= "+url)
    page_to_start = dst_folder + '\\'+str(page)
    xbmc.executebuiltin( "SlideShow("+dst_folder+"," +page+")" )
    


def show_cbx(params):
    plugintools.log('[%s %s].show_CBX %s' % (addonName, addonVersion, repr(params)))
    #xbmc.executebuiltin("Container.SetViewMode(500)")
    url = params.get("url")
    dst_folder = params.get("extra")
    page = params.get("page")
    plugintools.log("url= "+url)
    page_to_start = dst_folder + '\\'+str(page)    
    xbmc.executebuiltin( "ShowPicture("+url+")" )    
    

def show_image(params):
    plugintools.log('[%s %s].show_image %s' % (addonName, addonVersion, repr(params)))
    url=params.get("url")
    url = url.replace("img:", "")

    plugintools.log("Iniciando descarga desde..."+url)
    h=urllib2.HTTPHandler(debuglevel=0)  # Iniciamos descarga...
    request = urllib2.Request(url)
    opener = urllib2.build_opener(h)
    urllib2.install_opener(opener)
    filename = url.split("/")
    max_len = len(filename)
    max_len = int(max_len) - 1
    filename = filename[max_len]
    fh = open(temp + filename, "wb")  #open the file for writing
    connected = opener.open(request)
    meta = connected.info()
    filesize = meta.getheaders("Content-Length")[0]
    size_local = fh.tell()
    print 'filesize',filesize
    print 'size_local',size_local
    while int(size_local) < int(filesize):
        blocksize = 100*1024
        bloqueleido = connected.read(blocksize)
        fh.write(bloqueleido)  # read from request while writing to file
        size_local = fh.tell()
        print 'size_local',size_local
    imagen = temp + filename
    print imagen
    xbmc.executebuiltin( "ShowPicture("+imagen+")" )  


def devil_call(params):
    plugintools.log("[%s %s] devil_call " % (addonName, addonVersion))
    
    url = params.get("url")
    url = xbmc.executebuiltin('XBMC.RunPlugin('+url+')')
    print url
    plugintools.play_resolved_url(url)
    

def load_skin(params):
    plugintools.log('[%s %s] Load skin... %s' % (addonName, addonVersion, repr(params)))
    mastermenu = params.get("url")
    params["extra"]='load_skin'
    main_list(params)

	
def searchm3u(params):
    plugintools.log("[%s %s] Iniciando búsqueda de canales... %s " % (addonName, addonId, repr(params)))

    # TODO: Revisar error al no introducir texto y cancelar teclado de búsqueda
    
    try:
        term_search = plugintools.get_setting("term_search")        
        texto = plugintools.keyboard_input(term_search)
        plugintools.set_setting("term_search", texto)    
        while not xbmc.keyboard.is_canceled():
            if texto=="" or len(texto) <= 3: break
    except: pass

    if texto != "":
        
        # Creamos timestamp para guardar archivo de resultados
        formatodia = "%Y-%m-%d";hoy = datetime.today();ts = hoy.strftime(formatodia)
        fsearch = 'search-'+texto+'-'+str(ts)+'.m3u'
                    
        results = open(playlists+fsearch, 'wb');results.seek(0)
        results.write("#EXTM3U,contents:files\n\n")
        ficheros = os.listdir(playlists)
        for lista in ficheros:
            if lista.startswith("000-") == True:  # Solo serán objeto de búsqueda las listas M3U con este nombre de archivo: "000-xxxxx.m3u"
                plugintools.log("Iniciamos búsqueda de canal %s en lista %s " % (texto, lista))
                fm3u = open(playlists + lista, "r");data = fm3u.read();data=data.lower()
                if texto in data:  # Si localiza el texto en esa lista, iniciamos captura de datos
                    plugintools.log("Encontrado canal %s en lista %s " % (texto, lista))
                    fm3u.seek(0);tl=fm3u.readlines();j=len(tl);plugintools.log("j= "+str(j))
                    fm3u.seek(0);linea = fm3u.readline();i=0;linea=linea.lower();plugintools.log("linea= "+linea)
                    while i <= j:
                        if texto in linea:
                            url = fm3u.readline();i = i + 1;plugintools.log("linea= "+linea)
                            if url == '#multi':
                                titulo = linea.split(",")[1].strip() + ' [COLOR lightblue][I]('+lista+')[/I]'
                                plugintools.log("titulo= "+titulo)
                                results.write(titulo+'\n#multi\n')
                                while url != '#multi':
                                    url = fm3u.readline();i = i + 1
                                    results.write(url+'\n')
                                    if linea == '#multi':
                                        results.write("#multi\n\n");continue
                            elif url.startswith("http") == True:
                                plugintools.log("url= "+url)
                                plugintools.log("linea= "+linea)
                                #titulo = linea.split(",")[1].replace(texto, '[B]'+texto+'[/B]') + ' [COLOR lightblue][I]('+lista+')[/I]'
                                titulo = linea.split(",")[1].strip() + ' [COLOR lightblue][I]('+lista+')[/I]';titulo=titulo.replace("\n", "").strip()                        
                                results.write('#EXTINF:-1,'+titulo.strip()+'\n'+url+'\n\n');linea=fm3u.readline();linea=linea.lower();i=i+1;continue  # Ahora que sabemos que existe URL y no está en blanco, escribimos la entrada
                        else: linea = fm3u.readline();linea=linea.lower();plugintools.log("linea= "+linea);i = i + 1;continue
                        
        
        results.close()
        params['ext']='m3u';params['title']=fsearch.replace(".m3u", "").strip()
        m3u_reader(params)
		
    
run()


