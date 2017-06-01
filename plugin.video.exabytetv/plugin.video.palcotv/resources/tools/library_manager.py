# -*- coding: utf-8 -*-
#-------------------------------------------------------------------
# Library Manager for PalcoTV
# Kodi Add-on by Juarrox (juarrox@gmail.com)
#-------------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#-------------------------------------------------------------------

import os, sys, urllib, urllib2, re
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import plugintools

from __main__ import *
from resources.tools.media_analyzer import *

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

# Tools & resolvers
from resources.tools.resolvers import *
from resources.tools.mundoplus import *
from resources.tools.bum import *
from resources.tools.yt_playlist import *
from resources.tools.dailymotion import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))


def peli_from_library(params):
    plugintools.log("Playing from library... "+repr(params))
    option_list=[];url_list=[];title=params.get("title");url=params.get("url");plugintools.log("URL= "+url)
    if url.startswith("http") == True:
        data=plugintools.read(url).strip();plugintools.log("title= "+title)
    else: f=open(temp+'PELIS.m3u', "r");data=f.read()
    urls=plugintools.find_single_match(data, '#EXTINF:-1,'+title+'.*?#multi(.*?)#multi');plugintools.log("urls= "+urls)   
    lista_urls=urls.split("\n");url_options=[]
    for entry in lista_urls:
        entry=entry.replace("peli:", "").strip()
        if entry.find("oranline") >= 0:
            titlefull='[COLOR orange][I][Linker] [/COLOR][COLOR white]Oranline[/I][/COLOR]';entry=entry.split("$")[1].strip();option_list.append(titlefull);url_list.append(entry)
        elif entry.find("pordede") >= 0:
            titlefull='[COLOR orange][I][Linker] [/COLOR][COLOR white]Pordede[/I][/COLOR]';entry=entry.split("$")[1].strip();option_list.append(titlefull);url_list.append(entry)
        elif entry.find("inkapelis") >= 0:
            titlefull='[COLOR orange][I][Linker] [/COLOR][COLOR white]Inkapelis[/I][/COLOR]';entry=entry.split("$")[1].strip();option_list.append(titlefull);url_list.append(entry)
        elif entry.find("danko") >= 0:
            titlefull='[COLOR orange][I][Linker] [/COLOR][COLOR white]Danko[/I][/COLOR]';entry=entry.split("$")[1].strip();option_list.append(titlefull);url_list.append(entry)
        elif entry.find("tv-vip.com") >= 0:
            titlefull='[COLOR orange][I][Linker] [/COLOR][COLOR white]TV-VIP[/I][/COLOR]';entry=entry.split("$")[1].strip();option_list.append(titlefull);url_list.append(entry)            
        elif entry.find("peliculasdk") >= 0:
            titlefull='[COLOR orange][I][Linker] [/COLOR][COLOR white]PeliculasDK[/I][/COLOR]';entry=entry.split("$")[1].strip();option_list.append(titlefull);url_list.append(entry)            
        elif entry.find("hdfull") >= 0:
            titlefull='[COLOR orange][I][Linker] [/COLOR][COLOR white]HDFull[/I][/COLOR]';entry=entry.split("$")[1].strip();option_list.append(titlefull);url_list.append(entry)
        elif entry.find("pelisadicto") >= 0:
            titlefull='[COLOR orange][I][Linker] [/COLOR][COLOR white]Pelisadicto[/I][/COLOR]';entry=entry.split("$")[1].strip();option_list.append(titlefull);url_list.append(entry)            
        elif entry.find("descargacineclasico") >= 0:
            titlefull='[COLOR orange][I][Linker] [/COLOR][COLOR white]Cineclásico[/I][/COLOR]';entry=entry.split("$")[1].strip();option_list.append(titlefull);url_list.append(entry)
        elif entry.find("animeflv") >= 0:
            titlefull='[COLOR orange][I][Linker] [/COLOR][COLOR white]AnimeFLV[/I][/COLOR]';entry=entry.split("$")[1].strip();option_list.append(titlefull);url_list.append(entry)
        elif entry.find("jkanime") >= 0:
            titlefull='[COLOR orange][I][Linker] [/COLOR][COLOR white]JkAnime[/I][/COLOR]';entry=entry.split("$")[1].strip();option_list.append(titlefull);url_list.append(entry)
        elif entry.find("reyanime") >= 0:
            titlefull='[COLOR orange][I][Linker] [/COLOR][COLOR white]ReyAnime[/I][/COLOR]';entry=entry.split("$")[1].strip();option_list.append(titlefull);url_list.append(entry)            

    option_list.append("[COLOR orange][I][BUM+] [/COLOR][COLOR white]Buscar torrents...[/I][/COLOR]");url_list.append("torrentz")  # Búsqueda de torrents (deshabilitada temporalmente)
    video = False

    try:
        while video is False:
            option_user = plugintools.selector(option_list, title)
            if option_user > -1:
                url=url_list[option_user];params["url"]=url.replace("https://", "http://").strip();server = video_analyzer(url)
                if server!="unknown": video = True
                elif url.find("hdfull") >= 0:
                    options_hdfull=[];urls_hdfull=[];params["extra"]="library"
                    options_hdfull,urls_hdfull=hd_peli_linker(params)
                    #options_hdfull.append("[COLOR orange][I]Atrás... [/I][/COLOR]");urls_hdfull.append("return")
                    #atras=len(options_hdfull)-1;plugintools.log("atras en= "+str(atras))
                    linker_options = plugintools.selector(options_hdfull, title)
                    if linker_options > -1:
                        url=urls_hdfull[linker_options];params["url"]=url;params["extra"]="library"
                        url=getlink_hdfull_linker(params)
                        video = True
                elif url.find("oranline") >= 0:
                    options_oranline=[];urls_oranline=[];params["extra"]="library"
                    options_oranline,urls_oranline=oranline_linker0(params)
                    linker_options = plugintools.selector(options_oranline, title)
                    if linker_options > -1:
                        url=urls_oranline[linker_options]
                        video = True
                elif url.find("pelisdanko") >= 0:
                    options_dankopelis=[];urls_dankopelis=[];params["extra"]="library"
                    options_dankopelis,urls_dankopelis,params_danko_slug=danko_peli_linker(params)
                    linker_options = plugintools.selector(options_dankopelis, title)                
                    if linker_options > -1:
                        url=urls_dankopelis[linker_options];params["url"]=url;params["extra"]=params_danko_slug;params["page"]="library"
                        url=danko_slug(params)  # Petición URL final
                        video = True
                elif url.find("inkapelis") >= 0:
                    options_inkapelis=[];urls_inkapelis=[];params["extra"]="library"
                    options_inkapelis,urls_inkapelis=inkapelis_linker0(params)
                    linker_options = plugintools.selector(options_inkapelis, title)
                    if linker_options > -1:
                        url=urls_inkapelis[linker_options]
                        video = True
                elif url.find("pelisadicto") >= 0:
                    options_pelisadicto=[];urls_pelisadicto=[];params["extra"]="library"
                    options_pelisadicto,urls_pelisadicto=pelisadicto_linker0(params)
                    linker_options = plugintools.selector(options_pelisadicto, title)
                    if linker_options > -1:
                        url=urls_pelisadicto[linker_options]
                        video = True
                elif url.find("pordede") >= 0:
                    options_pordede=[];urls_pordede=[];params["page"]=url;params["extra"]="library"
                    options_pordede,urls_pordede=pordede_linker0(params)
                    linker_options = plugintools.selector(options_pordede, title)
                    if linker_options > -1:
                        url=urls_pordede[linker_options]
                        params["url"]=url;params["extra"]="library";url=pordede_getlink(params)  # Petición URL final
                        video = True
                elif url.find("peliculasdk") >= 0:
                    options_peliculasdk=[];urls_peliculasdk=[];params["page"]=url;params["extra"]="library"
                    options_peliculasdk,urls_peliculasdk=peliculasdk_linker0(params)
                    linker_options = plugintools.selector(options_peliculasdk, title)
                    if linker_options > -1:
                        url=urls_peliculasdk[linker_options]
                        video = True   
                elif url.find("descargacineclasico") >= 0:
                    options_cineclasico=[];urls_cineclasico=[];params["extra"]="library";params["url"]=url
                    options_cineclasico,urls_cineclasico=cineclasico_linker0(params)
                    linker_options = plugintools.selector(options_cineclasico, title)
                    if linker_options > -1:
                        url=urls_cineclasico[linker_options]
                        video = True
                elif url.find("tv-vip.com") >= 0:
                    options_tvvip=[];urls_tvvip=[];params["extra"]="library";params["url"]=url
                    options_tvvip,urls_tvvip=tvvip_linker0(params)
                    linker_options = plugintools.selector(options_tvvip, title)
                    if linker_options > -1:
                        url=urls_tvvip[linker_options]
                        video = True                        
                elif url.find("torrentz") >= 0:
                    options_tz=[];urls_tz=[]  # Primera opción: [BUM+]
                    options_tz,urls_tz=bum_from_library0(params)  # De la lista de resultados de Torrentz, escogemos los tres con mayor número de semillas
                    bum_options = plugintools.selector(options_tz, title)
                    if bum_options > -1:
                        url=urls_tz[bum_options];params['url']=url;params['title']=options_tz[bum_options]
                        options_tz.append("[COLOR orange][I]Atrás... [/I][/COLOR]")
                        options_tz,urls_tz=bum_from_library1(params)  # Del enlace seleccionado, mostramos en un segundo selector los servidores disponibles
                        option_tz = plugintools.selector(options_tz, title)
                        try:
                            if option_tz > -1:
                                url_item=urls_tz[option_tz]
                                if url_item.find("bitsnoop") >= 0:
                                    r=requests.get(url_item);data=r.content;url = 'magnet'+plugintools.find_single_match(data, '<a href="magnet([^"]+)').strip()                  
                                elif url_item.find("isohunt") >= 0:
                                    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31", "Referer": "https://isohunt.to/"}
                                    r=requests.get(url_item, headers=headers);data=r.content;url = 'magnet'+plugintools.find_single_match(data, '<a href="magnet([^"]+)').strip()
                                elif url_item.find("torrentdownloads") >= 0:
                                    s=requests.Session();s.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0', 'Referer': "https://www.torrentdownloads.me/"}
                                    b=s.get(url_item, allow_redirects=False);cookie='';resp=b.text;heads=b.headers;cook=b.cookies;print cook
                                    for cookies in cook:
                                        cookie+=cookies.name+'='+cookies.value+'; ';s.headers.update({'Cookie':cookie});print cookie
                                        if cookie:
                                            data=resp.encode('utf-8','ignore');bloque_url=plugintools.find_single_match(data, '<span>Magnet:(.*?)</a></p></div>')
                                            url=plugintools.find_single_match(bloque_url, 'href="([^"]+)').strip()
                                elif url_item.find("torrentproject") >= 0 or url_item.find("isohunt") >= 0:
                                    r=requests.get(url_item);data=r.content;url = 'magnet:'+plugintools.find_single_match(data, "magnet:([^']+)").replace("amp;", "").strip()                    
                                elif url_item.find("torlock") >= 0 or url_item.find("torrentreactor") >= 0 or url_item.find("kat.cr") >= 0:  # Parseo común a estas webs: TorrentReactor, Kickass y Torlock
                                    request_headers=[];headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31", "Referer": plugintools.get_setting("kurl")}
                                    r=requests.get(url_item.replace("https", "http"), headers=headers);data=r.content;url = 'magnet:'+plugintools.find_single_match(data, 'magnet:([^"]+)').strip()
                                elif url_item.find("yourbittorrent") >= 0:
                                    request_headers=[];headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31", "Referer": plugintools.get_setting("kurl")}
                                    r=requests.get(url_item, headers=headers);data=r.content;url = plugintools.get_setting("yburl").replace("https", "http")+plugintools.find_single_match(data, 'href=/(.*?).torrent')+'.torrent'
                                    plugintools.log("url= "+url)
                                elif url_item.find("torrenthound") >= 0:
                                    request_headers=[];headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31", "Referer": 'http://www.torrenthound.com/'}
                                    r=requests.get(url_item.replace("https", "http"), headers=headers);data=r.content;bloque=plugintools.find_single_match(data, '<ul id="tmenu">(.*?)<span class="icon fils"');plugintools.log("bloque= "+bloque)
                                    hash=plugintools.find_single_match(bloque, 'hash/([^//]+)');url='http://www.torrenthound.com/torrent/'+hash                               
                                addon_magnet = plugintools.get_setting("addon_magnet")  # Función launch_magnet del módulo media_analyzer
                                if addon_magnet == "0":  # Stream (por defecto)
                                    url = 'plugin://plugin.video.stream/play/'+url_item
                                elif addon_magnet == "1":  # Pulsar
                                    url = 'plugin://plugin.video.pulsar/play?uri=' + url        
                                elif addon_magnet == "2":  # KMediaTorrent
                                    url = 'plugin://plugin.video.kmediatorrent/play/'+url        
                                elif addon_magnet == "3":  # XBMCtorrent
                                    url = 'plugin://plugin.video.xbmctorrent/play/'+url
                                elif addon_magnet == "4":  # Quasar
                                    url = 'plugin://plugin.video.quasar/play?uri=' + url
                                plugintools.log("URL Magnet= "+url);item = xbmcgui.ListItem(path=url);xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item);video=True
                        except KeyboardInterrupt: pass;
                        except IndexError: raise;
                    else: video = True
            else: sys.exit()

    except KeyboardInterrupt: pass;
    except IndexError: raise;
    
    params['url']=str(url);server_analyzer(params);plugintools.log("URL= "+url)

