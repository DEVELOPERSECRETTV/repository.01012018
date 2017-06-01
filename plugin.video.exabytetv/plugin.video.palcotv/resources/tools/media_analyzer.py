# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Analizador de medios de PalcoTV
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import plugintools
import urllib2
import HTMLParser
import urllib,urlparse

from BeautifulSoup import BeautifulSoup as bs
from resources.tools.resolvers import *
from resources.tools.server_rtmp import *
import json

from __main__ import *

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

DESCARGAS = xbmc.translatePath(os.path.join('special://userdata/addon_data/'+addonId+'/descargas', ''))


def plugin_analyzer(data, title, plot, datamovie, thumbnail, fanart):
    plugintools.log("[%s %s] Analizando plugin... %s " % (addonName, addonVersion, plot))
    datamovie["plot"]=plot    
    if data.startswith("plugin://plugin.video.SportsDevil/") == True:
        url = data.strip()
        plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [SportsDevil][/I][/COLOR]', url = url , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )

    elif data.startswith("plugin://plugin.video.f4mTester") == True or data.startswith("plugin://plugin.video.pldplayerm3u/") == True:
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [F4M][/I][/COLOR]', plot = plot , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                    
    elif data.startswith("plugin://plugin.video.youtube") == True:
        if data.startswith("plugin://plugin.video.youtube/channel/") == True:
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [You[B]Tube[/B] Channel][/I][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )            
        elif data.startswith("plugin://plugin.video.youtube/user/") == True:
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [You[B]Tube[/B] User][/I][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
        elif data.startswith("plugin://plugin.video.youtube/playlist/") == True:
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [You[B]Tube[/B] Playlist][/I][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )            
        elif data.startswith("plugin://plugin.video.youtube/play/?playlist_id") == True:
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [You[B]Tube[/B] Playlist][/I][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )            
        else:
            plugintools.runAddon( action = "play" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [You[B]Tube[/B] Video][/I][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
       
    elif data.find("plugin.video.p2p-streams") == True:                        
        if data.find("mode=1") >= 0 :  # Acestream
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [Acestream][/I][/COLOR]' , plot = plot , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                        
        elif data.find("mode=2") >= 0 :  # Sopcast
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [Sopcast][/I][/COLOR]' , plot = plot , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )

        elif data.find("mode=401") >= 0 :  # P2P-Streams Parser
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [p2p-streams][/I][/COLOR]' , plot = plot , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )            

    elif data.startswith("plugin://plugin.video.p2psport") == True:
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [P2P Sport][/I][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )

    elif data.startswith("plugin://plugin.video.live.streamspro") == True:
        if data.strip().find("mode=1&name=") >=0 or data.strip().find("makelist") >=0 :  # Parcheado por DMO: Soporte de pseudo parsers de LSP y listas  (DMO)
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [LiveStreams][/I][/COLOR]', url = data.strip() , info_labels = datamovie, plot = plot, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
        else:
            plugintools.runAddon( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [LiveStreams][/I][/COLOR]', url = data.strip() , info_labels = datamovie, plot = plot, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )
            
    elif data.startswith("plugin://plugin.video.stalker") == True:
        mac=plugintools.read('https://copy.com/HuEtREKgnvlc9XrS');  # Mac PalcoTV
        data=data.replace("MAC_STALKER", mac).strip()
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [Stalker][/I][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )

    elif data.startswith("plugin://plugin.video.dailymotion_com") == True:  # Dailymotion (2.1.5)
        if data.find("mode=showPlaylist") >= 0:
            plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [Dailymotion Playlist][/I][/COLOR]', url = data , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
        else:
            plugintools.runAddon( action = "play" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [Dailymotion Video][/I][/COLOR]', url = data , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )

    elif data.startswith("plugin://plugin.video.videodevil") == True:  # VideoDevil modules
        plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [VideoDevil][/I][/COLOR]', url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )          
		
    elif data.startswith("plugin://plugin.video.pelisalacarta") == True:  # Pelisalacarta
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [Pelisalacarta][/I][/COLOR]' , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )

    elif data.startswith("plugin://script.extendedinfo") == True:
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [ExtendedInfo][/I][/COLOR]' , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )

    elif data.startswith("plugin://plugin.video.pulsar/movie/") == True:
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [Pulsar][/I][/COLOR]' , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )        

    else:        
        plugintools.add_item( action = "play" , title = '[COLOR white]' + title + '[COLOR lightyellow][I] [Addon][/I][/COLOR]' , url = data.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
      

def p2p_builder_url(url, title_fixed, p2p):

    if p2p == "ace":
        p2p_launcher = plugintools.get_setting("p2p_launcher")
        plugintools.log("p2p_launcher= "+p2p_launcher)        
        if p2p_launcher == "0":
            url = 'plugin://program.plexus/?url='+url+'&mode=1&name='+title_fixed
        else:
            url = 'plugin://plugin.video.p2p-streams/?url='+url+'&mode=1&name='+title_fixed

    elif p2p == "sop":
        p2p_launcher = plugintools.get_setting("p2p_launcher")
        plugintools.log("p2p_launcher= "+p2p_launcher)
        if p2p_launcher == "0":
            url = 'plugin://program.plexus/?url='+url+'&mode=2&name='+title_fixed
        else:
            url = 'plugin://plugin.video.p2p-streams/?url='+url+'&mode=2&name='+title_fixed

    elif p2p == "torrent":
        url = urllib.quote_plus(url)
        addon_torrent = plugintools.get_setting("addon_torrent")
        if addon_torrent == "0":  # Stream (por defecto)
            url = 'plugin://plugin.video.stream/play/'+url
        elif addon_torrent == "1":  # Pulsar
            url = 'plugin://plugin.video.pulsar/play?uri=' + url     
        elif addon_torrent == "2":  # XBMCtorrent
            url = 'plugin://plugin.video.quasar/play?uri=' + url
        elif addon_torrent == "3":  # Plexus
            url = 'plugin://program.plexus/?url=' + url
        elif addon_torrent == "4":  # Quasar
            url = 'plugin://plugin.video.quasar/play?uri=' + url
        elif addon_torrent == "5":  # YATP
            url = 'plugin://plugin.video.yatp/play?uri=' + url              

    elif p2p == "magnet":
        addon_magnet = plugintools.get_setting("addon_magnet")
        if addon_magnet == "0":  # Stream (por defecto)
            url = 'plugin://plugin.video.stream/play/'+url
        elif addon_magnet == "1":  # Pulsar
            url = 'plugin://plugin.video.pulsar/play?uri=' + url
        elif addon_magnet == "2":  # Kmediatorrent
            url = 'plugin://plugin.video.kmediatorrent/play/'+url
        elif addon_magnet == "3":  # XBMCtorrent
            url = 'plugin://plugin.video.xbmctorrent/play?uri=' + url             
        elif addon_magnet == "4":  # Quasar
            url = 'plugin://plugin.video.quasar/play?uri=' + url
        elif addon_magnet == "5":  # YATP
            url = 'plugin://plugin.video.yatp/play?uri=' + url
        
    plugintools.log("[%s %s] Creando llamada para URL P2P... %s " % (addonName, addonVersion, url))
    return url

def video_analyzer(url):
    plugintools.log("[%s %s] Análisis de URL de vídeo... " % (addonName, addonVersion))

    if url.find("allmyvideos") >=0: server = "allmyvideos"
    elif url.find("vidspot") >= 0: server = "vidspot"
    elif url.find("played") >= 0: server = "playedto"
    elif url.find("streamin.to") >= 0: server = "streaminto"
    elif url.find("streamcloud") >= 0: server = "streamcloud"
    elif url.find("nowvideo") >= 0: server = "nowvideo"
    elif url.find("veehd") >= 0: server = "veehd"
    elif url.find("vk") >= 0: server = "vk"
    elif url.find("lidplay") >= 0: server = "vk"   
    elif url.find("tumi") >= 0: server = "tumi"
    elif url.find("novamov") >= 0: server = "novamov"
    elif url.find("moevideos") >= 0: server = "moevideos"
    elif url.find("gamovideo") >= 0: server = "gamovideo"
    elif url.find("movshare") >= 0: server = "movshare"
    elif url.find("powvideo") >= 0: server = "powvideo"
    elif url.find("mail.ru") >= 0: server = "mailru"
    elif url.find("mediafire") >= 0: server = "mediafire"
    elif url.find("netu") >= 0: server = "netu"
    elif url.find("waaw") >= 0: server = "waaw"
    elif url.find("movreel") >= 0: server = "movreel"
    elif url.find("videobam") >= 0: server = "videobam"
    elif url.find("vimeo/videos") >= 0: server = "vimeo"
    elif url.find("vimeo/channels") >= 0: server = "vimeo_pl"        
    elif url.find("veetle") >= 0: server = "veetle"
    elif url.find("videoweed") >= 0: server = "videoweed"
    elif url.find("streamable") >= 0: server = "streamable"
    elif url.find("rocvideo") >= 0: server = "rocvideo"
    elif url.find("realvid") >= 0: server = "realvid"
    elif url.find("videomega") >= 0: server = "videomega"
    elif url.find("video.tt") >= 0: server = "videott"
    elif url.find("flashx") >= 0: server = "flashx"
    elif url.find("openload") >= 0: server = "openload"
    elif url.find("turbovideos") >= 0: server = "turbovideos"
    elif url.find("ok.ru") >= 0: server = "okru"
    elif url.find("vidto") >= 0: server = "vidtome"
    elif url.find("playwire") >= 0: server = "playwire" 
    elif url.find("vimple") >= 0: server = "vimple"
    elif url.find("vidgg") >= 0: server = "vidggto"
    elif url.find("uptostream") >= 0: server = "uptostream"
    elif url.find("youwatch") >= 0: server = "youwatch"
    elif url.find("idowatch") >= 0: server = "idowatch"
    elif url.find("cloudtime") >= 0: server = "cloudtime"
    elif url.find("allvid") >= 0: server = "allvid"
    elif url.find("vodlocker") >= 0: server = "vodlocker"
    elif url.find("vidzi") >= 0: server = "vidzitv"
    elif url.find("streame") >= 0: server = "streamenet"
    elif url.find("myvideoz") >= 0: server = "myvideoz"
    elif url.find("streamplay") >= 0: server = "streamplay"
    elif url.find("watchonline") >= 0: server = "watchonline"
    elif url.find("rutube") >= 0: server = "rutube"
    elif url.find("dailymotion") >= 0: server = "dailymotion"
    elif url.find("auroravid") >= 0: server = "auroravid"
    elif url.find("wholecloud") >= 0: server = "wholecloud"
    elif url.find("bitvid") >= 0: server = "bitvid"
    elif url.find("spruto") >= 0: server = "spruto"
    elif url.find("stormo") >= 0: server = "stormo"
    elif url.find("myvi.ru") >= 0: server = "myviru"
    elif url.find("youtube") >= 0: server = "youtube"
    elif url.find("filmon") >= 0: server = "filmon"
    elif url.find("thevideo.me") >= 0: server = "thevideome"
    elif url.find("videowood") >= 0: server = "videowood"
    elif url.find("neodrive") >= 0: server = "neodrive"
    elif url.find("cloudzilla") >= 0: server = "cloudzilla"
    elif url.find("thevideobee") >= 0: server = "thevideobee"
    elif url.find("fileshow") >= 0: server = "fileshow"
    elif url.find("vid.ag") >= 0: server = "vid"
    elif url.find("vidxtreme") >= 0: server = "vidxtreme"
    elif url.find("vidup") >= 0: server = "vidup"
    elif url.find("watchvideo") >= 0: server = "watchvideo"
    elif url.find("speedvid") >= 0: server = "speedvid"
    elif url.find("chefti.info") >= 0: server = "exashare"
    elif url.find("ajihezo.info") >= 0: server = "exashare"
    elif url.find("bojem3a.info") >= 0: server = "exashare"
    elif url.find("erd9x4.info") >= 0: server = "exashare"
    elif url.find("vodbeast") >= 0: server = "vodbeast"
    elif url.find("nosvideo") >= 0: server = "nosvideo"
    elif url.find("noslocker") >= 0: server = "noslocker"
    elif url.find("up2stream") >= 0: server = "up2stream"
    elif url.find("smartvid") >= 0: server = "smartvid"
    elif url.find("greevid") >= 0: server = "greevid"
    elif url.find("letwatch") >= 0: server = "letwatch"
    elif url.find("yourupload") >= 0: server = "yourupload"
    elif url.find("zalaa") >= 0: server = "zalaa" 
    elif url.find("uploadc") >= 0: server = "uploadc" 
    elif url.find("mp4upload") >= 0: server = "mp4upload"
    elif url.find("rapidvideo") >= 0: server = "rapidvideo"
    elif url.find("yourvideohost") >= 0: server = "yourvideohost"
    elif url.find("watchers") >= 0: server = "watchers"
    elif url.find("vidtodo") >= 0: server = "vidtodo"
    elif url.find("izanagi") >= 0: server = "izanagi"
    elif url.find("yotta") >= 0: server = "yotta"
    elif url.find("kami") >= 0: server = "kami"
    elif url.find("touchfile") >= 0: server = "touchfile"
    elif url.find("zstream") >= 0: server = "zstream"
    elif url.find("vodlock") >= 0: server = "vodlock"
    elif url.find("goodvideohost") >= 0: server = "goodvideohost"
    elif url.find("happystreams") >= 0: server = "happystreams"
    elif url.find("speedvideo") >= 0: server = "speedvideo"
    elif url.find("vidbull") >= 0: server = "vidbull"
    elif url.find("filehoot") >= 0: server = "filehoot"
    elif url.find("thevideos") >= 0: server = "thevideos"
    else: server = 'unknown'
    return server

def server_analyzer(params):
    plugintools.log("[%s %s] Análisis de Servidores de vídeo... " % (addonName, addonVersion))

    url_final = params.get("url")
    plugintools.log(">>>>> Analizando Servidor Para la Url= "+ url_final)

    if url_final.find("allmyvideos") >= 0: params["url"]=url_final; allmyvideos(params)
    elif url_final.find("vidspot") >= 0: params["url"]=url_final; vidspot(params)
    elif url_final.find("played.to") >= 0: params["url"]=url_final; playedto(params)
    elif url_final.find("streamin.to") >= 0: params["url"]=url_final; streaminto(params)
    elif url_final.find("streamcloud") >= 0: params["url"]=url_final; streamcloud(params)
    elif url_final.find("nowvideo.sx") >= 0: params["url"]=url_final; nowvideo(params)
    elif url_final.find("veehd") >= 0: params["url"]=url_final; veehd(params)
    elif url_final.find("vk") >= 0: params["url"]=url_final; vk(params)
    elif url_final.find("lidplay") >= 0: params["url"]=url_final; vk(params)
    elif url_final.find("tumi.tv") >= 0: params["url"]=url_final; tumi(params)
    elif url_final.find("novamov") >= 0: params["url"]=url_final; novamov(params)
    elif url_final.find("moevideos") >= 0: params["url"]=url_final; moevideos(params)
    elif url_final.find("gamovideo") >= 0: params["url"]=url_final; gamovideo(params)
    elif url_final.find("movshare") >= 0: params["url"]=url_final; movshare(params)
    elif url_final.find("powvideo") >= 0: params["url"]=url_final; powvideo(params)
    elif url_final.find("mail.ru") >= 0: params["url"]=url_final; mailru(params)
    elif url_final.find("mediafire") >= 0: params["url"]=url_final; mediafire(params)
    elif url_final.find("netu") >= 0: params["url"]=url_final; netu(params)
    elif url_final.find("waaw") >= 0: params["url"]=url_final; waaw(params)
    elif url_final.find("movreel") >= 0: params["url"]=url_final; movreel(params)
    elif url_final.find("videobam") >= 0: params["url"]=url_final; videobam(params)    
    elif url_final.find("vimeo/videos") >= 0: params["url"]=url_final; vimeo(params)
    elif url_final.find("vimeo/channels") >= 0: params["url"]=url_final; vimeo_pl(params)
    elif url_final.find("veetle") >= 0: params["url"]=url_final; veetle(params)
    elif url_final.find("videoweed") >= 0: params["url"]=url_final; videoweed(params)
    elif url_final.find("streamable") >= 0: params["url"]=url_final; streamable(params)
    elif url_final.find("rocvideo") >= 0: params["url"]=url_final; rocvideo(params)
    elif url_final.find("realvid") >= 0: params["url"]=url_final; realvid(params)
    elif url_final.find("videomega") >= 0: params["url"]=url_final; videomega(params)
    elif url_final.find("video.tt") >= 0: params["url"]=url_final; videott(params)
    elif url_final.find("flashx") >= 0: params["url"]=url_final; flashx(params)
    elif url_final.find("openload") >= 0: params["url"]=url_final; openload(params)
    elif url_final.find("turbovideos") >= 0: params["url"]=url_final; turbovideos(params)
    elif url_final.find("ok.ru") >= 0: params["url"]=url_final; okru(params)
    elif url_final.find("vidto.me") >= 0: params["url"]=url_final; vidtome(params)
    elif url_final.find("playwire") >= 0: params["url"]=url_final; playwire(params)
    elif url_final.find("vimple.ru") >= 0: params["url"]=url_final; vimple(params)
    elif url_final.find("vidgg") >= 0: params["url"]=url_final; vidggto(params)
    elif url_final.find("uptostream.com") >= 0: params["url"]=url_final; uptostream(params)
    #################################################################################
    elif url_final.find("youwatch") >= 0: params["url"]=url_final; youwatch(params)
    elif url_final.find("chouhaa") >= 0: params["url"]=url_final; youwatch(params)
    elif url_final.find("msemen") >= 0: params["url"]=url_final; youwatch(params)
    elif url_final.find("smed79") >= 0: params["url"]=url_final; youwatch(params)
    elif url_final.find("uroclm5d") >= 0: params["url"]=url_final; youwatch(params)
    #################################################################################
    elif url_final.find("idowatch") >= 0: params["url"]=url_final; idowatch(params)
    elif url_final.find("cloudtime") >= 0: params["url"]=url_final; cloudtime(params)
    elif url_final.find("allvid") >= 0: params["url"]=url_final; allvid(params)
    elif url_final.find("vodlocker") >= 0: params["url"]=url_final; vodlocker(params)
    elif url_final.find("vidzi.tv") >= 0: params["url"]=url_final; vidzitv(params)
    elif url_final.find("streame.net") >= 0: params["url"]=url_final; streamenet(params)
    elif url_final.find("myvideoz") >= 0: params["url"]=url_final; myvideoz(params)
    elif url_final.find("streamplay") >= 0: params["url"]=url_final; streamplay(params)
    elif url_final.find("watchonline") >= 0: params["url"]=url_final; watchonline(params)
    elif url_final.find("rutube") >= 0: params["url"]=url_final; rutube(params)
    elif url_final.find("dailymotion") >= 0: params["url"]=url_final; dailymotion(params)
    elif url_final.find("auroravid") >= 0: params["url"]=url_final; auroravid(params)
    elif url_final.find("wholecloud") >= 0: params["url"]=url_final; wholecloud(params)
    elif url_final.find("bitvid") >= 0: params["url"]=url_final; bitvid(params)
    elif url_final.find("spruto") >= 0: params["url"]=url_final; spruto(params)
    elif url_final.find("stormo") >= 0: params["url"]=url_final; stormo(params)
    elif url_final.find("myvi.ru") >= 0: params["url"]=url_final; myviru(params)
    elif url_final.find("youtube.com") >= 0: params["url"]=url_final; youtube(params)
    elif url_final.find("filmon.com") >= 0: params["url"]=url_final; filmon(params)
    elif url_final.find("thevideo.me") >= 0: params["url"]=url_final; thevideome(params)
    elif url_final.find("videowood.tv") >= 0: params["url"]=url_final; videowood(params)
    elif url_final.find("neodrive.co") >= 0: params["url"]=url_final; neodrive(params)
    elif url_final.find("cloudzilla") >= 0: params["url"]=url_final; cloudzilla(params)
    elif url_final.find("thevideobee.to") >= 0: params["url"]=url_final; thevideobee(params)
    elif url_final.find("fileshow.tv") >= 0: params["url"]=url_final; fileshow(params)
    elif url_final.find("vid.ag") >= 0: params["url"]=url_final; vid(params)
    elif url_final.find("vidxtreme.to") >= 0: params["url"]=url_final; vidxtreme(params)
    elif url_final.find("vidup") >= 0: params["url"]=url_final; vidup(params)
    elif url_final.find("watchvideo") >= 0: params["url"]=url_final; watchvideo(params)
    elif url_final.find("speedvid") >= 0: params["url"]=url_final; speedvid(params)
    #################################################################################
    elif url_final.find("chefti.info") >= 0: params["url"]=url_final; exashare(params)
    elif url_final.find("ajihezo.info") >= 0: params["url"]=url_final; exashare(params)
    elif url_final.find("bojem3a.info") >= 0: params["url"]=url_final; exashare(params)
    elif url_final.find("erd9x4.info") >= 0: params["url"]=url_final; exashare(params)
    #################################################################################
    elif url_final.find("vodbeast") >= 0: params["url"]=url_final; vodbeast(params)
    elif url_final.find("nosvideo") >= 0: params["url"]=url_final; nosvideo(params)
    elif url_final.find("noslocker") >= 0: params["url"]=url_final; noslocker(params)
    elif url_final.find("up2stream") >= 0: params["url"]=url_final; up2stream(params)
    elif url_final.find("smartvid") >= 0: params["url"]=url_final; smartvid(params)
    elif url_final.find("greevid") >= 0: params["url"]=url_final; greevid(params)
    elif url_final.find("letwatch") >= 0: params["url"]=url_final; letwatch(params)
    elif url_final.find("yourupload") >= 0: params["url"]=url_final; yourupload(params)
    elif url_final.find("zalaa") >= 0: params["url"]=url_final; zalaa(params)
    elif url_final.find("uploadc") >= 0: params["url"]=url_final; uploadc(params)
    elif url_final.find("mp4upload") >= 0: params["url"]=url_final; mp4upload(params)
    elif url_final.find("rapidvideo") >= 0: params["url"]=url_final; rapidvideo(params)
    elif url_final.find("yourvideohost") >= 0: params["url"]=url_final; yourvideohost(params)
    elif url_final.find("watchers") >= 0: params["url"]=url_final; watchers(params)
    elif url_final.find("vidtodo") >= 0: params["url"]=url_final; vidtodo(params)
    elif url_final.find("izanagi") >= 0: params["url"]=url_final; izanagi(params)
    elif url_final.find("yotta") >= 0: params["url"]=url_final; yotta(params)
    elif url_final.find("kami") >= 0: params["url"]=url_final; kami(params)
    elif url_final.find("touchfile") >= 0: params["url"]=url_final; touchfile(params)
    elif url_final.find("zstream") >= 0: params["url"]=url_final; zstream(params)
    elif url_final.find("vodlock") >= 0: params["url"]=url_final; vodlock(params)
    elif url_final.find("goodvideohost") >= 0: params["url"]=url_final; goodvideohost(params)
    elif url_final.find("happystreams") >= 0: params["url"]=url_final; happystreams(params)
    elif url_final.find("speedvideo") >= 0: params["url"]=url_final; speedvideo(params)
    elif url_final.find("vidbull") >= 0: params["url"]=url_final; vidbull(params)
    elif url_final.find("filehoot") >= 0: params["url"]=url_final; filehoot(params)
    

def parser_title(title):
    #plugintools.log('[%s %s].parserr_title %s' % (addonName, addonVersion, title))

    cyd=title;patcolor=plugintools.find_multiple_matches(cyd, '\[([^\]]+)')
    for entry in patcolor:
        plugintools.log("****entry= "+entry)
        entry='['+entry+']'
        cyd=cyd.replace(entry, "")
       
    plugintools.log("****cyd= "+cyd)
    cyd = cyd.replace(" [Lista M3U]", "").replace("[M3U]", "").replace("[[B]M3U[/B]]", "").replace("M3U]", "").strip()
    cyd = cyd.replace(" [Lista PLX]", "").replace("[[B]PLX[/B]]", "").replace("[[B]PLX[/B]]", "").replace("PLX]", "").strip()   
    cyd = cyd.replace("[COLOR orange][PLX][/COLOR]", "").replace(" [COLOR orange][[B]PLX[/B]][/COLOR]", "")
    cyd = cyd.replace("[COLOR orange][M3U][/COLOR]", "").replace("[COLOR orange][[B]M3U[/B]][/COLOR]", "")
    cyd=cyd.replace("/", "").replace("[", "").replace("]", "").replace("&quot;", '"')
    cyd=cyd.replace("[/COLOR]", "").replace("[B]", "").replace("[/B]", "").replace("[I]", "").replace("[/I]", "")
    cyd=cyd.replace("[Auto]", "").replace("[Parser]", "").replace("[TinyURL]", "").replace("[Auto]", "").replace("[Filtros]", "").replace("[Filtro]", "")    
    cyd = cyd.replace("[", "").replace("]", "").replace("[B]", "").replace("[I]", "").replace("[/B]", "").replace("[/I]", "")  # Control para evitar errores al crear archivos
    plugintools.log("****cyd= "+cyd)
    # Control para evitar filenames con corchetes
    cyd = cyd.replace(" [Multilink]", "")
    cyd = cyd.replace(" [Multi]", "").replace("[Multi]", "")
    cyd = cyd.replace(" [Multiparser]", "")
    cyd = cyd.replace(" [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR]", "")
    cyd = cyd.replace(" [COLOR lightyellow][B][Dailymotion[/B] video][/COLOR]", "")
    cyd = cyd.replace(' [COLOR gold][CBZ][/COLOR]', "")
    cyd = cyd.replace(' [COLOR gold][CBR][/COLOR]', "")
    cyd = cyd.replace(' [COLOR gold][Mediafire][/COLOR]', "")
    cyd = cyd.replace(' [CBZ]', "")
    cyd = cyd.replace(' [CBR]', "")
    cyd = cyd.replace(' [Mediafire]', "")
    cyd = cyd.replace(' [EPG-TXT]', "")
    cyd = cyd.replace('*', '').strip()
    cyd = cyd.replace('Â»', '').replace("»", '').replace("ï", "").replace("¿", "").replace("½", "").replace("[COLOR=FF888888]ï¿½[/COLOR]", "").strip()

    if cyd.endswith(" .plx") == True: title = title.replace(" .plx", ".plx")
    plugintools.log("****cyd= "+cyd)

    return cyd


def launch_magnet(params):
    plugintools.log('[%s %s] launch_magnet... %s' % (addonName, addonVersion, repr(params)))
    url = params.get("url")

    options_torrent=[];urls_torrent=[]
    options_torrent.append('Cliente interno [COLOR red][I](Requiere [B]libtorrent[/B])[/I][/COLOR]')
    if xbmc.getCondVisibility('System.HasAddon("plugin.video.xbmctorrent")'):
        options_torrent.append("XBMCtorrent");urls_torrent.append("plugin://plugin.video.xbmctorrent/play/"+url)        
    if xbmc.getCondVisibility('System.HasAddon("plugin.video.pulsar")'):
        options_torrent.append("Pulsar [COLOR lightgreen][I](Instalado!)[/I][/COLOR]");urls_torrent.append("plugin://plugin.video.pulsar/play?uri="+url)        
    if xbmc.getCondVisibility('System.HasAddon("plugin.video.quasar")'):
        options_torrent.append("Quasar [COLOR lightgreen][I](Instalado!)[/I][/COLOR]");urls_torrent.append("plugin://plugin.video.quasar/play?uri="+url)        
    if xbmc.getCondVisibility('System.HasAddon("plugin.video.stream")'):
        options_torrent.append("Stream [COLOR lightgreen][I](Instalado!)[/I][/COLOR]");urls_torrent.append("plugin://plugin.video.stream/play/"+url)
    if xbmc.getCondVisibility('System.HasAddon("plugin.video.torrenter")'):
        options_torrent.append("Torrenter [COLOR lightgreen][I](Instalado!)[/I][/COLOR]");urls_torrent.append("plugin://plugin.video.torrenter/?action=playSTRM&url="+url)
    if xbmc.getCondVisibility('System.HasAddon("plugin.video.torrentin")'):
        options_torrent.append("Torrentin [COLOR lightgreen][I](Instalado!)[/I][/COLOR]");urls_torrent.append("plugin://plugin.video.torrentin/?uri="+url+"&image=")

    option_user = plugintools.selector( options_torrent, params.get("title").replace("Torrent: ", "").strip() )
    plugintools.log("urls_torrent= "+repr(urls_torrent))
    if option_user > -1:
        if option_user == 0:  # Cliente interno: Conexión con libtorrent
            play_libtorrent(url)
        else: url=urls_torrent[option_user-1];plugintools.log("Magnet link= "+url);plugintools.play_resolved_url(url)    


def launch_torrent(params):
    plugintools.log('[%s %s] launch_torrent... %s' % (addonName, addonVersion, repr(params)))
    url = params.get("url")

    options_torrent=[];urls_torrent=[]
    options_torrent.append('Cliente interno [COLOR red][I](Requiere [B]libtorrent[/B])[/I][/COLOR]')
    if xbmc.getCondVisibility('System.HasAddon("plugin.video.xbmctorrent")'):
        options_torrent.append("XBMCtorrent");urls_torrent.append("plugin://plugin.video.xbmctorrent/play/"+url)        
    if xbmc.getCondVisibility('System.HasAddon("plugin.video.pulsar")'):
        options_torrent.append("Pulsar [COLOR lightgreen][I](Instalado!)[/I][/COLOR]");urls_torrent.append("plugin://plugin.video.pulsar/play?uri="+url)        
    if xbmc.getCondVisibility('System.HasAddon("plugin.video.quasar")'):
        options_torrent.append("Quasar [COLOR lightgreen][I](Instalado!)[/I][/COLOR]");urls_torrent.append("plugin://plugin.video.quasar/play?uri="+url)        
    if xbmc.getCondVisibility('System.HasAddon("plugin.video.stream")'):
        options_torrent.append("Stream [COLOR lightgreen][I](Instalado!)[/I][/COLOR]");urls_torrent.append("plugin://plugin.video.stream/play/"+url)
    if xbmc.getCondVisibility('System.HasAddon("plugin.video.torrenter")'):
        options_torrent.append("Torrenter [COLOR lightgreen][I](Instalado!)[/I][/COLOR]");urls_torrent.append("plugin://plugin.video.torrenter/?action=playSTRM&url="+url)
    if xbmc.getCondVisibility('System.HasAddon("plugin.video.torrentin")'):
        options_torrent.append("Torrentin [COLOR lightgreen][I](Instalado!)[/I][/COLOR]");urls_torrent.append("plugin://plugin.video.torrentin/?uri="+url+"&image=")
    if xbmc.getCondVisibility('System.HasAddon("program.plexus")'):
        options_torrent.append("Torrentin [COLOR lightgreen][I](Instalado!)[/I][/COLOR]");urls_torrent.append("plugin://plugin.program.plexus/?url=http://'+url+'&mode=1&name=")

    option_user = plugintools.selector( options_torrent, params.get("title").replace("Torrent: ", "").strip() )
    if option_user > -1:
        if option_user == 0:  # Cliente interno: Conexión con libtorrent
            play_libtorrent(url)
        else: url=urls_torrent[option_user];plugintools.log("Torrent File= "+url);plugintools.play_resolved_url(url)   


def play_libtorrent(url):
    plugintools.log("[%s, %s] Reproductor interno: Libtorrent... %s " % (addonName, addonId, url))

    import time
    from resources.lib.btserver import Client

    #Iniciamos el cliente:
    c = Client(url=url, is_playing_fnc= xbmc.Player().isPlaying, wait_time=20, timeout=5, temp_path = temp )
    videourl = None;played = False

    #Mostramos el progreso
    progreso = xbmcgui.DialogProgress()
    progreso.create( "PalcoTV" , "Iniciando torrent...")

    #Mientras el progreso no sea cancelado ni el cliente cerrado
    while not progreso.iscanceled() and not c.closed:
        
        try:
            #Obtenemos el estado del torrent
            s = c.status

            #Montamos las tres lineas con la info del torrent
            txt = '%.2f%% de %.1fMB %s | %.1f kB/s' % \
            (s.progress_file, s.file_size, s.str_state, s._download_rate)
            txt2 =  'S: %d(%d) P: %d(%d) | DHT:%s (%d) | Trackers: %d' % \
            (s.num_seeds, s.num_complete, s.num_peers, s.num_incomplete, s.dht_state, s.dht_nodes, s.trackers)
            txt3 = 'Origen Peers TRK: %d DHT: %d PEX: %d LSD %d ' % \
            (s.trk_peers,s.dht_peers, s.pex_peers, s.lsd_peers)

            #plugintools.log("s.buffer= "+str(s.buffer))
            #plugintools.log("s.progress_file= "+str(s.progress_file))
            #plugintools.log("s.file_size= "+str(s.file_size))
            #prc= (float(s.progress_file) * 10);plugintools.log("prc= "+str(prc))
            progreso.update(int(s.progress_file),txt, txt2, txt3)

            time.sleep(1)
                                
            #Si el buffer se ha llenado y la reproduccion no ha sido iniciada, se inicia
            if s.buffer == 100 and not played:
                plugintools.log("s.buffer_inside= "+str(s.buffer))
                plugintools.log("s.progress_file_inside= "+str(s.progress_file))

                #Cerramos el progreso
                progreso.close()

                #Obtenemos el playlist del torrent
                videourl = c.get_play_list()
                plugintools.log("Playing: "+videourl)
                plugintools.play_resolved_url(videourl)

                #Marcamos como reproducido para que no se vuelva a iniciar
                played = True

                #Y esperamos a que el reproductor se cierre
                while xbmc.Player().isPlaying():
                  time.sleep(1)

                #Cuando este cerrado,  Volvemos a mostrar el dialogo
                progreso.create( "PalcoTV - Torrent" , "Iniciando...")

        except:
            plugintools.log("Error en la reproducción del torrent");break

    progreso.update(100,"Terminando y eliminando datos"," "," ")

    if not c.closed: c.stop()  #Detenemos el cliente
    progreso.close()  #Y cerramos el progreso
    

def devil_analyzer(url,ref):
    url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+url+'%26referer='+referer
    xbmc.executebuiltin('XBMC.RunPlugin(' + url +')')


def url_analyzer(title, datamovie, thumbnail, fanart, plot, url):
    plugintools.log("url_analyzer= "+plot)
    title='[COLOR white]'+title+'[/COLOR]'
    urlk=plugintools.get_setting("urlk")
    
    if url.startswith("llamada") == True:
        ruta_llamadas = xbmc.translatePath(os.path.join(addon_path+'/resources/llamadas', ''))
        url = url.replace("llamada:", "");comandos = url.split("; ");fich_llamada = ruta_llamadas + comandos[0] + ".txt"  # El 1º es el nombre del fichero
        archivo_llamada = open(fich_llamada, "r");url_llamada = archivo_llamada.read();num_comandos = len(comandos)
        for comando in range(1, num_comandos):  # Empiezo en 1 para saltarme el 1º, q es el nombre del fichero, no un "comando" a reemplazar
            sustituye = plugintools.find_single_match(comandos[comando],'(.*?)=')
            por_este = plugintools.find_single_match(comandos[comando],'=(.*)')
            url_llamada = url_llamada.replace(sustituye, por_este)
            
        url = url_llamada;data = url_llamada

    elif url.startswith("plugin") == True:  # Llamadas plugin://
        plugin_analyzer(url, title, plot, datamovie, thumbnail, fanart)

    elif url.startswith("ivoox_pl") == True:
        url=url.replace("ivoox_pl:", "").strip()
        plugintools.addDir( action = "Secciones_Ivoox" , title = title+' [COLOR '+urlk+'][I][iVoox playlist][/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )        

    elif url.startswith("img") == True:
        plugintools.add_item( action = "show_image" , plot = datamovie["plot"] , extra = filename , title = title+' [COLOR '+urlk+'][I][IMG][/COLOR]' , url = url.strip() , info_labels = datamovie , thumbnail = thumbnail, fanart = fanart , folder = False , isPlayable = False )

    elif url.startswith("peli") == True or url.startswith("serie") == True:
        linker,lbl_server = linker_analyzer(url)
        if linker == "hdfull_linker0": params["extra"]="linker"  # Control para distinguir linker/biblioteca
        elif linker == "oranline_linker0": params["extra"]="linker"
        elif linker == "pelisadicto_linker0": params["extra"]="linker"
        elif linker == "pordede_linker0": params["extra"]="linker" 
        elif linker == "hdfull_linker0": params["extra"]="linker"
        elif linker == "inkapelis_linker0": params["extra"]="linker" 
        elif linker == "cineclasico_linker0": params["extra"]="linker"
        elif linker == "danko_linker0": params["extra"]="linker"  
        elif linker == "peliculasdk_linker0": params["extra"]="linker"
        url = url.replace("peli:", "").replace("serie:", "").strip();params["fanart"] = fanart#url=url.replace("oranline.com/pelicula/", "oranline.com/?review=")
        if plugintools.get_setting("pager_m3u") == "true" and interval == 1: plugintools.add_item( action = linker , title = '[COLOR white]' + title + lbl_server, url = url , page = url, extra = 'regex', thumbnail = thumbnail, fanart = fanart , folder = True , isPlayable = False )
        else: plugintools.add_item( action = linker , title = title + lbl_server, url = url , page = url, extra = 'regex', thumbnail = thumbnail, fanart = fanart , folder = True , isPlayable = False )

    elif url.startswith("bum") == True:
        url = url.strip();texto = url.replace("bum:", "")
        try: min_seeds=texto.split("_")[1];
        except: min_seeds=""
        if min_seeds!="": lbl_bum=' [COLOR '+urlk+'][I][BUM:'+min_seeds+'][/I][/COLOR]'
        else: lbl_bum=' [COLOR lime][I][BUM+][/I][/COLOR]'
        plugintools.addDir( action = "bum_linker" , title = title + lbl_bum, url = url, thumbnail = thumbnail, extra=texto, page=min_seeds, fanart = fanart , folder = True , isPlayable = False )

    elif url.startswith("cbz:") == True:
        if url.find("copy.com") >= 0:
            plugintools.log("CBR Copy.com")
            #url = url.replace("cbz:", "").strip()
        else:
            url = url.replace("cbz:", "").strip()
        title = title.split('"')[0].strip()
        plugintools.add_item( action = "cbx_reader" , title = title+' [COLOR '+urlk+'][I][CBZ][/I][/COLOR]', url = url , plot = datamovie["plot"], info_labels = datamovie , thumbnail = thumbnail, fanart = fanart , folder = True , isPlayable = False )

    elif url.startswith("cbr:") == True:
        if url.find("copy.com") >= 0:
            plugintools.log("CBR Copy.com")
            #url = url.replace("cbr:", "").strip()
        else:
            url = url.replace("cbr:", "").strip();title = title.split('"')[0].strip()
            plugintools.add_item( action = "cbx_reader" , title = title+' [COLOR '+urlk+'][I][CBR][/I][/COLOR]', url = url , plot = plot, info_labels = datamovie , thumbnail = thumbnail, fanart = fanart , folder = True , isPlayable = False )

    elif url.startswith("agendatv:") == True:
        url = url.replace("agendatv:", "").strip()
        if url == "futbolenlatv":
            url = 'http://agenda.futbolenlatv.com/m?deporte=agenda';action = 'futbolentv0'
        elif url == "footballonuktv":
            url = 'http://www.footballonuktv.com/';action = 'agendatv'
        elif url == "calciointv":
            url = 'http://www.calciointv.com/';action = 'agendatv'
        elif url == "futbolenlatele":
            url = 'http://www.futbolenlatele.com';action = 'agendatv'
        elif url == "queverahora":
            url = 'http://www.formulatv.com/programacion/';action = 'epg_verahora'                       
        plugintools.add_item( action = action , title = title+' [COLOR '+urlk+'][I][Agenda[B]TV[/B]][/I][/COLOR]', url = url , plot = datamovie["plot"], info_labels = datamovie , thumbnail = thumbnail, fanart = fanart , folder = False , isPlayable = False )

    elif url.startswith("epg-txt") == True:
        url=url.replace("epg-txt:", "");title_fixed=title
        try: url = epg_txt_dict(parser_title(title_fixed))
        except: url="";pass
        plugintools.add_item( action = "epg_txt0" , title = title+' [COLOR '+urlk+'][I][EPG-TXT][/I][/COLOR]', url = url , plot = datamovie["plot"], info_labels = datamovie , thumbnail = thumbnail, fanart = fanart , folder = False , isPlayable = False )

    elif url.startswith("short") == True:
        url = url.replace("short:", "").strip()
        plugintools.add_item( action = "longurl" , title = title+' [COLOR '+urlk+'][I][shortlink][/I][/COLOR]', url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )

    elif url.startswith("devil") == True:
        url=url.replace("devil:", "");ref="";pageurl=""
        if url.find("referer") >= 0:
            url = url.split(" referer=");pageurl=url[0].strip();ref=url[1].strip()
            if ref != "": url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+pageurl+'%26referer='+ref
            else: url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+pageurl
            url=urllib.quote_plus(url)
            plugintools.add_item( action = "runPlugin" , title = title+' [COLOR '+urlk+'][I][SportsDevil][/I][/COLOR]', plot = plot , url = url , thumbnail = thumbnail, fanart = fanart, folder = False, isPlayable=True)

    elif url.startswith("filtro") == True:
        url = url.replace("filtro:", "");url=url.split(",");filter=url[0];url=url[1]
        if filter.startswith("filtro_gen") == True:
            filter_fixed = filter.replace("filtro_gen:", "").strip();filter_fixed = 'Filtro de género:[B]'+filter_fixed+'[/B]'
        elif filter.startswith("filtro_title") == True:
            filter_fixed = filter.replace("filtro_title:", "").strip();filter_fixed = 'Filtro de título:[B]'+filter_fixed+'[/B]'
        elif filter.startswith("filtro_year") == True:
            filter_fixed = filter.replace("filtro_year:", "").strip();filter_fixed = 'Filtro de Año:[B]'+filter_fixed+'[/B]'
        elif filter.startswith("filtro_dir") == True:
            filter_fixed = filter.replace("filtro_dir:", "").strip();filter_fixed = 'Filtro de Director:[B]'+filter_fixed+'[/B]'
        elif filter.startswith("filtro_cast") == True:
            filter_fixed = filter.replace("filtro_cast:", "").strip();filter_fixed = 'Filtro de Reparto:[B]'+filter_fixed+'[/B]'
        elif filter.startswith("filtro_punt") == True:
            filter_fixed = filter.replace("filtro_punt:", "").strip();filter_fixed = 'Filtro de Puntuación:[B]'+filter_fixed+'[/B]'                        
        else: filter_fixed = 'Filtro desconocido'                  
        plugintools.add_item( action = "getfile_http" , title = '[COLOR white]' + title + '[COLOR '+urlk+'][I] ['+filter_fixed+'][/I][/COLOR]', url = url , info_labels=datamovie, extra = "1" , page=filter, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
        params["plot"]=datamovie

    elif url.startswith("pvr://") == True:
        plugintools.add_item( action="runPlugin" , title=title+' [COLOR '+urlk+'][I[PVR][/I][/COLOR]' , url=url , thumbnail=thumbnail , fanart=fanart , folder = False , isPlayable = False )

    elif url.startswith("plx") == True:
        url = url.replace("plx:", "")  # Se añade parámetro plot porque en las listas PLX no tengo en una función separada la descarga (FIX IT!)
        if title==">>>": title="[COLOR '+urlk+'][I]Siguiente[/I][/COLOR]"
        if plugintools.get_setting("nolabel") == "true": plugintools.add_item( action = "getfile_http" , title = title, plot="", info_labels = datamovie , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
        else: plugintools.add_item( action = "getfile_http" , title = title + ' [COLOR '+urlk+'][I][PLX][/I][/COLOR]', plot="PLX", info_labels = datamovie , url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )

    elif url.startswith("m3u") == True:  # Listas M3U y PLX
        url = url.replace("m3u:", "")
        if url.startswith("desc=") == True:
            url = url.replace("desc=", "").replace('"', "");datamovie = {};datamovie["plot"] = url
            if plugintools.get_setting("nolabel") == "true": plugintools.add_item( action = "getfile_http" , title = title, info_labels = datamovie , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
            else: plugintools.add_item( action = "getfile_http" , title = title + ' [COLOR '+urlk+'][I][M3U][/I][/COLOR]', info_labels = datamovie , url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
        else:
            if plugintools.get_setting("nolabel") == "true": plugintools.add_item( action = "getfile_http" , title = title, url = url ,  thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
            else: plugintools.add_item( action = "getfile_http" , title = title + ' [COLOR '+urlk+'][I][M3U][/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )                                          

    elif url.endswith(".plx") == True or url.find(".plx?action=sortsel") >= 0:
        url = url.replace("plx:", "")  # Se añade parámetro plot porque en las listas PLX no tengo en una función separada la descarga (FIX IT!)
        #plugintools.add_item( action = "plx_items" , plot = "" , title = title+' [COLOR '+urlk+'][I][B]PLX[/B]][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart, folder = True , isPlayable = False )
        if title==">>>": title="[COLOR lightyellow][I]Siguiente[/I][/COLOR]"
        if plugintools.get_setting("nolabel") == "true": plugintools.add_item( action = "getfile_http" , title = title, plot="", info_labels = datamovie , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
        else: plugintools.add_item( action = "getfile_http" , title = title + ' [COLOR '+urlk+'][I][PLX][/I][/COLOR]', plot="PLX", info_labels = datamovie , url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )        

    elif url.find("navixtreme.com/scrape") >= 0 or url.find("navixtreme.com/playlist") >= 0 or url.find(".plx?page=") >= 0:
        if parser_title(title).strip()==">>>": title="[COLOR lightyellow][I]Siguiente[/I][/COLOR]"
        if plugintools.get_setting("nolabel") == "true": plugintools.add_item( action = "getfile_http" , title = title, plot="", info_labels = datamovie , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
        else: plugintools.add_item( action = "getfile_http" , title = title + ' [COLOR '+urlk+'][I][PLX][/I][/COLOR]', plot="PLX", info_labels = datamovie , url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )            

    elif url.startswith("http") == True:
        if url.endswith(".plx") == True or url.find(".plx?action=sortsel") >= 0:
            url = url.replace("plx:", "")  # Se añade parámetro plot porque en las listas PLX no tengo en una función separada la descarga (FIX IT!)
            #plugintools.add_item( action = "plx_items" , plot = "" , title = title+' [COLOR '+urlk+'][I][B]PLX[/B]][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart, folder = True , isPlayable = False )
            if title==">>>": title="[COLOR lightyellow][I]Siguiente[/I][/COLOR]"
            if plugintools.get_setting("nolabel") == "true": plugintools.add_item( action = "getfile_http" , title = title, plot="", info_labels = datamovie , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
            else: plugintools.add_item( action = "getfile_http" , title = title + ' [COLOR '+urlk+'][I][PLX][/I][/COLOR]', plot="PLX", info_labels = datamovie , url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )

        elif url.find("navixtreme.com/scrape") >= 0 or url.find("navixtreme.com/playlist") >= 0 or url.find(".plx?page=") >= 0:
            if parser_title(title).strip()==">>>": title="[COLOR lightyellow][I]Siguiente[/I][/COLOR]"
            if plugintools.get_setting("nolabel") == "true": plugintools.add_item( action = "getfile_http" , title = title, plot="", info_labels = datamovie , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
            else: plugintools.add_item( action = "getfile_http" , title = title + ' [COLOR '+urlk+'][I][PLX][/I][/COLOR]', plot="PLX", info_labels = datamovie , url = url , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )         

        else:
            server = video_analyzer(url)
            if server!= 'unknown':
                plugintools.add_item( action = server , title = title+' [COLOR '+urlk+'][I]['+server+'][/I][/COLOR]' , url = url , thumbnail = thumbnail , info_labels = datamovie , fanart = fanart , folder = False , isPlayable = True )

            elif url.find("ivoox") >= 0:  # Ivoox podcast
                plugintools.addShow( action = "ivoox_regex" , title = title+' [COLOR '+urlk+'][I][iVoox][/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )

            elif url.find("www.youtube.com") >= 0:  # Video youtube
                plugintools.runAddon( action = "play" , title = title+' [[COLOR '+urlk+']You[B]tube[/B] Video][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )

            elif url.find("vimeo.com/channels") >= 0:  # Vimeo Playlist
                plugintools.addDir( action = "vimeo_pl" , title = title+' [COLOR '+urlk+'][I][Vimeo Playlist][/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )

            elif url.find("vimeo.com/video") >= 0:  # Video Vimeo
                plugintools.addShow( action = "vimeo" , title = title+' [COLOR '+urlk+'][I][Vimeo][/I][/COLOR]', url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            
            elif url.find("www.dailymotion.com/playlist") >= 0:  # Dailymotion playlist
                id_playlist = dailym_getplaylist(url)
                if id_playlist != "":
                    if thumbnail == "": thumbnail = 'http://press.dailymotion.com/wp-old/wp-content/uploads/logo-Dailymotion.png'
                    url = "https://api.dailymotion.com/playlist/"+id_playlist+"/videos"
                    plugintools.add_item( action="dailym_pl" , title=title+' [COLOR '+urlk+'][I][B][Dailymotion[/B] playlist][/I][/COLOR]', url=url , fanart = fanart , thumbnail=thumbnail , folder=True, isPlayable=False)

            elif url.find("dailymotion.com/video") >= 0:
                video_id = dailym_getvideo(url)
                if video_id != "":
                    thumbnail = "https://api.dailymotion.com/thumbnail/video/"+video_id+""
                    url = "plugin://plugin.video.dailymotion_com/?url="+video_id+"&mode=playVideo"
                    # Appends a new item to the xbmc item list
                    # API Dailymotion list of video parameters: http://www.dailymotion.com/doc/api/obj-video.html
                    plugintools.add_item( action="play" , title=title+ ' [COLOR [/I][B][Dailymotion[/B] video][/I][/COLOR]' , url=url , thumbnail = thumbnail, fanart = fanart , info_labels = datamovie, isPlayable=True, folder=False )           

            elif url.find("www.youtube.com") >= 0:
                title = title.split('"')[0].strip();videoid = url.replace("https://www.youtube.com/watch?v=", "");url = 'plugin://plugin.video.youtube/play/?video_id='+videoid
                plugintools.runAddon( action = "play" , title = title+' [COLOR '+urlk+'][I]You[B]tube[/B] Video][/I][/COLOR]', url = url ,  thumbnail = thumbnail, fanart = fanart , info_labels = datamovie, folder = False , isPlayable = False )

            elif url.endswith("m3u8") == True:
                title = title.split('"')[0].strip()
                plugintools.add_item( action = "play" , title = title+' [COLOR '+urlk+'][I][m3u8][/I][/COLOR]', url = url , plot = plot , info_labels = datamovie , thumbnail = thumbnail, fanart = fanart , folder = False , isPlayable = True )

            elif url.startswith("cbz") == True:
                if url.find("copy.com") >= 0: pass
                else: url = url.replace("cbz:", "").strip()
                title = title.split('"')[0].strip()             
                plugintools.add_item( action = "cbx_reader" , title = title+' [COLOR '+urlk+'][I][CBZ][/I][/COLOR]', url = url , plot = datamovie["plot"] , info_labels = datamovie , thumbnail = thumbnail ,fanart = fanart , folder = True , isPlayable = False )

            elif url.startswith("cbr") == True:
                if url.find("copy.com") >= 0: pass
                else: url = url.replace("cbr:", "").strip()
                title = title.split('"')[0].strip()             
                plugintools.add_item( action = "cbx_reader" , title = title+' [COLOR '+urlk+'][I][CBR][/I][/COLOR]', url = url , plot = datamovie["plot"], info_labels = datamovie , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )

            elif url.startswith("txt") == True or url.endswith(".txt") == True:
                url = url.replace("txt:", "").strip();title = title.split('"')[0].strip()             
                plugintools.add_item( action = "txt_reader" , title = title+' [COLOR '+urlk+'][I][TXT][/I][/COLOR]', url = url , plot = plot, info_labels = datamovie , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )

            elif url.endswith("acelive") == True:
                title_fixed = parser_title(title);title=title.replace(" ", "+").strip()
                url = p2p_builder_url(url, title_fixed, p2p="ace")
                plugintools.add_item( action = "runPlugin" , title = title+' [COLOR '+urlk+'][I][Acestream][/I][/COLOR]', url = url, thumbnail = thumbnail , fanart = fanart , info_labels = datamovie, folder = False , isPlayable = True )                         

            elif url.startswith("short") == True:
                url.replace("short:", "").strip();title = title_search.split('"')[0].strip()
                plugintools.add_item( action = "longurl" , title = title+' [COLOR '+urlk+'][I][HTTP][/I][/COLOR]', url = url , plot = plot , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )

            elif url.find("veetle.com") >= 0:
                plugintools.add_item( action = "veetle" , title = title+' [COLOR '+urlk+'][I][Veetle][/I][/COLOR]', url = url, thumbnail = thumbnail , fanart = fanart , info_labels = datamovie, folder = False , isPlayable = True )
               
            else: plugintools.add_item( action = "play" , title = title+' [COLOR '+urlk+'][I][HTTP][/I][/COLOR]' , url = url , plot = plot , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )         

    elif url.startswith("rtmp") == True or url.startswith("rtsp") == True:
        url = url.replace("rtmp://$OPT:rtmp-raw=", "").strip();params=plugintools.get_params();params["url"] = url;server_rtmp(params);server = params.get("server");url = params.get("url")
        plugintools.add_item( action = "launch_rtmp" , title = '[COLOR white]' + title + '[COLOR '+urlk+'][I] ['+ server + '][/I][/COLOR]' , plot = plot , url = url , info_labels = datamovie , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )

    elif url.startswith("udp") == True or url.startswith("rtp") == True:
        url = url.replace("rtmp://$OPT:rtmp-raw=", "").strip()
        plugintools.add_item( action = "play" , title = title+' [COLOR '+urlk+'][I][UDP][/I][/COLOR]' , plot = plot , url = url , info_labels = datamovie , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
                            
    elif url.startswith("mms") == True or url.startswith("rtp") == True:
        url = url.replace("rtmp://$OPT:rtmp-raw=", "").strip()
        plugintools.add_item( action = "play" , title = title+' [COLOR '+urlk+'][I][MMS][/I][/COLOR]' , plot = plot , url = url ,  thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )

    elif url.startswith("magnet") == True:  # Magnet links
        title = parser_title(title);url = url.strip()
        plugintools.add_item( action = "launch_magnet" , title = title+' [COLOR '+urlk+'][I][Magnet][/I][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )        

    elif url.startswith("torrent") == True:  # Archivos torrent
        title = parser_title(title);url = url.replace("torrent:", "").strip()
        plugintools.add_item( action = "launch_torrent" , title = title+' [COLOR '+urlk+'][I][Torrent][/I][/COLOR]', url = url , thumbnail = thumbnail , fanart = fanart, folder = False , isPlayable = True )

    elif url.startswith("sop") == True:  # Sopcast
        title = title.split('"')[0].replace("#EXTINF:-1,", "").strip()
        if filtros_on == "true" and params.get("extra") == "1":
            params["title"]=title;params["thumbnail"]=thumbnail;params["fanart"]=fanart;title = filtros0(params, datamovie);url = url.strip();title_fixed=parser_title(title);title_fixed=title_fixed.replace(" ", "+").strip()
            url = p2p_builder_url(url, title_fixed, p2p="sop")
            if title != "": plugintools.add_item( action = "play" , title = title+' [COLOR '+urlk+'][I][Sopcast][/I][/COLOR]', plot = plot , url = url , extra="1", thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
        else:
            title = parser_title(title);url = url.strip();title_fixed=title.replace(" ", "+").strip();title_fixed=parser_title(title);title_fixed=title_fixed.replace(" ", "+").strip();url = p2p_builder_url(url, title_fixed, p2p="sop")
            plugintools.add_item(action="play" , title = title+' [COLOR '+urlk+'][I][Sopcast][/I][/COLOR]' , plot = plot , url = url, thumbnail = thumbnail , fanart = fanart, folder = False , isPlayable = True)

    elif url.startswith("ace") == True:  # Acestream
        title = title.split('"')[0].replace("#EXTINF:-1,", "").strip()
        if filtros_on == "true" and params.get("extra") == "1":
            params["title"]=title;params["thumbnail"]=thumbnail;params["fanart"]=fanart;title = filtros0(params, datamovie);url = url.replace("ace:", "").strip();title_fixed=parser_title(title);title_fixed=title_fixed.replace(" ", "+").strip()
            url = p2p_builder_url(url, title_fixed, p2p="ace")
            if title != "": plugintools.add_item(action="play" , title = '[COLOR white]' + title + ' [COLOR '+urlk+'][I][Acestream][/I][/COLOR]' , plot = plot , url = url, extra="1" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)            
        else:
            title = parser_title(title);url = url.replace("ace:", "");url = url.strip();title_fixed=parser_title(title);title_fixed=title_fixed.replace(" ", "+").strip();url = p2p_builder_url(url, title_fixed, p2p="ace")
            plugintools.add_item(action="play" , title = '[COLOR white]' + title + ' [COLOR '+urlk+'][I][Acestream][/I][/COLOR]' , plot = plot , url = url, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)

    elif url.startswith("yt_playlist") == True:  # Youtube playlist & channel    
        title = title.split('"')[0].replace("#EXTINF:-1,", "");pid = url.replace("yt_playlist(", "").replace(")", "").replace(" ", "").strip();url = 'plugin://plugin.video.youtube/playlist/'+pid+'/'
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + ' [COLOR '+urlk+'][I] [You[B]Tube[/B] Playlist][/I][/COLOR]', url = url.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )        

    elif url.startswith("yt_channel") == True:
        title = title.split('"')[0].replace("#EXTINF:-1,", "");cid = url.replace("yt_channel(", "").replace(")", "").replace(" ", "").strip();url = 'plugin://plugin.video.youtube/channel/'+cid+'/'
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + ' [COLOR '+urlk+'][I] [You[B]Tube[/B] Channel][/I][/COLOR]', url = url.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )
        
    elif url.startswith("yt_user") == True:
        title = title.split('"')[0].replace("#EXTINF:-1,", "");uid = url.replace("yt_user(", "").replace(")", "").replace(" ", "").strip();url = 'plugin://plugin.video.youtube/user/'+uid+'/'
        plugintools.add_item( action = "runPlugin" , title = '[COLOR white]' + title + ' [COLOR '+urlk+'][I] [You[B]Tube[/B] User][/I][/COLOR]', url = url.strip() , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )

    elif url.startswith("yt_video") == True:
        vid = url.replace("yt_video(", "").replace(")", "").replace(" ", "").strip();url = 'plugin://plugin.video.youtube/play/?video_id='+vid
        plugintools.runAddon( action = "play" , title = '[COLOR white]' + title + ' [COLOR '+urlk+'][I] [You[B]Tube[/B] Video][/I][/COLOR]', url = url , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True )
        
    elif url.startswith("ftp") == True:  # Llamadas FTP
        plugintools.add_item( action = "play" , plot = "" , title = title+' [COLOR '+urlk+'][I][FTP][/COLOR]', url = url.strip() ,  thumbnail = thumbnail , fanart = fanart, folder = False , isPlayable = True )

    elif url.startswith("goear") == True:
        if data.startswith("desc") == True: datamovie["plot"] = url.replace("desc=", "").replace('"',"").strip()
        plugintools.add_item( action = "goear" , plot = plot , title = title + ' [COLOR '+urlk+'][I][Goear][/I][/COLOR]', url = url , info_labels = datamovie , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )

    elif url.startswith("txt:") == True or url.endswith("txt") == True:
        url = url.replace("txt:", "").strip();txt_file = url.replace("txt:", "").strip();title = title.split('"')[0].strip()
        plugintools.add_item( action = "txt_reader" , title = title+' [COLOR '+urlk+'][I][TXT][/I][/COLOR]', url = url , plot = plot, info_labels = datamovie , thumbnail = thumbnail, fanart = fanart , folder = False , isPlayable = False )
        

def linker_analyzer(url):
    plugintools.log("[%s %s] Análisis del linkker a ejecutar... %s" % (addonName, addonVersion, url))  # Ver linea 556
    
    if url.startswith("peli") == True:
        if url.find("pelisadicto") >= 0: linker = "pelisadicto_linker0";lbl_linker = ' [COLOR lightgreen][[B]Pelis[/B]adicto][/COLOR]'  
        elif url.find("oranline") >= 0: linker = "oranline_linker0";lbl_linker = ' [COLOR lightgreen][[B]Oranline][/COLOR]'
        elif url.find("pordede") >=0: linker = "pordede_linker0";lbl_linker = ' [COLOR lightgreen][Pordede][/COLOR]'    
        elif url.find("hdfull.tv") >= 0: linker = "hdfull_linker0";lbl_linker = ' [COLOR lightgreen][HDFull][/COLOR]'
        elif url.find("peliculasdk") >= 0: linker = "peliculasdk_linker0";lbl_linker = ' [COLOR lightgreen][PeliculasDK][/COLOR]'
        elif url.find("tv-vip.com") >= 0: linker = "tvvip_linker0";lbl_linker = ' [COLOR lightgreen][[B]TV-VIP][/COLOR]'
        elif url.find("inkapelis") >= 0: linker = "inkapelis_linker0";lbl_linker = ' [COLOR lightgreen][Inkapelis][/COLOR]'
        elif url.find("descargacineclasico") >= 0: linker = "cineclasico_linker0";lbl_linker = ' [COLOR lightgreen][DescargaCineClásico][/COLOR]'
        elif url.find("pelisdanko") >= 0: linker = "danko_linker0";lbl_linker = ' [COLOR lightgreen][[B]Pelis[/B]Danko][/COLOR]'
        elif url.find("jkanime") >= 0: linker = "jkanime_linker0";lbl_linker = ' [COLOR lightgreen][[B]JK[/B]anime][/COLOR]'
        elif url.find("animeflv") >= 0: linker = "animeflv_linker0";lbl_linker = ' [COLOR lightgreen][Anime[B]FLV[/B]][/COLOR]'
        elif url.find("reyanime") >= 0: linker = "reyanime_linker0";lbl_linker = ' [COLOR lightgreen][ReyAnime][/COLOR]'
        else: linker="";lbl_linker = ' [COLOR lightgreen][Unknown linker][/COLOR]'
        
    elif url.startswith("serie") == True:
        plugintools.log("serie: linker")
        if url.find("seriesadicto") >= 0: linker = "pelisadicto_linker0";lbl_linker = ' [COLOR lightgreen][[B]Series[/B]adicto][/COLOR]'    
        elif url.find("seriesflv") >= 0: linker = "seriesflv_linker0";lbl_linker = ' [COLOR lightgreen][[B]Series[/B]FLV][/COLOR]'
        elif url.find("seriesyonkis") >=0: linker = "serieyonkis_linker0";lbl_linker = ' [COLOR lightgreen][[B]Series[/B]Yonkis][/COLOR]'    
        elif url.find("seriesblanco") >= 0: linker = "seriesblanco_linker0";lbl_linker = ' [COLOR lightgreen][[B]Series[/B]Blanco][/COLOR]'
        elif url.find("pordede") >= 0: linker = "pordede_linker0";lbl_linker = ' [COLOR lightgreen][Pordede][/COLOR]'
        elif url.find("hdfull.tv") >= 0: linker = "hdfull_linker0";lbl_linker = ' [COLOR lightgreen][HDFull][/COLOR]'
        elif url.find("tv-vip.com") >= 0: linker = "tvvip_linker0";lbl_linker = ' [COLOR lightgreen][TV-VIP][/COLOR]' 
        elif url.find("inkapelis") >= 0: linker = "inkapelis_linker0";lbl_linker = ' [COLOR lightgreen][Inkapelis][/COLOR]'        
        elif url.find("seriesdanko") >= 0: linker = "danko_linker0";lbl_linker = ' [COLOR lightgreen][[B]Series[/B]Danko][/COLOR]'
        elif url.find("jkanime") >= 0: linker = "jkanime_linker0";lbl_linker = ' [COLOR lightgreen][[B]JK[/B]anime][/COLOR]'
        elif url.find("animeflv") >= 0: linker = "animeflv_linker0";lbl_linker = ' [COLOR lightgreen][Anime[B]FLV[/B]][/COLOR]'
        elif url.find("reyanime") >= 0: linker = "reyanime_linker0";lbl_linker = ' [COLOR lightgreen][ReyAnime][/COLOR]'        
        else: linker="";lbl_linker = ' [COLOR lightgreen][Unknown linker][/COLOR]'

    return linker, lbl_linker

    
def cargapvr0(params):
    for i in json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "PVR.GetChannels", "params": {"channelgroupid": "alltv"},"id": 1}'))['result']['channels']:
        #print str(i['channelid']),i['label'].encode('utf-8','ignore'),'_'*35
        plugintools.add_item(title=i['label'].encode('utf-8','ignore'),action='cargapvr1',url=params['url'],page=str(i['channelid']),thumbnail=params['thumbnail'],fanart=params['fanart'],isPlayable=True,folder=False);
    
def cargapvr1(params):
    play_id=params['page'];query='{"jsonrpc": "2.0","id": 1,"method": "Player.Open","params": {"item": {"channelid": '+play_id+'}}}'
    xbmc.executeJSONRPC(query)
