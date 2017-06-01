# -*- coding: utf-8 -*-
#-------------------------------------------------------------------
# Módulo de enlaces #multi para PalcoTV
# Kodi Add-on by Juarrox (juarrox@gmail.com)
#-------------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#-------------------------------------------------------------------
# Gracias a la librerías y tutoriales de Jesús (mimediacenter.info)
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
import plugintools

from __main__ import *
from resources.tools.media_analyzer import *

# Regex de EPG
from resources.tools.epg_miguiatv import *
from resources.tools.epg_ehf import *
from resources.tools.epg_arenasport import *
from resources.tools.epg_formulatv import *

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
from resources.regex.janjua import *

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

# Tools & resolvers
from resources.tools.resolvers import *
from resources.tools.mundoplus import *
from resources.tools.bum import *
from resources.tools.yt_playlist import *
from resources.tools.dailymotion import *

# Agenda TV
from resources.tools.felt import *
from resources.tools.agendatv import *
from resources.tools.epg_verahora import *


playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))


def rtmp_analyzer(params):
    plugintools.log('[%s %s] RTMP Analyzer PalcoTV %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")

    if url.startswith("rtmp") == True:
    
        if url.find("freetvcast.pw") >= 0:
            freetvcast(params)  
                    
        elif url.find("http://privado.streamingfreetv.net") >= 0:
            streamingfreetv0(params)  		

        elif url.find("9stream") >= 0:            
            ninestreams(params)

        elif url.find("freebroadcast") >= 0:
            freebroadcast(params)   

        elif url.find("cast247") >= 0:
            castdos(params)

        elif url.find("castalba") >= 0:
            castalba(params)     

        elif url.find("direct2watch") >= 0:
            directwatch(params)
        
        elif url.find("vaughnlive") >= 0:
            resolve_vaughnlive(params)

        elif url.find("shidurlive") >= 0:
            shidurlive(params)      
    
        elif url.find("vercosasgratis") >= 0:
            vercosas(params)

        elif url.find("businessapp1") >= 0:
            businessapp0(params)

        elif url.find("broadcastlive") >= 0:
            broadcastlive0(params)             

        elif url.find("pageUrl=http://rdmcast.com") >= 0:
            rdmcast0(params)

        elif url.find("janjua") >= 0:
            janjua0(params)
            
        else:            
            params["url"]=url            
            plugintools.play_resolved_url(url)

    elif url.startswith("bum") == True or url.startswith("BUM") == True:
        from resources.tools.bum import *
        url = url.strip()
        title = title.replace(" [COLOR lightyellow][I][BUM+][/COLOR]", "").strip()
        params["title"]=title
        params["url"]=url
        get_server(params)
        bum_multiparser(params)
 
    else:
	plugintools.play_resolved_url(url)


def multi_analyzer(params):
    plugintools.log('[%s %s] multi_analyzer %s' % (addonName, addonVersion, repr(params)))
    url = params.get("url");title='[COLOR white]'+params.get("title").replace("[I][Multi][/I]","").strip()+'[/COLOR]';title = multiparse_title(title,url)
    thumbnail = params.get("thumbnail");fanart=params.get("fanart");datamovie={};datamovie["plot"] = params.get("plot")

    if url.startswith("plugin") == True:
        plot = params.get("plot")
        title=params.get("title").replace("[I][Multi][/I]", "").strip()
        plugin_analyzer(url, title, plot, datamovie, thumbnail, fanart)    
 
    elif url.startswith("llamada") == True:
        plot = params.get("plot")
        title=params.get("title")  # .replace("[Multi]", "").strip()
        url = url.replace("llamada:", "")
        comandos = url.split("; ")
        fich_llamada = ruta_llamadas + comandos[0] + ".txt"  # El 1º es el nombre del fichero

        archivo_llamada = open(fich_llamada, "r")
        url_llamada = archivo_llamada.read()
        num_comandos = len(comandos)

        for comando in range(1, num_comandos):  # Empiezo en 1 para saltarme el 1º, q es el nombre del fichero, no un "comando" a reemplazar
            sustituye = plugintools.find_single_match(comandos[comando],'(.*?)=')
            por_este = plugintools.find_single_match(comandos[comando],'=(.*)')
            url_llamada = url_llamada.replace(sustituye, por_este)

        thumbnail=params.get("thumbnail")
        fanart=params.get("fanart")
        plugin_analyzer(url_llamada, title, plot, datamovie, thumbnail, fanart)

    elif url.startswith("bum") == True:
        #title_fixed = multiparse_title(title, url)
        try: min_seeds=url.split("_")[1];
        except: min_seeds=""
        plugintools.addDir(action = "bum_linker" , title = title, url = url.replace("bum:", "").strip(), thumbnail = thumbnail, extra=url.replace("bum:", ""), page=min_seeds, fanart = fanart , folder = True , isPlayable = False )         
        
    elif url.startswith("devil:") == True:
        url = url.replace("devil:", "").replace(" referer=","%26referer=")
        url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+url  # +'%26referer='+referer
        plugintools.add_item(action="runPlugin", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder = False, isPlayable=True)        
        
    # Linkers de películas y series
    elif url.startswith("peli") == True or url.startswith("serie") == True:
        linker,lbl_linker = linker_analyzer(url);url = url.replace("peli:", "");url = url.replace("serie:", "")
        plugintools.add_item(action=linker, title=title, url=url, extra="linker", page=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=True, isPlayable=False)
        
    # Youtube add-on endpoints

    elif url.startswith("yt_playlist") == True:  # Youtube add-on Playlist
        pid = url.replace("yt_playlist(", "").replace(")", "").replace(" ", "").strip()
        url = 'plugin://plugin.video.youtube/playlist/'+pid+'/'
        plugintools.add_item(action="runPlugin", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=True, isPlayable=False)

    elif url.startswith("yt_channel") == True:  # Youtube add-on Channel
        cid = url.replace("yt_channel(", "").replace(")", "").replace(" ", "").strip()
        url = 'plugin://plugin.video.youtube/channel/'+cid+'/'
        plugintools.add_item(action="runPlugin", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=True, isPlayable=False)        
        
    elif url.startswith("yt_user") == True:  # Youtube add-on User
        uid = url.replace("yt_user(", "").replace(")", "").replace(" ", "").strip()
        url = 'plugin://plugin.video.youtube/user/'+uid+'/'
        plugintools.add_item(action="runPlugin", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=True, isPlayable=False)

    elif url.startswith("yt_video") == True:  # Youtube add-on Video
        vid = url.replace("yt_video(", "").replace(")", "").replace(" ", "")
        url = 'plugin://plugin.video.youtube/play/?video_id='+vid
        plugintools.runAddon(action="play", title=title, url=url.strip(), thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=False, isPlayable=True)
          
    elif url.startswith("rtmp") == True or url.startswith("rtsp") == True:
        plugintools.add_item(action="rtmp_analyzer", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=False, isPlayable=True)

    elif url.startswith("pvr://") == True:
        plugintools.add_item( action="runPlugin" , title=title , url=url , thumbnail=thumbnail , fanart=fanart , folder = False , isPlayable = False )     
        
    elif url.startswith("http") == True:
        server = video_analyzer(url)       
           
        if server != "unknown":
            plugintools.add_item(action=server, title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=False, isPlayable=True)
            
        elif url.find("dailymotion.com/video") >= 0:
            video_id = dailym_getvideo(url)
            if video_id != "":
                thumbnail = "https://api.dailymotion.com/thumbnail/video/"+video_id+""
                url = "plugin://plugin.video.dailymotion_com/?url="+video_id+"&mode=playVideo"
                plugintools.add_item(action="dailym_getvideo", title=title, url=url, thumbnail=thumbnail, fanart=params.get("fanart"), info_labels=datamovie, folder=False, isPlayable=True)
                
        elif url.find("dailymotion.com/playlist") >= 0:
            id_playlist = dailym_getplaylist(url)
            if id_playlist != "":
                url = "https://api.dailymotion.com/playlist/"+id_playlist+"/videos"
                thumbnail = "https://api.dailymotion.com/thumbnail/video/"+id_playlist
                if thumbnail == "":
                    thumbnail = 'http://press.dailymotion.com/wp-old/wp-content/uploads/logo-Dailymotion.png'
                url = "https://api.dailymotion.com/playlist/"+id_playlist+"/videos"
                plugintools.add_item(action="dailym_pl", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=True, isPlayable=False)

        elif url.find("vimeo.com") >= 0:  # Vimeo
            if url.find("vimeo.com/channels") >= 0:
                plugintools.addDir( action = "vimeo_pl" , title = title, url = url ,  thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
            else:
                plugintools.addShow( action = "vimeo" , title = title, url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                
        elif url.find("https://www.youtube.com/watch?") >= 0:
            plot = params.get("plot")
            title=params.get("title").replace("[I][Multi][/I]", "").strip()
            videoid = url.replace("https://www.youtube.com/watch?v=", "")
            url = 'plugin://plugin.video.youtube/play/?video_id='+videoid
            plugin_analyzer(url, title, plot, datamovie, thumbnail, fanart)                
                
        elif url.find(".m3u8") >= 0:
            plugintools.add_item(action="play", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=False, isPlayable=True)

        else:
            plugintools.add_item(action="play", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=False, isPlayable=True)
            
    elif url.startswith("udp") == True:
        plugintools.add_item(action="play", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=False, isPlayable=True)
    
    elif url.startswith("rtp") == True:
        plugintools.add_item(action="play", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=False, isPlayable=True)
        
    elif url.startswith("mms") == True:
        plugintools.add_item(action="play", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=False, isPlayable=True)
            
    elif url.startswith("sop") == True:
        # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
        url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=2&name='
        plugintools.add_item(action="play", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=False, isPlayable=False)
        
    elif url.startswith("ace") == True:
        url = url.replace("ace:", "")
        url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=1&name='
        plugintools.add_item(action="play", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=False, isPlayable=False)
    
    elif url.startswith("short") == True:
        url = url.replace("short:", "").strip()                
        plugintools.add_item(action="longurl", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=True, isPlayable=False)                

    elif url.startswith("devil") == True:
        url_devil = url.replace("devil:", "").replace(" referer=","%26referer=")
        url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+url_devil  # +'%26referer='+referer
        #xbmc.executebuiltin('XBMC.RunPlugin(' + url +')')
        plugintools.add_item(action="runPlugin", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=False, isPlayable=False)
        
    elif url.startswith("bum") == True:
        plugintools.add_item(action="bum_multiparser", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=True, isPlayable=False)

    elif url.startswith("txt") == True:
        from resources.tools.txt_reader import *
        url=url.replace("txt:", "")
        plugintools.add_item(action="txt_reader", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=False, isPlayable=False)

    elif url.startswith("epg-txt") == True:
        from resources.tools.epg_txt import *
        url=url.replace("epg-txt:", "")
        url = epg_txt_dict(parser_title(url))
        plugintools.add_item(action="epg_txt0", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=False, isPlayable=False)                

    elif url.startswith("agendatv") == True:
        url = url.replace("agendatv:", "").strip()
        if url.startswith("futbolenlatv") == True:
            if url.endswith("futbol") == True: url='http://www.futbolenlatv.com/deporte/futbol'
            elif url.endswith("futsal") == True: url='http://www.futbolenlatv.com/deporte/futbol-sala'
            elif url.endswith("baloncesto") == True: url='http://www.futbolenlatv.com/deporte/baloncesto'
            elif url.endswith("balonmano") == True: url='http://www.futbolenlatv.com/deporte/balonmano'
            elif url.endswith("motociclismo") == True: url='http://www.futbolenlatv.com/deporte/motociclismo'
            elif url.endswith("automovilismo") == True: url='http://www.futbolenlatv.com/deporte/automovilismo'
            elif url.endswith("amfutbol") == True: url='http://www.futbolenlatv.com/deporte/futbol-americano'
            elif url.endswith("tenis") == True: url='http://www.futbolenlatv.com/deporte/tenis'
            elif url.endswith("rugby") == True: url='http://www.futbolenlatv.com/deporte/rugby'
            elif url.endswith("ciclismo") == True: url='http://www.futbolenlatv.com/deporte/ciclismo'
            elif url.endswith("todos") == True: url='http://www.futbolenlatv.com/deporte'
            plugintools.add_item(action="feltv0", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=False, isPlayable=False)                    
        elif url == "footballonuktv":
            url = 'http://www.footballonuktv.com/'
            plugintools.add_item(action="agendatv", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=False, isPlayable=False)                                        
        elif url == "calciointv":
            url = 'http://www.calciointv.com/'
            plugintools.add_item(action="agendatv", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=False, isPlayable=False)                                        
        elif url == "futbolenlatele":
            url = 'http://www.futbolenlatele.com'
            plugintools.add_item(action="agendatv", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=False, isPlayable=False)                                        
        elif url == "queverahora":
            url = 'http://www.formulatv.com/programacion/'
            plugintools.add_item(action="epg_verahora", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=False, isPlayable=False)                    
        else:
            plugintools.add_item(action="play", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=True, isPlayable=False)                    

    elif url.startswith("torrent") == True:
        url = p2p_builder_url(url, title, p2p="torrent")
        plugintools.add_item(action="launch_torrent", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=False, isPlayable=True)

    elif url.startswith("magnet") == True:
        url = p2p_builder_url(url, title, p2p="magnet")
        plugintools.add_item(action="launch_magnet", title=title, url=url, thumbnail=thumbnail, fanart=fanart, info_labels=datamovie, folder=False, isPlayable=True)
    
    elif url == "mundoplus":
        plugintools.add_item(action="mundoplus_guide", title=title, url=url, thumbnail=thumbnail, fanart=fanart, page=params.get("page"), info_labels=datamovie, folder=True, isPlayable=False)
    
    elif url.startswith("goear") == True:
        id_goear = url.replace("goear:", "").replace('"', "").strip()
        url = 'http://www.goear.com/action/sound/get/'+id_goear
        plugintools.add_item(action="play", title=title, url=url, thumbnail=thumbnail, fanart=fanart, extra="regex", info_labels=datamovie, folder=True, isPlayable=False)

    else:
        plugintools.add_item(action="play", title=title, url=url, thumbnail=thumbnail, fanart=fanart, extra="regex", info_labels=datamovie, folder=True, isPlayable=False)
        

def youtube_playlists(url):
    plugintools.log('[%s %s].youtube_playlists %s' % (addonName, addonVersion, url))	
    
    data = plugintools.read(url)
        
    pattern = ""
    matches = plugintools.find_multiple_matches(data,"<entry(.*?)</entry>")
    
    for entry in matches:       
        title = plugintools.find_single_match(entry,"<titl[^>]+>([^<]+)</title>")
        plot = plugintools.find_single_match(entry,"<media\:descriptio[^>]+>([^<]+)</media\:description>")
        thumbnail = plugintools.find_single_match(entry,"<media\:thumbnail url='([^']+)'")           
        url = plugintools.find_single_match(entry,"<content type\='application/atom\+xml\;type\=feed' src='([^']+)'/>")
        fanart = art + 'youtube.png'
        
        plugintools.add_item( action="youtube_videos" , title=title , plot=plot , url=url , thumbnail=thumbnail , fanart=fanart , folder=True )        


# Muestra todos los vídeos del playlist de Youtube
def youtube_videos(url):
    plugintools.log('[%s %s].youtube_videos %s' % (addonName, addonVersion, url))	
    
    # Fetch video list from YouTube feed
    data = plugintools.read(url)
    
    # Extract items from feed
    pattern = ""
    matches = plugintools.find_multiple_matches(data,"<entry(.*?)</entry>")
    
    for entry in matches:
        # Not the better way to parse XML, but clean and easy
        title = plugintools.find_single_match(entry,"<titl[^>]+>([^<]+)</title>")
        title = title.replace("I Love Handball | ","")
        plot = plugintools.find_single_match(entry,"<summa[^>]+>([^<]+)</summa")
        thumbnail = plugintools.find_single_match(entry,"<media\:thumbnail url='([^']+)'")
        fanart = art+'youtube.png'
        video_id = plugintools.find_single_match(entry,"http\://www.youtube.com/watch\?v\=([0-9A-Za-z_-]{11})")
        url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+video_id

        # Appends a new item to the xbmc item list
        plugintools.add_item( action="play" , title=title , plot=plot , url=url , thumbnail=thumbnail , fanart=fanart , isPlayable=True, folder=False )


def parse_url(url):
    if url != "":
        url = url.strip()
        url = url.replace("rtmp://$OPT:rtmp-raw=", "")        
        return url
    
    else:
        plugintools.log("error en url= ")  # Mostrar diálogo de error al parsear url (por no existir, por ejemplo)


def multilink(params):
    plugintools.log('[%s %s] PalcoTV Multilink %s' % (addonName, addonVersion, repr(params)))
    dialog = xbmcgui.Dialog()
    filename = params.get("extra")
    file = open(playlists + filename, "r")
    file.seek(0)
    title = params.get("title")
    title_parsed = parser_title(params.get("title"))
    if title.find("  ") >= 0:
        title = "@"+title.split("  ")[0].strip()  # En la lista aparecerá el título precedido por el símbolo @
    if title.startswith("[COLOR white]") == True:
        title_fixed=title[13:].strip()
        encuentra = '#EXTINF:-1,' + title_fixed.replace("[COLOR lightyellow][I][Multi][/I][/COLOR]","").strip()
    else:
        encuentra = '#EXTINF:-1,' + title.replace("[COLOR lightyellow][I][Multi][/I][/COLOR]","").strip()
    if encuentra.startswith("#EXTINF:-1,@") == True:
        title_epg = title.replace("[COLOR white]","").split("[COLOR orange")
        if len(title_epg) >= 1:
            title_epg = title_epg[0]
        encuentra = '#EXTINF:-1,'+title_epg;encuentra=encuentra.strip()
    #plugintools.log("*** Texto a buscar= "+encuentra)
    i = 0
    data = file.readline()
    if data.startswith("#EXTINF:-1,@") == True:
        epg_no = plugintools.get_setting("epg_no")        
        if epg_no == "0":  # No desactivado EPG
            pass
        else:
            data = data.replace("@", "")
    encuentra = encuentra.replace("@", "")    
    while i <=8:  # Control para EOF
        if data == "":
            i = i + 1
            data = file.readline().strip()
            if data.startswith("#EXTINF:-1,@") == True:
                data = data.replace("@", "")
            continue
        else:
            i = 0
            #plugintools.log("A buscar: "+encuentra)
            #plugintools.log("Leyendo... "+data)
            if data.startswith(encuentra) == True or data.startswith('#EXTINF:-1,@' + title.replace(" [COLOR lightyellow][I][Multi][/I][/COLOR]","")) == True:
                data = file.readline().strip()
                if data == "#multi" or data == "#multilink":
                    title_options = []
                    url_options = []
                    thumb_options = []
                    fanart_options = []
                    sinopsis_options = []
                    #Leemos número de enlaces
                    i = 1  # Variable contador desde 1 porque nos servirá para nombrar los títulos
                    # Recopilamos enlaces en una lista
                    linea_url = file.readline().strip()
                    if linea_url.startswith("desc") == True:
                        linea_url = file.readline().strip()                        
                    while linea_url != "#multi" :
                        linea_url = linea_url.strip().split("$")
                        subcomas = len(linea_url)  # Parche para enlaces con comas (Stalker, Livestreamspro, etc)
                        thumb_option = params.get("thumbnail")
                        fanart_option = params.get("fanart")
                        sinopsis_option = params.get("plot")
                        # Soporte de sinopsis y thumbnail en subitems de #multi (08/02/2016) y soporte de sinopsis y fanart en #multi (08/04/2016)
                        print 'subcomas',subcomas
                        if subcomas == 5: sinopsis_option = linea_url[4];fanart_option = linea_url[3];thumb_option = linea_url[2];url_option = linea_url[1]
                        elif subcomas == 4: fanart_option = linea_url[3];thumb_option = linea_url[2];url_option = linea_url[1]
                        elif subcomas == 3: url_option = linea_url[1];thumb_option = linea_url[2]  
                        elif subcomas == 2: url_option = linea_url[1]
                        else:
                            url_option = linea_url[1:subcomas]
                            print 'url_option',url_option
                            i = 0;hurl=""
                            for item in url_option:
                                if hurl == "":
                                    hurl = url_option[i]
                                else:
                                    hurl=hurl+'$'+url_option[i].strip()
                                i = i + 1
                                #plugintools.log("#multi: "+hurl)
                                url_option=hurl  # Fin del parche para enlaces con comas (plugin://)
                        # Control para imágenes en blanco (se cargan imágenes por defecto del #multi). Ejemplo: Título$URL$$$Sinopsis
                        if thumb_option=="": thumb_option = params.get("thumbnail")
                        if fanart_option=="": fanart_option = params.get("fanart")
                        title_option = linea_url[0]                        
                        if title_option.startswith("@") == True:
                            title_option = title_option.replace("@", "")
                            # Ejecutamos EPG...
                            epg_channel = []
                            epg_channel = epg_now(title_option)
                            if epg_now(title_option) == False:
                                pass
                            else:
                                try:
                                    ejemplo = epg_channel[0]
                                    title_option = title_option + " [COLOR orange][I][B] " + epg_channel[0] + "[/B] " + epg_channel[1] + "[/I][/COLOR] "
                                    num_items = i - 1
                                    if title.startswith("@") == True:  # Para evitar que en el título del cuadro de diálogo aparezca el nombre del canal precedido por el símbolo arroba (@)
                                        title = title.replace("@","")

                                except:
                                    pass
                                
                        i = i + 1
                        title_options.append(title_option)
                        url_options.append(url_option)
                        thumb_options.append(thumb_option)
                        fanart_options.append(fanart_option)
                        sinopsis_options.append(sinopsis_option)
                        linea_url = file.readline()
                        linea_url = linea_url.strip()

                #try:
                i = 0
                datamovie={}
                datamovie["Plot"]=params.get("plot")
                plot=params.get("plot")
                for item in title_options:
                    params["url"] = url_options[i]
                    params["title"]=title_options[i]
                    params["thumbnail"] = thumb_options[i]
                    params["fanart"]=fanart_options[i]
                    params["plot"]=sinopsis_options[i]
                    fanart=params.get("fanart")                        
                    datamovie["plot"]=plot
                    params["page"]=parser_title(title).strip()
                    multi_analyzer(params)
                    i = i + 1
                        
                #except KeyboardInterrupt: pass;
                #except IndexError: raise;
            else:
                data = file.readline().strip()        


# Esta función añade coletilla de tipo de enlace a los multilink
def multiparse_title(title, url):
    if url == "mundoplus":
        title = title + ' [COLOR lightyellow][I][Guía[B]TV[/B]][/I][/COLOR]'

    elif url.startswith("yt") == True:
        if url.startswith("yt_playlist") == True:
            title = title + ' [COLOR lightyellow][I] [You[B]Tube[/B] Playlist][/I][/COLOR]'

        elif url.startswith("yt_channel") == True:
            title = title + ' [COLOR lightyellow][I] [You[B]Tube[/B] Channel][/I][/COLOR]'

        elif url.startswith("yt_user") == True:
            title = title + ' [COLOR lightyellow][I] [You[B]Tube[/B] User][/I][/COLOR]'

        elif url.startswith("yt_video") == True:
            title = title + ' [COLOR lightyellow][I] [You[B]Tube[/B] Video][/I][/COLOR]'          

        elif url.startswith("pvr") == True:
            title = title + ' [COLOR lightyellow][I][PVR][/I][/COLOR]'

    elif url.startswith("bum") == True:
        try: min_seeds=url.split("_")[1];title=title + ' [COLOR lightyellow][I][BUM:[B]'+min_seeds+'[/B]][/I][/COLOR]'
        except: title = title + ' [COLOR lightyellow][I][BUM+][/I][/COLOR]'            

    elif url.startswith("peli") == True:
        if url.find("oranline") >= 0:
            title = title + ' [COLOR lightyellow][I][Oranline][/I][/COLOR]'
        elif url.find("pelisadicto") >= 0:
            title = title + ' [COLOR lightyellow][I][PelisAdicto][/I][/COLOR]'
        elif url.find("pordede") >= 0:
            title = title + ' [COLOR lightyellow][I][Pordede][/I][/COLOR]'
        elif url.find("openload") >= 0:
            title = title + ' [COLOR lightyellow][I][Openload][/I][/COLOR]'
        elif url.find("hdfull.tv") >= 0:
            title = title + ' [COLOR lightyellow][I][HDFull][/I][/COLOR]'
        elif url.find("tv-vip.com") >= 0:
            title = title + ' [COLOR lightyellow][I][TV-VIP][/I][/COLOR]'
        elif url.find("inkapelis") >= 0:
            title = title + ' [COLOR lightyellow][I][Inkapelis][/I][/COLOR]'
        elif url.find("descargacineclasico") >= 0:
            title = title + ' [COLOR lightyellow][I][DescargaCineClásico][/I][/COLOR]'
        elif url.find("danko") >= 0:
            title = title + ' [COLOR lightyellow][I][PelisDanko][/I][/COLOR]'
        elif url.find("peliculasdk") >= 0:
            title = title + ' [COLOR lightyellow][I][PeliculasDK][/I][/COLOR]'
        elif url.find("reyanime") >= 0:
            title = title + ' [COLOR lightyellow][I][ReyAnime][/I][/COLOR]'
        elif url.find("jkanime") >= 0:
            title = title + ' [COLOR lightyellow][I][JkAnime][/I][/COLOR]'
        elif url.find("animeflv") >= 0:
            title = title + ' [COLOR lightyellow][I][AnimeFLV][/I][/COLOR]'   
        else: title = title + ' [COLOR lightyellow][I][Unknown Linker][/I][/COLOR]'

    elif url.startswith("serie") == True:
        if url.find("seriesadicto") >= 0:
            title = title + ' [COLOR lightyellow][I][SeriesAdicto][/I][/COLOR]'
        elif url.find("seriesflv") >= 0:
            title = title + ' [COLOR lightyellow][I][SeriesFLV][/I][/COLOR]'
        elif url.find("seriesyonkis") >= 0:
            title = title + ' [COLOR lightyellow][I][SeriesYonkis][/I][/COLOR]'
        elif url.find("seriesblanco") >= 0:
            title = title + ' [COLOR lightyellow][I][SeriesBlanco][/I][/COLOR]'
        elif url.find("pordede") >= 0:
            title = title + ' [COLOR lightyellow][I][Pordede][/I][/COLOR]'
        elif url.find("hdfull.tv") >= 0:
            title = title + ' [COLOR lightyellow][I][HDFull][/I][/COLOR]'
        elif url.find("tv-vip.com") >= 0:
            title = title + ' [COLOR lightyellow][I][TV-VIP][/I][/COLOR]'
        elif url.find("inkapelis") >= 0:
            title = title + ' [COLOR lightyellow][I][InkaPelis][/I][/COLOR]'
        elif url.find("seriesdanko") >= 0:
            title = title + ' [COLOR lightyellow][I][SeriesDanko][/I][/COLOR]'              
        elif url.find("reyanime") >= 0:
            title = title + ' [COLOR lightyellow][I][ReyAnime][/I][/COLOR]'
        elif url.find("jkanime") >= 0:
            title = title + ' [COLOR lightyellow][I][JkAnime][/I][/COLOR]'
        elif url.find("animeflv") >= 0:
            title = title + ' [COLOR lightyellow][I][AnimeFLV][/I][/COLOR]' 
        else: title = title + ' [COLOR lightyellow][I][Unknown Linker][/I][/COLOR]'   

    elif url.startswith("txt:") == True:
        title = title + ' [COLOR lightyellow][I][TXT][/I][/COLOR]'

    elif url.startswith("epg-txt:") == True:
        title = title + ' [COLOR lightyellow][I][EPG-TXT][/I][/COLOR]'        

    elif url.startswith("goear") == True:
        title = title + ' [COLOR lightyellow][I][goear][/I][/COLOR]'        

    elif url.startswith("http") == True:
        server = video_analyzer(url)
        if server != "unknown":
            title = title + ' [COLOR lightyellow][I]['+server+'][/I][/COLOR]'
        
        elif url.find("www.youtube.com") >= 0:
            title = title + ' [COLOR lightyellow][I][Youtube][/I][/COLOR]'

        elif url.find("vimeo.com") >= 0:
            if url.find("vimeo.com/channels") >= 0:
                title = title + ' [COLOR lightyellow][I][Vimeo Playlist][/I][/COLOR]'
            else:
                title = title + ' [COLOR lightyellow][I][Vimeo][/I][/COLOR]'            

        elif url.find("dailymotion.com/video") >= 0:
            title = title + ' [COLOR lightyellow][I][Dailymotion][/I][/COLOR]'

        elif url.find("dailymotion.com/playlist") >= 0:
            title = title + ' [COLOR lightyellow][I][Dailymotion Playlist][/I][/COLOR]'

        elif url.find(".m3u8") >= 0:
            title = title + ' [COLOR lightyellow][I][M3u8][/I][/COLOR]'

        else:
            title = title + ' [COLOR lightyellow][I][HTTP][/I][/COLOR]'
            
    elif url.startswith("rtmp") == True:        
        if url.find("iguide.to") >= 0:
            title = title + ' [COLOR lightyellow][I][iguide][/I][/COLOR]'
        elif url.find("mips") >= 0:
            title = title + ' [COLOR lightyellow][I][mips][/I][/COLOR]'            
        elif url.find("freetvcast.pw") >= 0:
            title = title + ' [COLOR lightyellow[I][freetvcast][/I][/COLOR]'
        elif url.find("pageUrl=http://privado.streamingfreetv.net") >= 0:
            title = title + ' [COLOR lightyellow][I][streamingfreetv][/I][/COLOR]'
        elif url.find("9stream") >= 0:
            title = title + ' [COLOR lightyellow][I][9stream][/I][/COLOR]'
        elif url.find("freebroadcast") >= 0:
            title = title + ' [COLOR lightyellow][I][freebroadcast][/I][/COLOR]'
        elif url.find("cast247") >= 0:
            title = title + ' [COLOR lightyellow][I][cast247][/I][/COLOR]'
        elif url.find("castalba") >= 0:
            title = title + ' [COLOR lightyellow][I][castalba][/I][/COLOR]'
        elif url.find("direct2watch") >= 0:
            title = title + ' [COLOR lightyellow][I][direct2watch][/I][/COLOR]'
        elif url.find("vaughnlive") >= 0:
            title = title + ' [COLOR lightyellow][I][vaughnlive][/I][/COLOR]'
        elif url.find("sawlive") >= 0:
            title = title + ' [COLOR lightyellow][I][sawlive][/I][/COLOR]'        
        elif url.find("shidurlive") >= 0:
            title = title + ' [COLOR lightyellow][I][shidurlive][/I][/COLOR]'
        elif url.find("vercosas") >= 0:
            title = title + ' [COLOR lightyellow][I][vercosas][/I][/COLOR]'
        elif url.find("pageUrl=http://rdmcast.com") >= 0:
            title = title + ' [COLOR lightyellow][I][rdmcast][/I][/COLOR]'
        elif url.find("businessapp1") >= 0:
            title = title + ' [COLOR lightyellow][I][businessapp1][/I][/COLOR]'
        elif url.find("broadcastlive") >= 0:
            title = title + ' [COLOR lightyellow][I][broadcastlive][/I][/COLOR]'               
        else:
            title = title + ' [COLOR lightyellow][I][rtmp][/I][/COLOR]'            
            
    elif url.startswith("udp") == True:
        title = title + ' [COLOR lightyellow][I][udp][/I][/COLOR]'         
    
    elif url.startswith("rtp") == True:
        title = title + ' [COLOR lightyellow][I][rtp][/I][/COLOR]'            
    
    elif url.startswith("mms") == True:
        title = title + ' [COLOR lightyellow][I][mms][/I][/COLOR]'      

    elif url.startswith("plugin") == True:
        if url.startswith("plugin://plugin.video.SportsDevil/") == True:
            title = title + ' [COLOR lightyellow][I][SportsDevil][/I][/COLOR]'

        elif url.startswith("plugin://plugin.video.f4mTester") == True:
            title = title + ' [COLOR lightyellow][I][F4M][/I][/COLOR]'
                        
        elif url.startswith("plugin://plugin.video.youtube/") == True:
            if url.startswith("plugin://plugin.video.youtube/play/") == True:
                title = title + ' [COLOR lightyellow][I][Youtube Video][/I][/COLOR]'

            elif url.startswith("plugin://plugin.video.youtube/user/") == True:
                title = title + ' [COLOR lightyellow][I][Youtube User][/I][/COLOR]'

            elif url.startswith("plugin://plugin.video.youtube/channel/") == True:
                title = title + ' [COLOR lightyellow][I][Youtube Channel][/I][/COLOR]'
            
        elif url.find("plugin.video.p2p-streams") == True:                        
            if url.find("mode=1") >= 0 :  # Acestream
                title = title + ' [COLOR lightyellow][I][Acestream][/I][/COLOR]'
                            
            elif url.find("mode=2") >= 0 :  # Sopcast
                title = title + ' [COLOR lightyellow][I][Sopcast][/I][/COLOR]'

            elif url.find("mode=401") >= 0 :  # P2P-Streams Parser
                title = title + ' [COLOR lightyellow][I][p2p-streams parser][/I][/COLOR]'

        elif url.startswith("plugin://plugin.video.p2psport") == True:
            title = title + ' [COLOR lightyellow][I][P2P Sport][/I][/COLOR]'

        elif url.startswith("plugin://plugin.video.live.streamspro") == True:
            title = title + ' [COLOR lightyellow][I][Livestreams][/I][/COLOR]'

        elif url.startswith("plugin://plugin.video.stalker") == True:
            title = title + ' [COLOR lightyellow][I][Stalker][/I][/COLOR]'

        elif url.startswith("plugin://plugin.video.pelisalacarta/") == True:
            title = title + ' [COLOR lightyellow][I][[B]Pelis[/B]alacarta][/I][/COLOR]'            
            
        else:
            title = title + ' [COLOR lightyellow][I][Addon][/I][/COLOR]'
            
    elif url.startswith("magnet") == True:
        title = title + ' [COLOR lightyellow][I][Magnet][/I][/COLOR]'

    elif url.startswith("torrent") == True:
        title = title + ' [COLOR lightyellow][I][Torrent][/I][/COLOR]'        

    elif url.startswith("sop") == True:
        title = title + ' [COLOR lightyellow][I][Sopcast][/I][/COLOR]'        
        
    elif url.startswith("ace") == True:
        title = title + ' [COLOR lightyellow][I][Acestream][/I][/COLOR]'

    elif url.startswith("bum") == True:
        title = title + ' [COLOR lightyellow][I][BUM+][/I][/COLOR]'        

    elif url.startswith("devil") == True:
        title = title + ' [COLOR lightyellow][I][SportsDevil][/I][/COLOR]'

    elif url.startswith("short") == True:
        title = title + ' [COLOR lightyellow][I][ShortLink][/I][/COLOR]'        

    elif url.startswith("img") == True:
        title = title + ' [COLOR lightyellow][I][IMG][/I][/COLOR]'

    elif url.startswith("agendatv") == True:
        title = title + ' [COLOR lightyellow][I][Agenda TV][/I][/COLOR]'          
        
    else:
        title = title + ' [COLOR lightyellow][I][Unknown][/I][/COLOR]'

    return title


# Función modificada de show_image para multilinks para evitare rror en url = params.get("url") porque url es #multilink 
def show_image(url):
    plugintools.log('[%s %s].show_image %s' % (addonName, addonVersion, url))

    h=urllib2.HTTPHandler(debuglevel=0)  # Iniciamos descarga...
    request = urllib2.Request(url)
    opener = urllib2.build_opener(h)
    urllib2.install_opener(opener)
    filename = url.split("/")
    max_len = len(filename)
    max_len = int(max_len) - 1
    filename = filename[max_len]
    fh = open(__temp__ + filename, "wb")  #open the file for writing
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
    imagen = __temp__ + filename
    xbmc.executebuiltin( "ShowPicture("+imagen+")" )

def run_tube(url):    
    plugintools.log("RunPlugin = "+url)
    xbmc.executebuiltin('XBMC.RunPlugin('+url+')')

def run_tube2(params):    
    plugintools.log("RunPlugin = "+repr(params))
    url = params.get("url")
    xbmc.executebuiltin('XBMC.RunScript('+url+')')

    