########## DANKO ##########

def dankopelis_library(params):
    plugintools.log('[%s %s] Linker Danko for Kodi Library: %s' % (addonName, addonVersion, repr(params)))    
    url = params.get("url");r = requests.get(url);data = r.content
    cookie_ses = r.cookies['pelisdanko_session'] #cookie de la sesion 
    bloq_film = plugintools.find_single_match(data,'<h3 class="coolfont">Streaming</h3>(.*?)</tbody>')
    film =plugintools.find_multiple_matches(bloq_film,'<tr class="rip hover"(.*?)</tr>')
    for item in film:
        langfull = plugintools.find_multiple_matches(item,'src="http://pelisdanko.com/img/flags/(.*?).png')
        lang = danko_lang(langfull)
        id_vid = plugintools.find_single_match(item,'data-id="([^"]+)"')  #id del video
        slug1 = plugintools.find_single_match(item,'data-slug="([^"]+)"')  #slug del video
        url_slug1 = params.get("url")+'/'+slug1+'/ss?#ss'  #http://pelisdanko.com/peli/deadpool-5233/7V9gGJlcbE1vi7TJ10697/ss?#ss
        params_danko_slug = cookie_ses+'|'+id_vid+'|'+slug1
        quality = plugintools.find_single_match(item,'quality-.*?">([^<]+)</span>').replace(" Real ", "-").strip()
        titlefull = sc+"  Audio: "+ec+sc2+lang+ec2+sc+"  Video: "+ec+" "+sc5+'[I]['+quality+'][/I]'+ec5
        params["extra"]=params_danko_slug
    
    headers = {'Host': 'pelisdanko.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0', 'Referer': params.get("url"),'pelisdanko_session':cookie_ses}    
    r = requests.get(url,headers=headers);data = r.content;option_list=[];url_list=[]
    streaming = plugintools.find_single_match(data,'<h3 class="coolfont">Streaming</h3>(.*?)</iframe>')
    if streaming !="":
        url_streaming = plugintools.find_single_match(streaming,'src="([^"]+)"')
        server = video_analyzer(streaming)
        titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+lang.strip()+'] [/COLOR][COLOR lightblue]['+quality+'][/COLOR][COLOR red][Danko][/I][/COLOR]'
    else: pass
    
    bloq_slug2 = plugintools.find_single_match(data,'class="lnks"><div class="text-center">(.*?)">Mostrar enlaces</span></a>')
    slug2 = plugintools.find_single_match(bloq_slug2,'data-slug="([^"]+)"')    
    headers = {'Host': 'pelisdanko.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0', 'Referer': url,'pelisdanko_session':cookie_ses}
    url = 'http://pelisdanko.com/strms/'+id_vid+'/'+slug1+'/'+slug2
    r = requests.post(url,headers=headers);data = r.content
    bloq_server = plugintools.find_multiple_matches(data,'<tr>(.*?)</tr>')
    for item in bloq_server:
        url_vid = plugintools.find_single_match(item,'<a href="([^"]+)"')
        server = video_analyzer(url_vid)
        titlefull = sc+str(i)+'. '+title_pel+ec+sc5+' [I]['+server+'][/I]'+ec5
        titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+lang.strip()+'] [/COLOR][COLOR lightblue]['+quality+'][/COLOR][COLOR red][Danko][/I][/COLOR]'
        option_list.append(titlefull)
        url_list.append(url_vid) 

    return option_list, url_list     

    
########## ORANLINE ##########

def oranline_library(params):
    plugintools.log('[%s %s] Linker Oranline for Kodi Library: %s' % (addonName, addonVersion, repr(params)))    
    headers = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'}
    url = params.get("url");r = requests.get(url, headers=headers);data = r.content;option_list=[];url_list=[]
    bloque = plugintools.find_single_match(data,'<div id="online">.*?</thead>(.*?)</table>')
    bloque_peli = plugintools.find_multiple_matches(bloque,'<tr>(.*?)</tr>')    
    for entry in bloque_peli:
        lang_audio = plugintools.find_single_match(entry,'</span></td>\s+<td>([^<]+)</td>').replace('Español','ESP').replace('Latino','LAT').replace('Subtítulo','SUB -').replace('Original','V.O.').strip()
        if lang_audio =="":
            lang_audio = plugintools.find_single_match(entry,'</span></td><td>([^<]+)</td>').replace('Español','ESP').replace('Latino','LAT').replace('Subtítulo','SUB -').replace('Original','V.O.').strip()
        formatq = plugintools.find_single_match(entry,'</span></td>\s+<td>[^<]+</td>\s+<td>([^<]+).*?</td>').replace("\t\r\n", "").strip()
        if formatq =="":
            formatq = formatq = plugintools.find_single_match(entry,'</span></td>\<td>[^<]+</td><td>([^<]+).*?</td>')
        server_url = plugintools.find_single_match(entry,'<td><a href="([^"]+)"')
        server = video_analyzer(server_url)
        if server != "":
            titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+lang_audio+'] [/COLOR][COLOR lightblue]['+formatq+'] [/COLOR][COLOR gold][Oranline][/I][/COLOR]'
            option_list.append(titlefull)
            url_list.append(server_url)

    return option_list, url_list


########## INKAPELIS ##########

def inkapelis_library(params):
    plugintools.log("[%s %s] Linker Inkapelis for Kodi Library: %s" % (addonName, addonVersion, repr(params)))   
    url = params.get("url");r = requests.get(url);data = r.content
    option_list=[];url_list=[];i = 1
    while i <= 4:
        lang_embed1 = plugintools.find_single_match(data,'<a href="#embed"'+str(i)+' data-toggle="tab">(.*?)</a>').replace('Español','ESP').replace('Latino','LAT').replace('Subtitulado','SUB').replace('Original','V.O.').strip()
        if lang_embed1 !="":
            quality_embed = plugintools.find_single_match(data,'id="embed1"><div class="calishow">(.*?)</div>')
            url_embed = plugintools.find_single_match(data,'id="embed1">.*?src="([^"]+)"')
            server = video_analyzer(url_embed)
            titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+lang_embed.strip()+'] [/COLOR][COLOR lightblue]['+quality_embed.replace(" Real ", "-")+'] [/COLOR][COLOR gold][Inkapelis][/I][/COLOR]'
            option_list.append(titlefull1)
            url_list.append(url_embed1)
            i = i + 1
        else: pass
  
    bloq_server = plugintools.find_single_match(data,'class="dlmt">Opciones Para Ver Online</h2>(.*?)class="dlmt">Opciones Para Descargar</h2>')
    serverfull = plugintools.find_multiple_matches(bloq_server,'<tr><td>(.*?)</tr>')
    for item in serverfull:
    	lang = plugintools.find_single_match(item,'</span></td><td>([^<]+)</td><td>').replace('Español','ESP').replace('Latino','LAT').replace('Subtítulo','SUB -').replace('Subtitulado','SUB').replace('Original','V.O.').strip()
    	quality = plugintools.find_single_match(item,'</span></td><td>.*?</td><td>([^<]+)</td>').strip()
        url_vid = plugintools.find_single_match(item,'<a href="([^"]+)"')
        server = video_analyzer(url_vid)
        titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+lang.strip()+'] [/COLOR][COLOR lightblue]['+quality.replace(" Real ", "-")+'] [/COLOR][COLOR gold][Inkapelis][/I][/COLOR]'
        option_list.append(titlefull)
        url_list.append(url_vid)

    return option_list, url_list


########## HDFULL ##########

def hdfull_library(params):
    plugintools.log("[%s %s] Linker HDfull for Kodi Library %s" % (addonName, addonVersion, repr(params)))
    url = params.get("url");r = requests.get(url);data = r.content;option_list=[];url_list=[]
    title = plugintools.find_single_match(data,'<div id="summary-title" itemprop="name">([^<]+)</div>').upper()
    bloq_film = plugintools.find_single_match(data,'<div class="row-pages-wrapper">(.*?)<div id="link_list"')
    film =plugintools.find_multiple_matches(bloq_film,'<div class="embed-selector"(.*?)<div class="embed-movie">')
    for item in film:
        lang = plugintools.find_single_match(item,'Idioma:.*?</b>([^<]+)</span>').strip().replace("\n","").replace("\t","").replace('&ntilde;','ñ')
        lang = lang.replace('&aacute;','á').replace('&eacute;','é').replace('&iacute;','í').replace('&oacute;','ó').replace('&uacute;','ú')
        lang = lang.replace('Audio','').replace('Español','ESP').replace('Latino','LAT').replace('Subtítulo','SUB -').replace('Original','V.O.')
        serverfull = plugintools.find_single_match(item,'class="provider" style="background-image: url\(.*?\)">([^<]+)</b>')
        quality = plugintools.find_single_match(item,'Calidad:.*?</b>([^<]+)</span>').strip().replace("\n","").replace("\t","")
        id_vid = plugintools.find_single_match(item,'onclick="reportMovie\((.*?)\)')
        url_vid = plugintools.find_single_match(item,'<a href="javascript.*?<a href="([^"]+)"')
        server = video_analyzer(url_vid)
        titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+lang.strip()+'] [/COLOR][COLOR lightblue]['+quality+'] [/COLOR][COLOR gold][HDFull][/I][/COLOR]'
        option_list.append(titlefull);url_list.append(url_vid)

    return option_list, url_list

def hdfull_series_library(params):
    url = params.get("url");r = requests.get(url);data = r.content;option_list=[];url_list=[]
    bloq_film = plugintools.find_single_match(data,'<div class="row-pages-wrapper">(.*?)<div id="link_list"')
    film =plugintools.find_multiple_matches(bloq_film,'<div class="embed-selector"(.*?)<div class="embed-movie">')
    for item in film:
        lang = plugintools.find_single_match(item,'Idioma:.*?</b>([^<]+)</span>').strip().replace("\n","").replace("\t","").replace('&ntilde;','ñ')
        lang = lang.replace('&aacute;','á').replace('&eacute;','é').replace('&iacute;','í').replace('&oacute;','ó').replace('&uacute;','ú')
        lang = lang.replace('Audio','').replace('Español','ESP').replace('Latino','LAT').replace('Subtítulo','SUB -').replace('Original','V.O')
        quality = plugintools.find_single_match(item,'Calidad:.*?</b>([^<]+)</span>').strip().replace("\n","").replace("\t","")
        url_vid = plugintools.find_single_match(item,'<a href="javascript.*?<a href="([^"]+)"')
        server = video_analyzer(url_vid)
        titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+lang.strip()+'] [/COLOR][COLOR lightblue]['+quality+'] [/COLOR][COLOR gold][HDFull][/I][/COLOR]'
        option_list.append(titlefull);url_list.append(url_vid)

########## PELISADICTO ##########

def pelisadicto_library(params):
    plugintools.log("[%s %s] Linker Pelisadicto for Kodi Library %s" % (addonName, addonVersion, repr(params)))    
    url = params.get("url");r = requests.get(url);data = r.content;option_list=[];url_list=[]
    title = plugintools.find_single_match(data,'<meta property="og:title" content="(.*?)\(').strip()
    if title =="": title = plugintools.find_single_match(data,'<meta property="og:title" content="(.*?)"')
    bloq_link = plugintools.find_single_match(data,'<tbody>(.*?)</table>')
    link = plugintools.find_multiple_matches(bloq_link,'<tr>(.*?)</tr>')
    for item in link:
        lang = plugintools.find_single_match(item,'<td><img src="([^"]+)"')
        try:
            if '1.png' in lang: lang = 'ESP'
            if '2.png' in lang: lang = 'LAT'
            if '3.png' in lang: lang = 'ENG-SUB'
            if '4.png' in lang: lang = 'ENG'            
        except: lang=""        
        quality = plugintools.find_single_match(item,'<td><img src=".*?</td>\s+<td>(.*?)</td>')
        url_vid = plugintools.find_single_match(item,' href="([^"]+)"')
        server = video_analyzer(url_vid)
        titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+lang.strip()+'] [/COLOR][COLOR lightblue]['+quality+'] [/COLOR][COLOR gold][Pelisadicto][/I][/COLOR]'
        option_list.append(titlefull);url_list.append(url_vid)

    return option_list, url_list


########## PORDEDE ##########

def pordede_library(params):
    plugintools.log("[%s %s] Linker Pordede for Kodi Library%s" % (addonName, addonVersion, repr(params)))
    pdd_url='http://www.pordede.com';page_url = params.get("page");option_list=[];url_list=[]
    if plugintools.get_setting("pordede_user") == "":
        plugintools.add_item(action="", title="Habilita tu cuenta de pordede en la configuración", folder=False, isPlayable=False)
    else:
        url = "http://www.pordede.com/site/login"
        post = "LoginForm[username]="+plugintools.get_setting("pordede_user")+"&LoginForm[password]="+plugintools.get_setting("pordede_pwd")
        headers = DEFAULT_HEADERS[:]       
        body,response_headers = plugintools.read_body_and_headers(url,post=post)
        try:
            if os.path.exists(temp+'pordede.com') is True:
                print "Eliminando carpeta caché..."
                os.remove(temp+'pordede.com')
        except: pass
        
        headers = DEFAULT_HEADERS[:]
        body,response_headers = plugintools.read_body_and_headers(page_url,headers=headers)
        info_user = plugintools.find_single_match(body,'<div class="userinfo">(.*?)</div>')
        usuario = plugintools.find_single_match(info_user,'<div class="friendMini shadow" title="(.*?)"')
        plugintools.log("usuario= "+usuario)
        avatar = plugintools.find_single_match(info_user,'src="(.*?)"')
        plugintools.log("avatar= "+avatar)
        if 'defaultavatar.png' in avatar: avatar = thumbnail

        bloq_fich = plugintools.find_single_match(body,'<div class="sidebar">(.*?)<h2 class="info">Más información</h2>')
        logo = plugintools.find_single_match(bloq_fich,'onerror="this.src=\'/images/logo.png\'" src="(.*?)"')
        if logo =="":
            logo = thumbnail
        fondo = plugintools.find_single_match(body,'onerror="controller.noBigCover.*?src="(.*?)"')
        if fondo =="":
            fondo = fanart
        info_vid = plugintools.find_single_match(body,'<div class="main">(.*?)<div class="centered">')
        sinopsis = plugintools.find_single_match(info_vid,'style="max-height: 140px;overflow:hidden">(.*?)</div>').strip()
        if "peli" in page_url:
            title = plugintools.find_single_match(info_vid,'<h1>(.*?)</h1>').replace("&amp;","&")#.upper()
            id_ajax = plugintools.find_single_match(body,'data-model="peli" data-id="([^"]+)">') #id necesario marcado como visto
            plugintools.log("id_ajax= "+id_ajax)
            #url y parametros para marcar como visto (params Extra)
            parametros_ajax = 'http://www.pordede.com/ajax/mediaaction|model=peli&id='+id_ajax+'&action=status&value=3|'+page_url 
            status = plugintools.find_single_match(body,'controller.userStatus(.*?);').split(',') #marcada en la web
            #comprobado si esta marcada como vista
            if "3" in status[2]:
                title = plugintools.find_single_match(info_vid,'<h1>(.*?)</h1>').replace("&amp;","&")#.upper()
                titlefull = '[COLOR white]['+str(title)+'][/COLOR] [COLOR red][Vista] [/COLOR][COLOR gold][Pordede][/I][/COLOR]'
            else:
                titlefull = '[COLOR white]['+str(title)+'][/COLOR] [/COLOR][COLOR gold][Pordede][/I][/COLOR]'
        elif "serie" in page_url:
            title = plugintools.find_single_match(info_vid,'<h1>(.*?)<span class="titleStatus">').replace("&amp;","&")
            if title =="":
                title = plugintools.find_single_match(info_vid,'<h1>(.*?)</h1>').replace("&amp;","&")

            status = plugintools.find_single_match(info_vid,'<h1>.*?<span class="titleStatus">(.*?)</span></h1>')
            if status =="": status = '(N/D)'
            titlefull = sc5+"[B]"+str(title)+"[/B]"+" ("+str(status)+")"+ec5
            titlefull = '[COLOR white]['+str(title)+'][/COLOR] [COLOR red]['+str(status)+'] [/COLOR][COLOR gold][Pordede][/I][/COLOR]'
            
        punt = plugintools.find_single_match(bloq_fich,'<span class="puntuationValue" data-value="(.*?)"')
        year_duration = plugintools.find_single_match(bloq_fich,'<p class="info">(.*?)</p>.*?<p class="info">(.*?)</p>')

        bloq_genr = plugintools.find_single_match(body,'<h2 class="info genresTitle">Géneros</h2>(.*?)</p>')
        genrfull = plugintools.find_multiple_matches(bloq_genr,'href=".*?">([^<]+)<')
        genr = pordede_genr(genrfull)

        url_links = plugintools.find_single_match(info_vid,'<button class="defaultPopup big" href="(.*?)"')
        url_linksfull = pdd_url + url_links
        plugintools.log("url_links= "+url_linksfull)
        
        if url_links !="":
            body,response_headers = plugintools.read_body_and_headers(url_linksfull) 
            bloq_aport = plugintools.find_single_match(body,'<ul class="linksList">(.*?)<ul class="linksList">')
            aport = plugintools.find_multiple_matches(bloq_aport, '<a target="_blank" class="a aporteLink done"(.*?)</a>')
            for item in aport:
                link_ok = plugintools.find_single_match(item,'class="num green"><span data-num="(.*?)"')
                link_ko = plugintools.find_single_match(item,'class="num red"><span data-num="(.*?)"')
                if int(link_ok) >= int(link_ko):
                    name_server = plugintools.find_single_match(item,'popup_(.*?)">').replace(".png","").capitalize()
                    url = plugintools.find_single_match(item,'href="(.*?)"')
                    url_aport = pdd_url+url          
                    idiomas = re.compile('<div class="flag([^"]+)">([^<]+)</div>',re.DOTALL).findall(item)
                    idioma_0 = (idiomas[0][0].replace("&nbsp;","").strip() + " " + idiomas[0][1].replace("&nbsp;","").strip()).strip()
                    if len(idiomas) > 1:
                        idioma_1 = (idiomas[1][0].replace("&nbsp;","").strip() + " " + idiomas[1][1].replace("&nbsp;","").strip()).strip()
                        idioma = idioma_0+" - "+idioma_1
                    else:
                        idioma_1 = ''
                        idioma = idioma_0
                    idioma=idioma.replace("spanish", "ESP").replace("english", "ENG").replace("spanish SUB", "SUB-ESP").replace("english SUB", "SUB-ENG").replace("german", "GER")
                    calidad_video = plugintools.find_single_match(item,'<div class="linkInfo quality"><i class="icon-facetime-video"></i>([^<]+)</div>').strip()
                    calidad_audio = plugintools.find_single_match(item,'<div class="linkInfo qualityaudio"><i class="icon-headphones"></i>([^<]+)</div>').strip()
                    titlefull = '[COLOR white]'+name_server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+idioma.strip()+'] [/COLOR][COLOR lightblue]['+calidad_video+'/'+calidad_audio+'] [/COLOR][COLOR gold][Pordede][/I][/COLOR]'
                    option_list.append(titlefull)
                    plugintools.log("parametros_ajax= "+parametros_ajax)
                    url_post = parametros_ajax.split("|")[0]
                    post = parametros_ajax.split("|")[1]  #El post viene montado desde la funcion
                    url = parametros_ajax.split("|")[2]
                    headers = {"Host":"www.pordede.com","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Referer": url}
                    body,response_headers = plugintools.read_body_and_headers(url_post,post=post,headers=headers)  #Enviando los parametros para marcar visto                 
                    goto = plugintools.find_single_match(body,'<p class="nicetry links">(.*?)target="_blank"')
                    link_redirect = plugintools.find_single_match(goto,'<a href="(.*?)"')
                    link_redirect = pdd_url + link_redirect
                    url_list.append(link_redirect)                
        else:
            headers = DEFAULT_HEADERS[:]
            body,response_headers = plugintools.read_body_and_headers(url,headers=headers)
            temporada = '<div class="checkSeason"[^>]+>([^<]+)<div class="right" onclick="controller.checkSeason(.*?)\s+</div></div>'
            itemtemporadas = re.compile(temporada,re.DOTALL).findall(body)
            for nombre_temporada,bloque_episodios in itemtemporadas:
                patron  = '<span class="title defaultPopup" href="([^"]+)"><span class="number">([^<]+)</span>([^<]+)</span>(\s*</div>\s*<span[^>]*><span[^>]*>[^<]*</span><span[^>]*>[^<]*</span></span><div[^>]*><button[^>]*><span[^>]*>[^<]*</span><span[^>]*>[^<]*</span></button><div class="action([^"]*)" data-action="seen">)?'
                matches = re.compile(patron,re.DOTALL).findall(bloque_episodios)
                num_temp = nombre_temporada.replace("Temporada","").replace("Extras","Extras 0")
                for item in matches:
                    id_ajax = plugintools.find_single_match(item[0],'/links/viewepisode/id/([0-9]*)')  #id necesario marcado como visto
                    parametros_ajax = 'http://www.pordede.com/ajax/action|model=episode&id='+id_ajax+'&action=seen&value=1|'+url #url y parametros para marcar como visto (params Extra)
                    visto = plugintools.find_single_match(item[3],'</button><div class="([^"]+)"')
                    if 'action active' in visto:
                        title = item[2]
                        titlefull = '[COLOR white]['+num_temp.title()+'x'+item[1].strip()+'][/COLOR][COLOR lightyellow][I]['+title.strip()+'] [/COLOR] [COLOR red][Visto] [/COLOR][COLOR gold][Pordede][/I][/COLOR]'
                    else:
                        title = item[2]
                        titlefull = '[COLOR white]['+num_temp.title()+'x'+item[1].strip()+'][/COLOR][COLOR lightyellow][I]['+title.strip()+'] [/COLOR] [COLOR gold][Pordede][/I][/COLOR]'
                    url = web+item[0];option_list.append(titlefull);url_list.append(url)

    return option_list, url_list, parametros_ajax

def pordedeseries0_library(params):
    parametros_ajax = params.get("extra")  #Recibe los parametros necesarios para marcar como visto (split '|')
    url = params.get("url");option_list=[];url_list=[]
    body,response_headers = plugintools.read_body_and_headers(url) 
    bloq_aport = plugintools.find_single_match(body,'<ul class="linksList">(.*?)<ul class="linksList">')
    aport = plugintools.find_multiple_matches(bloq_aport, '<a target="_blank" class="a aporteLink done"(.*?)</a>')
    for item in aport:
        link_ok = plugintools.find_single_match(item,'class="num green"><span data-num="(.*?)"')
        link_ko = plugintools.find_single_match(item,'class="num red"><span data-num="(.*?)"')
        if int(link_ok) >= int(link_ko):
            name_server = plugintools.find_single_match(item,'popup_(.*?)">').replace(".png","").capitalize()
            url = plugintools.find_single_match(item,'href="(.*?)"')
            url_aport = web+url   
            idiomas = re.compile('<div class="flag([^"]+)">([^<]+)</div>',re.DOTALL).findall(item)
            idioma_0 = (idiomas[0][0].replace("&nbsp;","").strip() + " " + idiomas[0][1].replace("&nbsp;","").strip()).strip()
            if len(idiomas) > 1:
                idioma_1 = (idiomas[1][0].replace("&nbsp;","").strip() + " " + idiomas[1][1].replace("&nbsp;","").strip()).strip()
                idioma = idioma_0+" - "+idioma_1
            else:
                idioma_1 = ''
                idioma = idioma_0
            idioma=idioma.replace("spanish", "Esp").replace("english", "Eng").replace("spanish SUB", "Sub-Esp").replace("english SUB", "Sub-Eng").replace("german", "Ger")
            calidad_video = plugintools.find_single_match(item,'<div class="linkInfo quality"><i class="icon-facetime-video"></i>([^<]+)</div>').strip()
            calidad_audio = plugintools.find_single_match(item,'<div class="linkInfo qualityaudio"><i class="icon-headphones"></i>([^<]+)</div>').strip()
            titlefull = '[COLOR white]'+name_server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+idioma.strip()+'] [/COLOR][COLOR lightblue]['+calidad_video+'/'+calidad_audio+'] ['+link_ok+'/'+link_ko+'] [/COLOR][COLOR gold][Pordede][/I][/COLOR]'
            option_list.append(titlefull)
            url_list.append(url_aport)

    return option_list, url_list, parametros_ajax

def pordedeseries1_library(params):    
    parametros_ajax = params.get("extra").split('|')  #Recibe los parametros necesarios para marcar como visto (split '|')
    url_post = parametros_ajax[0]
    post = parametros_ajax[1]  #El post viene montado desde la funcion
    url = parametros_ajax[2]
    headers = {"Host":"www.pordede.com","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Referer": url}
    body,response_headers = plugintools.read_body_and_headers(url_post,post=post,headers=headers)  #Enviando los parametros para marcar visto
    link = params.get("url")
    title = params.get("title")    
    body,response_headers = plugintools.read_body_and_headers(link)
    goto = plugintools.find_single_match(body,'<p class="nicetry links">(.*?)target="_blank"')
    link_redirect = plugintools.find_single_match(goto,'<a href="(.*?)"')
    link_redirect = web + link_redirect    
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Referer": link}
        body,response_headers = plugintools.read_body_and_headers(link_redirect) 
        #print body
        for i in response_headers:
		 if i[0]=='location':location=i[1]
        if location:print '$'*25+'- By PalcoTV Team -'+'$'*25,location,'$'*69
       
        if "allmyvideos" in location: media_url = location; params["url"]=media_url; allmyvideos(params)
        elif "streamcloud" in location: media_url = location; params["url"]=media_url; streamcloud(params)
        elif "played.to" in location: media_url = location; params["url"]=media_url; playedto(params)
        elif "vidspot" in location: media_url = location; params["url"]=media_url; vidspot(params)
        elif "vk" in location: media_url = location; params["url"]=media_url; vk(params)
        elif "nowvideo" in location: media_url = location; params["url"]=media_url; nowvideo(params)
        elif "tumi.tv" in location: media_url = location; params["url"]=media_url; tumi(params)
        elif "veehd" in location: media_url = location; params["url"]=media_url; veehd(params)
        elif "turbovideos.net" in location: media_url = location; params["url"]=media_url; turbovideos(params)
        elif "streamin.to" in location: media_url = location; params["url"]=media_url; streaminto(params)
        elif "powvideo" in location: media_url = location; params["url"]=media_url; powvideo(params)
        elif "mail.ru" in location: media_url = location; params["url"]=media_url; mailru(params)
        elif "mediafire" in location: media_url = location; params["url"]=media_url; mediafire(params)
        elif "novamov" in location: media_url = location; params["url"]=media_url; novamov(params)
        elif "gamovideo" in location: media_url = location; params["url"]=media_url; gamovideo(params)
        elif "moevideos" in location: media_url = location; params["url"]=media_url; moevideos(params)
        elif "movshare" in location: media_url = location; params["url"]=media_url; movshare(params)
        elif "movreel" in location: media_url = location; params["url"]=media_url; movreel(params)
        elif "videobam" in location: media_url = location; params["url"]=media_url; videobam(params)
        elif "vimeo" in location: media_url = location; params["url"]=media_url; vimeo(params)
        elif "veetle" in location: media_url = location; params["url"]=media_url; veetle(params)
        elif "videoweed" in location: media_url = location; params["url"]=media_url; videoweed(params)
        elif "streamable" in location: media_url = location; params["url"]=media_url; streamable(params)
        elif "rocvideo" in location: media_url = location; params["url"]=media_url; rocvideo(params)
        elif "realvid" in location: media_url = location; params["url"]=media_url; realvid(params)
        elif "netu.tv" in location: media_url = location; params["url"]=media_url; netu(params)
        elif "waaw" in location: media_url = location; params["url"]=media_url; waaw(params)
        elif "videomega" in location: media_url = location; params["url"]=media_url; videomega(params)
        elif "Video.tt" in location: media_url = location; params["url"]=media_url; videott(params)
        elif "flashx" in location: media_url = location; params["url"]=media_url; flashx(params)
        elif "ok.ru" in location: media_url = location; params["url"]=media_url; okru(params)
        elif "vidto.me" in location: media_url = location; params["url"]=media_url; vidtome(params)
        elif "playwire" in location: media_url = location; params["url"]=media_url; playwire(params)
        elif "uptostream.com" in location: media_url = location; params["url"]=media_url; uptostream(params)
        elif "youwatch" in location: media_url = location; params["url"]=media_url; youwatch(params)
        elif "vidgg.to" in location: media_url = location; params["url"]=media_url; vidggto(params)
        elif "vimple.ru" in location: media_url = location; params["url"]=media_url; vimple(params)
        elif "idowatch.net" in location: media_url = location; params["url"]=media_url; idowatch(params)
        elif "cloudtime.to" in location: media_url = location; params["url"]=media_url; cloudtime(params)
        elif "vidzi.tv" in location: media_url = location; params["url"]=media_url; vidzitv(params)
        elif "vodlocker" in location: media_url = location; params["url"]=media_url; vodlocker(params)
        elif "streame.net" in location: media_url = location; params["url"]=media_url; streamenet(params)
        elif "watchonline" in location: media_url = location; params["url"]=media_url; watchonline(params)
        elif "rutube.ru" in location: media_url = location; params["url"]=media_url; rutube(params)
        elif "dailymotion" in location: media_url = location; params["url"]=media_url; dailymotion(params)
        elif "auroravid" in location: media_url = location; params["url"]=media_url; auroravid(params)
        elif "wholecloud.net" in location: media_url = location; params["url"]=media_url; wholecloud(params)
        elif "bitvid" in location: media_url = location; params["url"]=media_url; bitvid(params)
        elif "spruto.tv" in location: media_url = location; params["url"]=media_url; spruto(params)
        elif "stormo.tv" in location: media_url = location; params["url"]=media_url; stormo(params)
        elif "myvi.ru" in location: media_url = location; params["url"]=media_url; myviru(params)
        elif "youtube.com" in location: media_url = location; params["url"]=media_url; youtube(params)
        elif "filmon.com" in location: media_url = location; params["url"]=media_url; filmon(params)
        elif "thevideo.me" in location: media_url = location; params["url"]=media_url; thevideome(params)
        elif "videowood.tv" in location: media_url = location; params["url"]=media_url; videowood(params)
        elif "neodrive.co" in location: media_url = location; params["url"]=media_url; neodrive(params)
        elif "thevideobee.to" in location: media_url = location; params["url"]=media_url; thevideobee(params)
        elif "fileshow.tv" in location: media_url = location; params["url"]=media_url; fileshow(params)
        elif "vid.ag" in location: media_url = location; params["url"]=media_url; vid(params)
        elif "vidxtreme.to" in location: media_url = location; params["url"]=media_url; vidxtreme.to(params)
        elif "vidup" in location: media_url = location; params["url"]=media_url; vidup(params)
        elif "watchvideo" in location: media_url = location; params["url"]=media_url; watchvideo(params)
        elif "speedvid" in location: media_url = location; params["url"]=media_url; speedvid(params)
        elif "chefti.info" in location: media_url = location; params["url"]=media_url; exashare(params)
        elif "vodbeast" in location: media_url = location; params["url"]=media_url; vodbeast(params)
        elif "nosvideo" in location: media_url = location; params["url"]=media_url; nosvideo(params)
        elif "noslocker" in location: media_url = location; params["url"]=media_url; noslocker(params)
        elif "up2stream" in location: media_url = location; params["url"]=media_url; up2stream(params)                
    except: pass

 
########## [BUM+] TORRENTZ ##########
 
def bum_from_library0(params):
    plugintools.log('[%s %s] [BUM+] Searching magnet links for Kodi Library... %s' % (addonName, addonVersion, repr(params)))
    tzurl=plugintools.get_setting("tzurl").replace("https", "http");url = tzurl+'search?q='+params.get("title").lower().replace(" ", "+").strip();plugintools.log("url busqueda torrentz= "+url)
    r=requests.get(url);resp=r.text;data=resp.encode('utf-8','ignore');option_list=[];url_list=[]
    items=plugintools.find_multiple_matches(data, '<dl>(.*?)</dl>')
    i = 0
    for entry in items:
        page_url = tzurl + plugintools.find_single_match(entry, 'href="/([^"]+)')
        title=plugintools.find_single_match(entry, '<a href[^>]+>(.*?)</dt>').replace("<b>", "").replace("</b>", "").replace("<strong>", "").replace("</strong>", "").replace("<a>", "").replace("</a>", "").split("&#187;")[0].strip()
        try:
            size=plugintools.find_single_match(entry, '<span class="s">(.*?)</span>')
            plugintools.log("size= "+size)
            seeds=plugintools.find_single_match(entry, '<span class="u">(.*?)</span>').replace(",", "").strip()
            plugintools.log("seeds= "+seeds)
        except: seeds="0";size="0"
        if title!= "" and size!="0" and size!="" and i<5:
            titlefull = '[COLOR white]'+title.title()+' '+'[/COLOR][COLOR lightyellow][I]['+seeds+'] [/COLOR][COLOR lightblue]['+size+'] [/I][/COLOR]'
            option_list.append(titlefull);url_list.append(page_url)
            i = i + 1
            
    return option_list, url_list
              
def bum_from_library1(params):
    plugintools.log('[%s %s] [BUM+] Magnet link options for Kodi Library... %s' % (addonName, addonVersion, repr(params)))
    url=params.get("url").replace("https", "http");url_list=[];option_list=[]
    s=requests.Session();s.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0', 'Referer': "https://www.torrentdownloads.me/"}
    b=s.get(url, allow_redirects=False);cookie=''
    resp=b.text;heads=b.headers;cook=b.cookies;print cook;
    for cookies in cook:
        cookie+=cookies.name+'='+cookies.value+'; ';s.headers.update({'Cookie':cookie});print cookie
    if cookie:
        data=resp.encode('utf-8','ignore')
        title,dls=plugintools.find_single_match(data, '<h2><span>(.*?)</span>(.*?)</h2>')        
        results=plugintools.find_single_match(data, '<div class="download">(.*?)</p></div>')
        items=plugintools.find_multiple_matches(results, '<dl><dt>(.*?)</span></dd></dl>')
        for item in items:
            url_item= plugintools.find_single_match(item, 'href="([^"]+)')
            plugintools.log("url_item= "+url_item)
            server = plugintools.find_single_match(item, '<span class="u".*?>(.*?)<')
            if server.startswith("Download") == False:
                plugintools.log("title= "+params.get("title"))
                titlefull=' [COLOR gold]'+server+'[/COLOR] '+params.get("title").split("[/COLOR]")[1]+'[/COLOR]'+params.get("title").split("[/COLOR]")[2]+'[/COLOR]'
                url_list.append(url_item);option_list.append(titlefull)
            
            
    return option_list, url_list
                     


def series_from_library(params):
    plugintools.log("SERIES from library... "+repr(params))
    option_list=[];url_list=[];title=params.get("title")
    #data=plugintools.read(params.get("url"))  # Leemos base de datos de películas (Lista M3U)
    f=open(temp+'SERIES.m3u', "r");data=f.read()
    urls=plugintools.find_single_match(data, '#EXTINF:-1,'+title+'.*?#multi(.*?)#multi')    
    lista_urls=urls.split("\n");url_options=[]
    for entry in lista_urls:
        entry=entry.replace("peli:", "").strip()
        if entry.find("seriesyonkis") >= 0:
            titlefull='[COLOR orange][I][Linker] [/COLOR][COLOR white]SeriesYonkis[/I][/COLOR]';entry=entry.split("$")[1].strip();option_list.append(titlefull);url_list.append(entry)
        elif entry.find("pordede") >= 0:
            titlefull='[COLOR orange][I][Linker] [/COLOR][COLOR white]Pordede[/I][/COLOR]';entry=entry.split("$")[1].strip();option_list.append(titlefull);url_list.append(entry)
        elif entry.find("seriesblanco") >= 0:
            titlefull='[COLOR orange][I][Linker] [/COLOR][COLOR white]SeriesBlanco[/I][/COLOR]';entry=entry.split("$")[1].strip();option_list.append(titlefull);url_list.append(entry)
        elif entry.find("seriesflv") >= 0:
            titlefull='[COLOR orange][I][Linker] [/COLOR][COLOR white]SeriesFLV[/I][/COLOR]';entry=entry.split("$")[1].strip();option_list.append(titlefull);url_list.append(entry)
        elif entry.find("seriesadicto") >= 0:
            titlefull='[COLOR orange][I][Linker] [/COLOR][COLOR white]Seriesadicto[/I][/COLOR]';entry=entry.split("$")[1].strip();option_list.append(titlefull);url_list.append(entry)            
        elif entry.find("hdfull") >= 0:
            titlefull='[COLOR orange][I][Linker] [/COLOR][COLOR white]HDFull[/I][/COLOR]';entry=entry.split("$")[1].strip();option_list.append(titlefull);url_list.append(entry)

    option_list.append("[COLOR orange][I][BUM+] [/COLOR][COLOR white]Buscar torrents...[/I][/COLOR]");url_list.append("torrentz")  # Búsqueda de torrents
    video = False

    try:
        while video is False:
            option_user = plugintools.selector(option_list, title)
            if option_user > -1:
                url=url_list[option_user]
                params["url"]=url.replace("https://", "http://").replace("serie:", "").strip();cap=params.get("cap")                
                if int(cap) <= 9: cap = "0"+str(cap);plugintools.log("cap= "+cap)  # Control para capitulos con "0" delante
                if url.find("hdfull") >= 0:
                    url='http://hdfull.tv/serie/game-of-thrones/temporada-'+params.get("temp")+'/episodio-'+cap
                    options_hdfull=[];urls_hdfull=[];params['extra']="serie"
                    options_hdfull,urls_hdfull=hdfull_series_library(params)
                    linker_options = plugintools.selector(options_hdfull, title)
                    if linker_options > -1:
                        url=urls_hdfull[linker_options];video=True
                elif url.find("seriesblanco") >= 0:
                    #SERIE: http://seriesblanco.com/serie/230/game-of-thrones.html
                    #CAP: http://seriesblanco.com/serie/230/temporada-3/capitulo-01/ver.html
                    id_serie=plugintools.find_single_match(url, 'serie/([^//]+)');plugintools.log("id_serie= "+id_serie);suffix=url.split(id_serie)[1]
                    url='http://seriesblanco.com/serie/'+id_serie+'/temporada-'+params.get("temp")+'/capitulo-'+cap+'/ver.html';plugintools.log("url= "+url);params['url']=url
                    options_serieblanco=[];urls_serieblanco=[];params['extra']="serie"
                    options_serieblanco,urls_serieblanco=seriesblanco_library(params)
                    linker_options = plugintools.selector(options_serieblanco, title+' [COLOR white][I]['+cap+'x'+params.get("temp")+'][/COLOR][COLOR lightyellow] [SeriesBlanco][/I][/COLOR]')
                    if linker_options > -1:
                        params['url']=urls_serieblanco[linker_options];url=seriesblanco2_library(params);video=True                                        
                elif url.find("seriesyonkis") >= 0:
                    #http://www.seriesyonkis.com/capitulo/the-walking-dead-yonkis1/capitulo-6/256335 (pide ID de capítulo)
                    #http://www.seriesyonkis.com/capitulo/the-walking-dead-yonkis1/capitulo-6/224931
                    options_seriesyonkis=[];urls_seriesyonkis=[];params['extra']="serie"
                    options_seriesyonkis,urls_seriesyonkis=seriesyonkis_library(params)
                    linker_options = plugintools.selector(options_seriesyonkis, title)
                    if linker_options > -1:
                        url=urls_seriesyonkis[linker_options];video=True                    
                elif url.find("danko") >= 0:
                    options_dankopelis=[];urls_dankopelis=[];params['extra']="serie"
                    options_dankopelis,urls_dankopelis=dankopelis_library(params)
                    linker_options = plugintools.selector(options_dankopelis, title)                
                    if linker_options > -1:
                        url=urls_dankopelis[linker_options];video=True
                elif url.find("pordede") >= 0:
                    options_pordede=[];urls_pordede=[];params["extra"]=url;params_ajax=""
                    #options_pordede,urls_pordede,params_ajax=pordede_library(params)
                    options_pordede,urls_pordede=pordede_getlink(params)
                    linker_options = plugintools.selector(options_pordede, title)
                    if linker_options > -1:
                        url=urls_pordede[linker_options];video=True             
                elif url.find("torrentz") >= 0:
                    options_tz=[];urls_tz=[]  # Primera opción: [BUM+]
                    options_tz,urls_tz=bum_from_library0(params)  # De la lista de resultados de Torrentz, escogemos los tres con mayor número de semillas
                    bum_options = plugintools.selector(options_tz, title)
                    if bum_options > -1:
                        url=urls_tz[bum_options];params['url']=url;params['title']=options_tz[bum_options]
                        options_tz.append("[COLOR orange][I]Atrás... [/I][/COLOR]")
                        options_tz,urls_tz=bum_from_library1(params)  # Del enlace seleccionado, mostramos en un segundo selector los servidores disponibles
                        option_tz = plugintools.selector(options_tz, title)
                        try:
                            if option_tz > -1:
                                url_item=urls_tz[option_tz]
                                if url_item.find("bitsnoop") >= 0:
                                    r=requests.get(url_item);data=r.content;url = 'magnet'+plugintools.find_single_match(data, '<a href="magnet([^"]+)').strip()                  
                                elif url_item.find("isohunt") >= 0:
                                    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31", "Referer": "https://isohunt.to/"}
                                    r=requests.get(url_item, headers=headers);data=r.content;url = 'magnet'+plugintools.find_single_match(data, '<a href="magnet([^"]+)').strip()
                                elif url_item.find("torrentdownloads") >= 0:
                                    s=requests.Session();s.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0', 'Referer': "https://www.torrentdownloads.me/"}
                                    b=s.get(url_item, allow_redirects=False);cookie='';resp=b.text;heads=b.headers;cook=b.cookies;print cook
                                    for cookies in cook:
                                        cookie+=cookies.name+'='+cookies.value+'; ';s.headers.update({'Cookie':cookie});print cookie
                                        if cookie:
                                            data=resp.encode('utf-8','ignore');bloque_url=plugintools.find_single_match(data, '<span>Magnet:(.*?)</a></p></div>')
                                            url=plugintools.find_single_match(bloque_url, 'href="([^"]+)').strip()
                                elif url_item.find("torrentproject") >= 0 or url_item.find("isohunt") >= 0:
                                    r=requests.get(url_item);data=r.content;url = 'magnet:'+plugintools.find_single_match(data, "magnet:([^']+)").replace("amp;", "").strip()                    
                                elif url_item.find("torlock") >= 0 or url_item.find("torrentreactor") >= 0 or url_item.find("kat.cr") >= 0:  # Parseo común a estas webs: TorrentReactor, Kickass y Torlock
                                    request_headers=[];headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31", "Referer": plugintools.get_setting("kurl")}
                                    r=requests.get(url_item.replace("https", "http"), headers=headers);data=r.content;url = 'magnet:'+plugintools.find_single_match(data, 'magnet:([^"]+)').strip()
                                elif url_item.find("yourbittorrent") >= 0:
                                    request_headers=[];headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31", "Referer": plugintools.get_setting("kurl")}
                                    r=requests.get(url_item, headers=headers);data=r.content;url = plugintools.get_setting("yburl").replace("https", "http")+plugintools.find_single_match(data, 'href=/(.*?).torrent')+'.torrent'
                                    plugintools.log("url= "+url)
                                elif url_item.find("torrenthound") >= 0:
                                    request_headers=[];headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31", "Referer": 'http://www.torrenthound.com/'}
                                    r=requests.get(url_item.replace("https", "http"), headers=headers);data=r.content;bloque=plugintools.find_single_match(data, '<ul id="tmenu">(.*?)<span class="icon fils"');plugintools.log("bloque= "+bloque)
                                    hash=plugintools.find_single_match(bloque, 'hash/([^//]+)');url='http://www.torrenthound.com/torrent/'+hash                               
                                addon_magnet = plugintools.get_setting("addon_magnet")  # Función launch_magnet del módulo media_analyzer
                                if addon_magnet == "0":  # Stream (por defecto)
                                    url = 'plugin://plugin.video.stream/play/'+url_item
                                elif addon_magnet == "1":  # Pulsar
                                    url = 'plugin://plugin.video.pulsar/play?uri=' + url
                                elif addon_magnet == "2":  # KMediaTorrent
                                    url = 'plugin://plugin.video.kmediatorrent/play/'+url
                                elif addon_magnet == "3":  # XBMCtorrent
                                    url = 'plugin://plugin.video.xbmctorrent/play/'+url                                    
                                elif addon_magnet == "4":  # Quasar
                                    url = 'plugin://plugin.video.quasar/play?uri=' + url                                    
                                plugintools.log("URL Magnet= "+url);item = xbmcgui.ListItem(path=url);xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item);video=True
                        except KeyboardInterrupt: pass;
                        except IndexError: raise; 
                    
            else: sys.exit()

    except KeyboardInterrupt: pass;
    except IndexError: raise;

    params['url']=url;plugintools.log("URL= "+url)
    if url.find("allmyvideos") >=0: allmyvideos(params)
    elif url.find("vidspot") >= 0: vidspot(params)
    elif url.find("played") >= 0: playedto(params)
    elif url.find("streamin.to") >= 0: streaminto(params)
    elif url.find("streamcloud") >= 0: streamcloud(params)
    elif url.find("nowvideo") >= 0: nowvideo(params)
    elif url.find("veehd") >= 0: veehd(params)
    elif url.find("vk") >= 0: vk(params)
    elif url.find("lidplay") >= 0: vk(params)
    elif url.find("tumi") >= 0: tumi(params)
    elif url.find("novamov") >= 0: novamov(params)
    elif url.find("moevideos") >= 0: moevideos(params)
    elif url.find("gamovideo") >= 0: gamovideo(params)
    elif url.find("movshare") >= 0: movshare(params)
    elif url.find("powvideo") >= 0: powvideo(params)
    elif url.find("mail.ru") >= 0: mailru(params)
    elif url.find("mediafire") >= 0: mediafire(params)
    elif url.find("netu") >= 0: netu(params)
    elif url.find("movreel") >= 0: movreel(params)
    elif url.find("videobam") >= 0: videobam(params)
    elif url.find("vimeo/videos") >= 0: vimeo(params)
    elif url.find("vimeo/channels") >= 0: vimeo_pl(params)
    elif url.find("veetle") >= 0: veetle(params)
    elif url.find("videoweed") >= 0: videoweed(params)
    elif url.find("streamable") >= 0: streamable(params)
    elif url.find("rocvideo") >= 0: rocvideo(params)
    elif url.find("realvid") >= 0: realvid(params)
    elif url.find("videomega") >= 0: videomega(params)
    elif url.find("video.tt") >= 0: videott(params)
    elif url.find("flashx") >= 0: flashx(params)
    elif url.find("waaw") >= 0: waaw(params)
    elif url.find("openload") >= 0: openload(params)
    elif url.find("turbovideos") >= 0: turbovideos(params)
    elif url.find("ok.ru") >= 0: okru(params)
    elif url.find("vidto") >= 0: vidtome(params)
    elif url.find("playwire") >= 0: playwire(params)
    elif url.find("vimple") >= 0: vimple(params)
    elif url.find("vidgg") >= 0: vidggto(params)
    elif url.find("uptostream") >= 0: uptostream(params)
    elif url.find("youwatch") >= 0: youwatch(params)
    elif url.find("idowatch") >= 0: idowatch(params)
    elif url.find("cloudtime") >= 0: cloudtime(params)
    elif url.find("allvid") >= 0: allvid(params)
    elif url.find("vodlocker") >= 0: vodlocker(params)
    elif url.find("vidzi") >= 0: vidzitv(params)
    elif url.find("streame") >= 0: streamenet(params)
    elif url.find("myvideoz") >= 0: myvideoz(params)
    elif url.find("streamplay") >= 0: streamplay(params)
    elif url.find("watchonline") >= 0: watchonline(params)
    elif url.find("rutube") >= 0: rutube(params)
    elif url.find("dailymotion") >= 0: dailymotion(params)
    elif url.find("auroravid") >= 0: auroravid(params)
    elif url.find("wholecloud") >= 0: wholecloud(params)
    elif url.find("bitvid") >= 0: bitvid(params)
    elif url.find("spruto") >= 0: spruto(params)
    elif url.find("stormo") >= 0: stormo(params)
    elif url.find("myvi.ru") >= 0: myviru(params)
    elif url.find("youtube") >= 0: youtube(params)
    elif url.find("filmon") >= 0: filmon(params)
    elif url.find("thevideo.me") >= 0: thevideome(params)
    elif url.find("videowood") >= 0: videowood(params)
    elif url.find("neodrive") >= 0: neodrive(params)
    elif url.find("thevideobee") >= 0: thevideobee(params)
    elif url.find("fileshow") >= 0: fileshow(params)
    elif url.find("vid.ag") >= 0: vid(params)
    elif url.find("vidxtreme") >= 0: vidxtreme(params)
    elif url.find("vidup") >= 0: vidup(params)
    elif url.find("watchvideo") >= 0: watchvideo(params)
    elif url.find("speedvid") >= 0: speedvid(params)
    elif url.find("chefti.info") >= 0: exashare(params)
    elif url.find("vodbeast") >= 0: vodbeast(params)
    elif url.find("nosvideo") >= 0: nosvideo(params)
    elif url.find("noslocker") >= 0: noslocker(params)
    elif url.find("exashare") >= 0: exashare(params)
    elif url.find("thevideobee") >= 0: thevideobee(params)
    elif url.find("letwatch") >= 0: letwatch(params)
    elif url.find("smartvid") >= 0: smartvid(params)
    elif url.find("greevid") >= 0: greevid(params)    
    elif url.find("letwatch") >= 0: letwatch(params)
    elif url.find("yourupload") >= 0: yourupload(params)
    elif url.find("zalaa") >= 0: zalaa(params)
    elif url.find("uploadc") >= 0: uploadc(params)
    elif url.find("mp4upload") >= 0: mp4upload(params)
    elif url.find("rapidvideo") >= 0: rapidvideo(params)
    elif url.find("yourvideohost") >= 0: yourvideohost(params)
    elif url.find("watchers") >= 0: watchers(params)
    elif url.find("vidtodo") >= 0: vidtodo(params)    
    else: xbmc.executebuiltin('PlayerControl(Stop)')


   
def seriesblanco_library(params):
    plugintools.log("[%s %s] Linker SeriesBlanco %s" % (addonName, addonVersion, repr(params)))
    
    url = params.get("url");referer = "http://seriesblanco.com";headers = {"User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12", "Referer": referer}
    r = requests.get(url,headers=headers);data = r.content;option_list=[];url_list=[]

    match_listacapis = plugintools.find_single_match(data,"<h2>Visionados Online</h2>(.*?)<h2>Descarga</h2>")  #No hay petición Ajax
    if match_listacapis =="":  #Si hay petición Ajax
        ajax = plugintools.find_single_match(data,"function LoadGrid(.*?)success:")  # Buscando datos del envio post a la peticion ajax
        post = plugintools.find_single_match(ajax,'data : "(action=load&serie=.*?=&temp=.*?=&cap=.*?=)"')
        headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0', "Referer": params.get("url")};url = "http://seriesblanco.com/ajax.php";r = requests.post(url,data=post,headers=headers);data = r.content  # Petición ajax
    match_listacapis = plugintools.find_single_match(data,'<h2>Visionados Online</h2>(.*?)</table>')
    match_capi = plugintools.find_multiple_matches(match_listacapis,'<td><div class="grid_content sno">(.*?)<br>')
    for entry in match_capi:
        plugintools.log("entry= "+entry)
        url_capi = referer+plugintools.find_single_match(entry,'<a href="([^"]+)"');plugintools.log("URL capitulo= "+url_capi)
        lang = plugintools.find_single_match(entry,'<img src="http://seriesblanco.tv/banderas/([^"]+)"')
        if lang =="": 
            lang = plugintools.find_single_match(entry,'<img src="http://seriesblanco.com/banderas/([^"]+)"')
        if lang.find("es.png") >= 0: lang = "ESP"
        elif lang.find("la.png") >= 0: lang = "LAT"
        elif lang.find("vos.png") >= 0: lang = "V.O.S."
        elif lang.find("vo.png") >= 0: lang = "V.O."            
        url_server = plugintools.find_single_match(entry,"<img src='/servidores/([^']+)")
        url_server = url_server.replace(".png", "").replace(".jpg", "")
        quality = plugintools.find_single_match(entry, 'target="_blank">.*?<div class="grid_content sno">.*?<div class="grid_content sno"><span>(.*?)</span>')
        server = video_analyzer(url_server)
        if quality!= "": titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+lang.strip()+'] [/COLOR][COLOR lightblue]['+quality+'][/I][/COLOR]'
        else: titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+lang.strip()+'] [/COLOR][/I]'
        option_list.append(titlefull);plugintools.log("titlefull= "+titlefull)
        url_list.append(url_capi);plugintools.log("url capi= "+url_capi)

    return option_list, url_list

def seriesblanco2_library(params):
    url = params.get("url");plugintools.log("URL refeer= "+url);headers={'Referer': url};r=requests.get(url, headers=headers);data=r.content;plugintools.log("data= "+data)
    # onclick='window.open("http://allmyvideos.net/lh18cer7ut8r")
    url_final = plugintools.find_single_match(data, "onclick='window.open(.*?);'/>").replace('("', "").replace('")', "");return url_final
