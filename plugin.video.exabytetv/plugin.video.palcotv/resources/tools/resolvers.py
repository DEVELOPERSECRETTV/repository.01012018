# -*- coding: utf-8 -*-
#------------------------------------------------------------
# PalcoTV - Kodi Add-on by Juarrox (juarrox@gmail.com)
# Conectores multimedia para PalcoTV
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a las librerías de pelisalacarta de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re
import string
import shutil
import zipfile
import time
import urlparse
import random
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import scrapertools, plugintools, unpackerjs, requests, jsunpack, base64, json, wiz#, png
import cookielib

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

from __main__ import *
'''para UNPACK'''
from wiz import *

art = addonPath + "/art/"
temp = xbmc.translatePath(os.path.join('special://home/userdata/playlists/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/userdata/playlists', ''))

def urlr(url):
    plugintools.log('[%s %s] Probando URLR con... %s' % (addonName, addonVersion, url))

    import urlresolver
    host = urlresolver.HostedMediaFile(url)
    print 'host',host
    if host:
        resolver = urlresolver.resolve(url)
        print 'URLR',resolver
        return resolver
    else:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "URL Resolver: Servidor no soportado", 3 , art+'icon.png'))

def novamov(params): auroravid(params)
def movshare(params): wholecloud(params)
def videoweed(params): bitvid(params)
def waaw(params): netu(params)
def noslocker(params): nosvideo(params)
def cloudzilla(params): neodrive(params)
def uptobox(params): uptostream(params)
   

def allmyvideos(params):
    plugintools.log('[%s %s] Allmyvideos %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not 'embed' in page_url:
        #http://amvtv.net/embed-3hn5sihfhp5o-728x400.html
        page_url = page_url.replace("https://allmyvideos.net/", "http://amvtv.net/embed-")
        page_url = page_url.replace("http://allmyvideos.net/", "http://amvtv.net/embed-")+'-728x400.html'   
    r = requests.get(page_url)
    data = r.content

    ######################### Thanks to code Pelisalacarta ############################
    ####################### Adaptation PalcoTV by Aquilesserr #########################

    if "Access denied" in data:
        # url = "http://www.anonymousbrowser.xyz/hide.php"
        # post = "go=%s" % page_url
        url = "http://www.videoproxy.co/hide.php"
        post = "go=%s" % page_url
        
        r = requests.get(url,data=post,allow_redirects=False)#,headers=headers)
        data = r.content
        print data
        location = r.headers['location']
        #url=http://www.videoproxy.co/go/247005/nph-proxy.cgi/en/20/http//amvtv.net/embed-jwvvkc14b0xr-728x400.html
        page_url = page_url.replace('http://','')
        url = "http://www.videoproxy.co/" + location+page_url
        
        r = requests.get(url)
        data = r.content 
        # Extrae la URL
        media = plugintools.find_multiple_matches(data, '"file" : "([^"]+)",')
        for item in media:
            if item.endswith('mp4?v2'):
                #http://www.videoproxy.co/go/91523/nph-proxy.cgi/en/20/http//d6066.allmyvideos.net/d/4smooougyq5dh6lnatf4x2osp67jyomdwvaivwqtp3qfmryett6sf56t677cvdq/video.mp4?v2&direct=false
                item = item.replace('http://','')
                media_url = "http://www.videoproxy.co/" + location+item+'&direct=false'
                print '<'*10+'- Thanks to code Pelisalacarta -'+'>'*10
                print '$'*80+'- By PalcoTV Team -'+'$'*80,media_url,'$'*179          
    else:
        media = plugintools.find_multiple_matches(data, '"file" : "([^"]+)",')
        for item in media:
            if item.endswith('mp4?v2'):
                media_url = item+'&direct=false'
                print '<'*10+'- Thanks to code Pelisalacarta -'+'>'*10
                print '$'*65+'- By PalcoTV Team -'+'$'*65,media_url,'$'*149

    ######################### Thanks to code Pelisalacarta ############################
    ####################### Adaptation PalcoTV by Aquilesserr #########################
                
    plugintools.play_resolved_url(media_url)
    
def streamcloud(params):
    plugintools.log('[%s %s]Streamcloud %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    try:
        request_headers=[]
        request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
        body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
        #plugintools.log("data= "+body)
        # Barra de progreso para la espera de 10 segundos
        progreso = xbmcgui.DialogProgress()
        progreso.create("PalcoTV", "Abriendo Streamcloud..." , url )
        i = 13000
        j = 0
        percent = 0
        while j <= 13000 :
            percent = ((j + ( 13000 / 10.0 )) / i)*100
            xbmc.sleep(i/10)  # 10% = 1,3 segundos
            j = j + ( 13000 / 10.0 )
            msg = "Espera unos segundos, por favor... "
            percent = int(round(percent))
            print percent
            progreso.update(percent, "" , msg, "")
        progreso.close()
        media_url = plugintools.find_single_match(body , 'file\: "([^"]+)"')
        if media_url == "":
            op = plugintools.find_single_match(body,'<input type="hidden" name="op" value="([^"]+)"')
            usr_login = ""
            id = plugintools.find_single_match(body,'<input type="hidden" name="id" value="([^"]+)"')
            fname = plugintools.find_single_match(body,'<input type="hidden" name="fname" value="([^"]+)"')
            referer = plugintools.find_single_match(body,'<input type="hidden" name="referer" value="([^"]*)"')
            hashstring = plugintools.find_single_match(body,'<input type="hidden" name="hash" value="([^"]*)"')
            imhuman = plugintools.find_single_match(body,'<input type="submit" name="imhuman".*?value="([^"]+)">').replace(" ","+")
            post = "op="+op+"&usr_login="+usr_login+"&id="+id+"&fname="+fname+"&referer="+referer+"&hash="+hashstring+"&imhuman="+imhuman
            request_headers.append(["Referer",url])
            body,response_headers = plugintools.read_body_and_headers(url, post=post, headers=request_headers)
            #plugintools.log("data= "+body)
            # Extrae la URL
            media_url = plugintools.find_single_match( body , 'file\: "([^"]+)"' )
            print '$'*43+'- By PalcoTV Team -'+'$'*43,media_url,'$'*105
            plugintools.play_resolved_url(media_url)
            if 'id="justanotice"' in body:
                #plugintools.log("[streamcloud.py] data="+body)
                plugintools.log("[streamcloud.py] Ha saltado el detector de adblock")
                return -1
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def playedto(params):
    plugintools.log('[%s %s] Played.to %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    page_url = page_url.split("/")
    url_fixed = "http://played.to/embed-" + page_url[3] +  "-640x360.html"
    plugintools.log("url_fixed= "+url_fixed)
    try:
        request_headers=[]
        request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
        body,response_headers = plugintools.read_body_and_headers(url_fixed, headers=request_headers)
        body = body.strip()
        if body == "<center>This video has been deleted. We apologize for the inconvenience.</center>":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Enlace borrado...", 3 , art+'icon.png'))
        elif body.find("Removed for copyright infringement") >= 0:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Removed for copyright infringement", 3 , art+'icon.png'))
        else:
            r = re.findall('file(.+?)\n', body)
            for entry in r:
                entry = entry.replace('",', "")
                entry = entry.replace('"', "")
                entry = entry.replace(': ', "")
                entry = entry.strip()
                plugintools.log("vamos= "+entry)
                if entry.endswith("flv"):
                    media_url = entry             
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)


def vidspot(params):
    plugintools.log('[%s %s] Vidspot %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    if not 'embed' in page_url:
        page_url = page_url.replace("http://vidspot.net/", "http://vidspot.net/embed-")+".html"   
    r = requests.get(page_url)
    data = r.content

    ######################### Thanks to code Pelisalacarta ############################
    ####################### Adaptation PalcoTV by Aquilesserr #########################
    
    if "Access denied" in data:
        '''
        # url = "http://www.anonymousbrowser.xyz/hide.php"
        # post = "go=%s" % page_url
        ref = 'http://anonymouse.org/anonwww.html'
        url = "http://anonymouse.org/cgi-bin/anon-redirect.cgi"
        post = "what="+page_url
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0","Referer": ref}
        r = requests.post(url,headers=headers,data=post,allow_redirects=False)
        data = r.content
        print r.headers
        location = r.headers['location']
        #print location

        r = requests.get(location,headers=headers)
        data = r.content
        print data
        media = plugintools.find_multiple_matches(data, '"file" : "([^"]+)",')

        '''
        url = "http://www.videoproxy.co/hide.php"
        post = "go=%s" % page_url
        
        r = requests.get(url,data=post,allow_redirects=False)
        data = r.content
        print r.headers
        location = r.headers['location']
        print location
        #url=http://www.videoproxy.co/go/247005/nph-proxy.cgi/en/20/http//amvtv.net/embed-jwvvkc14b0xr-728x400.html
        
        page_url = page_url.replace('http://','')
        url = "http://www.videoproxy.co/" + location+page_url
        r = requests.get(url)
        data = r.content 
        # Extrae la URL
        media = plugintools.find_multiple_matches(data, '"file" : "([^"]+)",')
        for item in media:
            if item.endswith('mp4?v2'):
                #http://www.videoproxy.co/go/91523/nph-proxy.cgi/en/20/http//d6066.allmyvideos.net/d/4smooougyq5dh6lnatf4x2osp67jyomdwvaivwqtp3qfmryett6sf56t677cvdq/video.mp4?v2&direct=false
                item = item.replace('http://','')
                media_url = "http://www.videoproxy.co/" + location+item+'&direct=false'
                print '<'*10+'- Thanks to code Pelisalacarta -'+'>'*10
                print '$'*80+'- By PalcoTV Team -'+'$'*80,media_url,'$'*179

    else:
        media = plugintools.find_multiple_matches(data, '"file" : "([^"]+)",')
        for item in media:
            if item.endswith('mp4?v2'):
                media_url = item+'&direct=false'
                print '<'*10+'- Thanks to code Pelisalacarta -'+'>'*10
                print '$'*65+'- By PalcoTV Team -'+'$'*65,media_url,'$'*149

    ######################### Thanks to code Pelisalacarta ############################
    ####################### Adaptation PalcoTV by Aquilesserr #########################
               
    plugintools.play_resolved_url(media_url)
				
def vk(params):
    plugintools.log('[%s %s] Vk %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        page_url = page_url.replace('http://lidplay.net/jwplayer/video_ext.php?','http://new.vk.com/video_ext.php?')
        page_url = page_url.replace('http://vkontakte.ru/video_ext.php?','http://new.vk.com/video_ext.php?')
        page_url = page_url.replace('http://f6.videosxd.org/v.php?v=','http://new.vk.com/video_ext.php?oid=')

        ######################## Public Video #########################
        try:
            id_vid = plugintools.find_single_match(page_url,'video(.*_.*)')
            url = 'http://vk.com/al_video.php?act=show_inline&al=1&video='+id_vid
            headers ={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"}
            r = requests.get(url)#,headers=headers)
            data = r.content
            recompile_url = plugintools.find_multiple_matches(data,'source src="(.*?)"')
            media_url = recompile_url[0]
        ###############################################################   
        ######################## Private Video ########################   
        except:
            extrac_params = page_url.split("=")
            #http://vk.com/video_ext.php?oid=295239104&id=171117835&hash=2425e0df405e816a&hd=2
            extrac_oid = plugintools.find_single_match(extrac_params[1],'(\w{9})')
            extrac_id = plugintools.find_single_match(extrac_params[2],'(\w{9})')
            extrac_hash = plugintools.find_single_match(extrac_params[3],'(\w{16})')
            url = 'http://api.vk.com/method/video.getEmbed?oid='+extrac_oid+'&video_id='+extrac_id+'&embed_hash='+extrac_hash
            r = requests.get(url)
            data = r.content
            data_js = json.loads(data)
            oid = data_js['error']['request_params'][2]['value']
            id = data_js['error']['request_params'][3]['value']
            hash = data_js['error']['request_params'][4]['value']
            url_js = 'http://vk.com/al_video.php?act=show_inline&al=1&video='+oid+'_'+id
            r = requests.get(url_js)#,headers=headers)
            data = r.content
            recompile_url = plugintools.find_multiple_matches(data,'source src="(.*?)"')
            media_url = recompile_url[0]
        ###############################################################
        print '$'*90+'- By PalcoTV Team -'+'$'*90,media_url,'$'*199
        plugintools.play_resolved_url(media_url)
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
def nowvideo(params):
    plugintools.log('[%s %s] Nowvideo %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            page_url = page_url.replace("http://www.nowvideo.sx/video/","http://embed.nowvideo.sx/embed/?v=")
        headers = {"Host": "embed.nowvideo.sx","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r=requests.get(page_url)#,headers=headers)
        data=r.content
        if '<source src=' in data:
            bloq_media = plugintools.find_multiple_matches(data,'<source src="(.*?)"')
            if bloq_media == "":
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "El Archivo no esta disponible", 3 , art+'icon.png'))       
            else:
                media_url = bloq_media[-1]
                print '<'*10+'- Reproduciendo Met.1 -'+'>'*10
                print '$'*45+'- By PalcoTV Team -'+'$'*45,media_url,'$'*109
                plugintools.play_resolved_url(media_url)
        else:
            page_url = page_url.replace("http://embed.nowvideo.sx/embed/?v=","http://www.nowvideo.sx/video/")
            r = requests.get(page_url)
            data = r.content
            stepkey = plugintools.find_single_match(data, 'name="stepkey" value="(.*?)"')
            submit = "submit"
            post = 'stepkey='+stepkey+'&submit='+submit
            headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12', "Referer": params.get("url")}
            body,response_headers = plugintools.read_body_and_headers(page_url,headers=headers,post=post,follow_redirects=True)
            data = body
            if "no longer exists" in data:
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "El archivo no está en disponible", 3 , art+'icon.png'))        
            else:
                domain = plugintools.find_single_match(data, 'flashvars.domain="([^"]+)"')
                video_id = plugintools.find_single_match(data, 'flashvars.file="([^"]+)"')
                filekey = plugintools.find_single_match(data, 'flashvars.filekey=([^;]+);')
                token_txt = 'var '+filekey
                token = plugintools.find_single_match(data, filekey+'=\"([^"]+)"')
                token = token.replace(".","%2E").replace("-","%2D")
                if video_id == "":
                    xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "El archivo no está en disponible", 3 , art+'icon.png'))
                else:
                    #http://www.nowvideo.sx/api/player.api.php?user=undefined&pass=undefined&cid3=undefined&numOfErrors=0&cid2=undefined&key=83%2E47%2E1%2E12%2D8d68210314d70fb6506817762b0d495e&file=b5c8c44fc706f&cid=1
                    url = 'http://www.nowvideo.sx/api/player.api.php?user=undefined&pass=undefined&cid3=undefined&numOfErrors=0&cid2=undefined&key='+token+'&file='+video_id+'&cid=1'
                    r = requests.get(url)
                    data = r.content
                    referer = 'http://www.nowvideo.sx/'
                    request_headers=[]
                    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
                    request_headers.append(["Referer",referer])
                    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
                    body = body.replace("url=", "")
                    body = body.split("&")
                    if len(body) >= 0:
                        media_url = body[0]
                        print '<'*10+'- Reproduciendo Met.2 -'+'>'*10
                        print '$'*45+'- By PalcoTV Team -'+'$'*45,media_url,'$'*109
                        plugintools.play_resolved_url(media_url)           
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
         
def veehd(params):
    plugintools.log('[%s %s] VeeHD %s' % (addonName, addonVersion, repr(params)))
    
    uname = plugintools.get_setting("veehd_user")
    pword = plugintools.get_setting("veehd_pword")
    if uname == '' or pword == '':
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Debes configurar el identificador para Veehd.com", 3 , art+'icon.png'))
        return
    url = params.get("url")
    url_login = 'http://veehd.com/login'
    try:
        request_headers=[]
        request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
        request_headers.append(["Referer",url])
    
        post = {'ref': url, 'uname': uname, 'pword': pword, 'submit': 'Login', 'terms': 'on'}
        post = urllib.urlencode(post)
    
        body,response_headers = plugintools.read_body_and_headers(url_login, post=post, headers=request_headers, follow_redirects=True)
        vpi = plugintools.find_single_match(body, '"/(vpi.+?h=.+?)"')
        if not vpi:
            if 'type="submit" value="Login" name="submit"' in body:
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Error al identificarse en Veehd.com", 3 , art+'icon.png'))
            else:
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Error buscando el video en Veehd.com", 3 , art+'icon.png'))            
            return
        req = urllib2.Request('http://veehd.com/'+vpi)
        for header in request_headers:
            req.add_header(header[0], header[1]) # User-Agent
        response = urllib2.urlopen(req)
        body = response.read()
        response.close()
        va = plugintools.find_single_match(body, '"/(va/.+?)"')
        if va:
            req = urllib2.Request('http://veehd.com/'+va)
            for header in request_headers:
                req.add_header(header[0], header[1]) # User-Agent
            urllib2.urlopen(req)
        req = urllib2.Request('http://veehd.com/'+vpi)
        for header in request_headers:
            req.add_header(header[0], header[1]) # User-Agent
        response = urllib2.urlopen(req)
        body = response.read()
        response.close()

        video_url = False
        if 'application/x-shockwave-flash' in body:
            video_url = urllib.unquote(plugintools.find_single_match(body, '"url":"(.+?)"'))
        elif 'video/divx' in body:
            video_url = urllib.unquote(plugintools.find_single_match(body, 'type="video/divx"\s+src="(.+?)"'))
        if not video_url:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Error abriendo el video en Veehd.com", 3 , art+'icon.png'))
            return
        media_url = video_url
        print '$'*33+'- By PalcoTV Team -'+'$'*33,media_url,'$'*85
        plugintools.play_resolved_url(media_url) 
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def streaminto(params):
    plugintools.log('[%s %s] streaminto %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://streamin.to/","http://streamin.to/embed-") +'.html'
    try:
        headers = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'}
        r = requests.get(page_url, headers=headers)
        data = r.content
        if data == "File was deleted":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))        
        else:
            media_url = plugintools.find_single_match(data,'file: "([^"]+)"')
            print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95
            plugintools.play_resolved_url(media_url)     
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def powvideo(params):
    plugintools.log('[%s %s] Powvideo %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    #Evitando Error si la url entra com embed-
    if 'embed' in page_url:
        id_vid = plugintools.find_single_match(page_url,'http://powvideo.net/embed-(.*?)-')
        page_url = 'http://powvideo.net/'+id_vid  
    try:
        if not "iframe" in page_url:
            page_iframe = page_url.replace("http://powvideo.net/","http://powvideo.net/iframe-") + "-640x360.html"
        ref = page_iframe.replace('iframe','embed')
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0','Referer': ref}
        r = requests.get(page_iframe,headers=headers)
        data = r.text
        if not 'File was deleted' in data:
            data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
            data = wiz.unpack(data)
        else:
            page_url = params.get("url")
            if not "preview" in page_url:
                page_preview = page_url.replace("http://powvideo.net/","http://powvideo.net/preview-") + "-640x360.html"
            r = requests.get(page_preview)
            data = r.content
            ref = page_preview
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0','Referer': ref}
            page_iframe = page_preview.replace('preview','iframe')
            r = requests.get(page_iframe,headers=headers)
            data = r.text
            data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
            data = wiz.unpack(data)
        sources = plugintools.find_multiple_matches(data,"image:image,tracks:tracks,src:'(.*?)'")
        if sources !="":
            if 'mp4' in sources[-1]: media_url = sources[-1] #mp4
            elif 'm3u8' in sources[-1]: media_url = sources[-1]+"|User-Agent="+headers['User-Agent'] #m3u8
            #Ignoramos el rtmp
            print '$'*40+'- By PalcoTV Team -'+'$'*40,media_url,'$'*99
            plugintools.play_resolved_url(media_url)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "El Archivo no esta disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url  

def mailru(params):
    plugintools.log('[%s %s] Mail.ru %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        r = requests.get(page_url)
        data = r.content

        if not 'videoapi' in page_url:
            #page_url = page_url.replace('/my.mail.ru/video/', '/api.video.mail.ru/videos/embed')
            new_url = plugintools.find_single_match(data,'metaUrl":.*?"([^"]+)"').strip()
            new_url = new_url+"?ver=0.2.114"     
        else:
            new_url = plugintools.find_single_match(data,'metadataUrl":.*?"([^"]+)"').strip()
            new_url = 'http:'+new_url+"?ver=0.2.129"

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
        "Referer": "http://my1.imgsmail.ru/r/video2/uvpv3.swf?75"}
        #Cookie: video_key=16d3637ca27c94312812741024af82f6015a8f80 |Cookie=video_key="
        r = requests.get(new_url,headers=headers)
        data_js = r.text
        cookie_vidkey = r.cookies['video_key']
        js = json.loads(data_js)
        media = js['videos'][0]['url'].replace('%3A',':').replace('%2F','/').replace('%3D','=').replace('%3F','?').replace('%26','&')
        if media == "":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
        else:
            media_url = 'http:'+media + "|Cookie=video_key=" + cookie_vidkey
            print '$'*115+'- By PalcoTV Team -'+'$'*115,media_url,'$'*249
            plugintools.play_resolved_url(media_url)
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url  
    
def mediafire(params):
    plugintools.log('[%s %s] Mediafire %s' % (addonName, addonVersion, repr(params)))

    # Solicitud de página web
    url = params.get("url")
    data = plugintools.read(url)

    # Espera un segundo y vuelve a cargar
    plugintools.log("[PalcoTV] Espere un segundo...")
    import time
    time.sleep(1)
    data = plugintools.read(url)
    plugintools.log("data= "+data)
    pattern = 'kNO \= "([^"]+)"'
    matches = re.compile(pattern,re.DOTALL).findall(data)
    for entry in matches:
        plugintools.log("entry= "+entry)
    # Tipo 1 - http://www.mediafire.com/download.php?4ddm5ddriajn2yo
    pattern = 'mediafire.com/download.php\?([a-z0-9]+)'
    matches = re.compile(pattern,re.DOTALL).findall(data)    
    for entry in matches:
        if entry != "":
            url = 'http://www.mediafire.com/?'+entry
            plugintools.log("URL Tipo 1 = "+url)
            
'''
    # Tipo 2 - http://www.mediafire.com/?4ckgjozbfid
    pattern  = 'http://www.mediafire.com/\?([a-z0-9]+)'
    matches = re.compile(pattern,re.DOTALL).findall(data)
    for entry in matches:
        if entry != "":
            url = 'http://www.mediafire.com/?'+entry
            plugintools.log("URL Tipo 2 = "+url)
        
    # Tipo 3 - http://www.mediafire.com/file/c0ama0jzxk6pbjl
    pattern  = 'http://www.mediafire.com/file/([a-z0-9]+)'
    plugintools.log("[mediafire.py] find_videos #"+pattern+"#")
    matches = re.compile(pattern,re.DOTALL).findall(data)
    for entry in matches:
        if entry != "":
            url = 'http://www.mediafire.com/?'+entry
            plugintools.log("URL Tipo 3 = "+url)

'''
            
def auroravid(params):
    plugintools.log('[%s %s] Novamov (Antes: Novamov) %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        if 'novamov' in page_url:
            page_url = page_url.replace('http://www.novamov.com','http://www.auroravid.to')
        #headers = {"Host": "www.auroravid.to","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"}
        r=requests.get(page_url)#,headers=headers)
        data=r.content
        videoid = plugintools.find_single_match(page_url,"http://www.auroravid.to/video/([a-z0-9]+)")
        stepkey = plugintools.find_single_match(data,'name="stepkey" value="([^"]+)"')
        ref = page_url
        post = "stepkey="+stepkey+"&submit=submit"   
        headers = {"Host": "www.auroravid.to","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0","Referer":page_url}
        body,response_headers = plugintools.read_body_and_headers(page_url, post=post)    
        #http://www.auroravid.to/api/player.api.php?file=d0f559fe7f8ec&key=87.219.239.45-bb8140bed80d5abe821ce4f61781c1f7&cid2=undefined&numOfErrors=0&cid3=auroravid.to&user=undefined&pass=undefined&cid=1
        stream_url = plugintools.find_single_match(body,'flashvars.filekey="(.*?)"')
        cid1 = plugintools.find_single_match(body,'flashvars.cid="(.*?)"')
        headers = {"Host": "www.auroravid.to","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
        "Referer":"http://www.auroravid.to/player/cloudplayer.swf"}    
        #url = "http://www.auroravid.to/api/player.api.php?file="+videoid+"&key="+stream_url+"&cid2=undefined&numOfErrors=0&cid3=auroravid.to&user=undefined&pass=undefined&cid="+str(cid1)
        url = "http://www.auroravid.to/api/player.api.php?cid3=auroravid.to&cid2=undefined&file="+videoid+"&key="+stream_url+"&numOfErrors=0&user=undefined&pass=undefined&cid="+str(cid1)      
        #http://www.auroravid.to/api/player.api.php?cid3=auroravid.to&cid2=undefined&file=d0f559fe7f8ec&key=212.106.224.246-f5738b980374d938342b5757841c116d&numOfErrors=0&user=undefined&pass=undefined&cid=1
        r=requests.get(url,headers=headers)
        data=r.content
        if data != "":
            media_url = plugintools.find_single_match(data,'url=(.*?)&title')
            print '$'*45+'- By PalcoTV Team -'+'$'*45,media_url,'$'*109
            plugintools.play_resolved_url(media_url)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "El Archivo no esta disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url    
      
def gamovideo(params):
    plugintools.log('[%s %s] Gamovideo %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        r = requests.get(page_url)
        data = r.content
        if "File was deleted" in data or "File Not Found" in data:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "El Archivo no esta disponible", 3 , art+'icon.png'))
        else:
            bloq_vid = plugintools.find_single_match(data,"playlist: \[\{(.*?)</script>")
            if bloq_vid !="":
                #http://94.23.216.171:8777/6qx23xz5fipskjwff77scahq3u5vio5iiqlk2pjctvpbjlons4ld7aa332tq/v.flv
                host = plugintools.find_single_match(bloq_vid,'image: "(http://.*?/)')
                bloq_file = plugintools.find_multiple_matches(bloq_vid,'file: "([^"]+)"')
                filefull = bloq_file[-1].split('='); file_id = filefull[-1]
                media_url = host + file_id + '/v.flv'
                print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95
                plugintools.play_resolved_url(media_url)  
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
       
def wholecloud(params):
    plugintools.log('[%s %s] Wholecloud (Antes: Movshare) %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        ############## Codigo Nuevo Wholecloud ############## 
        if ("https://www.wholecloud.net/" in page_url) or ("http://www.wholecloud.net/" in page_url):
            page_url = page_url.replace("https://www.wholecloud.net/","http://www.wholecloud.net/")
            if not "embed" in page_url:
                    page_url = page_url.replace("http://www.wholecloud.net/video/","http://www.wholecloud.net/embed/?v=")
            headers = {"Host": "www.wholecloud.net","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
            r=requests.get(page_url)#,headers=headers)
            data=r.content
            bloq_media = plugintools.find_multiple_matches(data,'<source src="(.*?)"')
            if bloq_media == "":
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "El Archivo no esta disponible", 3 , art+'icon.png'))       
            else:
                media_url = bloq_media[-1]
                print '<'*10+'- Reproduciendo Met.Wholecloud -'+'>'*10
                print '$'*45+'- By PalcoTV Team -'+'$'*45,media_url,'$'*109
                plugintools.play_resolved_url(media_url)
    
        ############## Codigo Anterior Movshare ############## 
        elif "http://www.movshare.net/" in page_url:
            try:
                r=requests.get(page_url,allow_redirects=False)#,headers=headers)
                data=r.headers
                location_url = r.headers['Location']
                headers = {"Host": "www.wholecloud.net","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"}
                r=requests.get(location_url,headers=headers)
                data=r.content
                videoid = plugintools.find_single_match(page_url,"http://www.movshare.net/video/([a-z0-9]+)")
                stepkey = plugintools.find_single_match(data,'name="stepkey" value="([^"]+)"')
                post = "stepkey="+stepkey+"&submit=submit"
                headers = {"Host": "www.wholecloud.net","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Referer":page_url}
                page_wholecloud = "http://www.wholecloud.net/video/"+videoid
                body,response_headers = plugintools.read_body_and_headers(page_wholecloud, post=post)
                stream_url = plugintools.find_single_match(body,'flashvars.filekey="(.*?)"')
                cid1 = plugintools.find_single_match(body,'flashvars.cid="(.*?)"')
                headers = {"Host": "www.wholecloud.net","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
                "Referer":"https://www.wholecloud.net/player/cloudplayer.swf"}
                #http://www.wholecloud.net/api/player.api.php?file=7yg5spgst3nsq&cid=1&cid3=undefined&numOfErrors=0&user=undefined&key=95.22.211.72-7176b1a01db70b1bc18f0d87413ed37e&pass=undefined&cid2=undefined 
                url = "http://www.wholecloud.net/api/player.api.php?file="+videoid+"&cid=1&cid3=undefined&numOfErrors=0&user=undefined&key="+stream_url+"&pass=undefined&cid2=undefined"  
                r=requests.get(url,headers=headers)
                data=r.content
                #http://s81.zerocdn.to/dl/9abddcb58df9a601c696b675eb1fe28f/57b482de/ffa48c690b7c9993898ea1a4dee6134884.flv?client=FLASH
                media_url = plugintools.find_single_match(data,'url=(.*?)&title')+'?client=FLASH'
                plugintools.play_resolved_url(media_url)
                print '<'*10+'- Reproduciendo Met.Movshare -'+'>'*10
                print '$'*50+'- By PalcoTV Team -'+'$'*50,media_url,'$'*119
            except:
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "El Archivo no esta disponible", 3 , art+'icon.png'))     
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url    
        
def videobam(params):
    plugintools.log('[%s %s] Videobam %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        data = scrapertools.cache_page(page_url)
        videourl = ""
        match = ""
        if "Video is processing" in data:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible temporalmente!", 3 , art+'icon.png'))
        else:
            patronHD = " high: '([^']+)'"
            matches = re.compile(patronHD,re.DOTALL).findall(data)
            for match in matches:
                media_url = match
                plugintools.log("Videobam HQ :"+match)

            if videourl == "":
                patronSD= " low: '([^']+)'"
                matches = re.compile(patronSD,re.DOTALL).findall(data)
                for match in matches:
                    media_url = match
                    plugintools.log("Videobam LQ :"+match)

                if match == "":
                    if len(matches)==0:
                        # "scaling":"fit","url":"http:\/\/f10.videobam.com\/storage\/11\/videos\/a\/aa\/AaUsV\/encoded.mp4
                        patron = '[\W]scaling[\W]:[\W]fit[\W],[\W]url"\:"([^"]+)"'
                        matches = re.compile(patron,re.DOTALL).findall(data)
                        for match in matches:
                            videourl = match.replace('\/','/')
                            videourl = urllib.unquote(videourl)
                            plugintools.log("Videobam scaling: "+videourl)
                            if videourl != "":
                                media_url = videourl              
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)

def vimeo(params):
    plugintools.log('[%s %s] Vimeo %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    #https://vimeo.com/101182831
    #https://player.vimeo.com/video/101182831
    
    try:
        if not "player" in page_url:
            page_url = page_url.replace("https://vimeo.com/","https://player.vimeo.com/video/")
        headers = {'Host':'player.vimeo.com','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
        r = requests.get(page_url,headers=headers)
        data = r.content
        data_js = plugintools.find_single_match(data,'\(function\(e,a\){var t=(.*?);if')
        js = json.loads(data_js)
        try:
            media_urlhd = js['request']['files']['progressive'][1]['url']
            media_url = media_urlhd
        except:
            media_urlsd = js['request']['files']['progressive'][0]['url']
            media_url = media_urlsd
            if media_url == "":
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
        print "$"*65+"- By PalcoTV -"+"$"*65,media_url,"$"*144
        plugintools.play_resolved_url(media_url)
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def bitvid(params):
    plugintools.log('[%s %s] Bitvid (Antes: Videoweed) %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if 'v=' in page_url:
        id_vid = page_url.split('v=') #http://embed.videoweed.es/embed.php?v=ead46574447ac
        id_vid = id_vid[-1]
        if '&' in id_vid: #http://embed.videoweed.es/embed.php?v=ead46574447ac&width=773&height=453
            id_vid = id_vid.split('&')
            id_vid = id_vid[0]
    #http://www.bitvid.sx/file/993ec886f277e http://www.videoweed.es/file/993ec886f277e       
    elif 'file' in page_url: 
        id_vid = page_url.replace('http://www.bitvid.sx/file/','').replace('http://www.videoweed.es/file/','')   
    page_url = 'http://www.bitvid.sx/embed/?v='+id_vid
    try:
        headers = {"Host": "www.bitvid.sx","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Referer": page_url}
        body,response_headers = plugintools.read_body_and_headers(page_url,headers=headers)
        url = "http://www.bitvid.sx/api/player.api.php?"
        file_id = plugintools.find_single_match(body,'flashvars.file="([^"]+)"')
        filekey = plugintools.find_single_match(body,'var fkz="([^"]+)"')#.replace(".","%2E").replace("-","%2D")
        #http://www.bitvid.sx/api/player.api.php?user=undefined&cid2=undefined&pass=undefined&cid3=undefined&key=95.22.39.89-f176a0ce46e3f19fc46e1516a98c4331-&cid=0&file=ead46574447ac&numOfErrors=0
        urlfull = url+"user=undefined&cid2=undefined&pass=undefined&cid3=undefined&key="+filekey+"&cid=0&file="+file_id+"&numOfErrors=0"                        
        ref = "http://www.bitvid.sx/player/cloudplayer.swf"
        headers = {"Host": "www.bitvid.sx","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Referer": ref}
        r = requests.get(urlfull, headers=headers)
        data = r.text
        media_url = plugintools.find_single_match(data,"url=(.*?)&title=")+'?start=0'
        if media_url != "":
            print '$'*48+'- By PalcoTV Team -'+'$'*48,media_url,'$'*115
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))          
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
        
    plugintools.play_resolved_url(media_url)


def streamable(params):
    plugintools.log('[%s %s] Streamable %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            page_url = page_url.replace("https://streamable.com/","https://streamable.com/e/")
        headers = { "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14"}
        r = requests.get(page_url)
        data = r.content
        media = plugintools.find_single_match(data,'<source src="(.*?)"')
        media=media.replace('-mobile','')
        if media !="":
            media_url = 'http:'+media
            print '$'*18+'- By PalcoTV Team -'+'$'*18,media_url,'$'*55
            plugintools.play_resolved_url(media_url)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))   
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
   
####################################################################################
##  Netu - Waaw - Hqq
####################################################################################       

def netu(params):
    plugintools.log('[%s %s] Netu %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    
    if "http://netu.tv/" in page_url:
        page_url = page_url.replace("netu","hqq")
    elif "http://waaw.tv/" in page_url:
        page_url = page_url.replace("waaw","hqq")
    
    ## Encode a la url para pasarla como valor de parámetro con hqq como host
    urlEncode = urllib.quote_plus(page_url)

    id_video = page_url.split("=")[1]
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Referer": params.get("url")}
    #http://hqq.tv/player/embed_player.php?vid=7NHXS7A81RU6&autoplay=no
    url_hqq = "http://hqq.tv/player/embed_player.php?vid="+id_video+"&autoplay=no"
    r=requests.get(url_hqq,headers=headers) 
    data_hqq =r.content
    #print data_hqq
    data64 = plugintools.find_single_match(data_hqq,'base64,([^"]+)"')
    utf8_decode = double_b64(data64)
    
    at = plugintools.find_single_match(utf8_decode,'<input name="at" type="text" value="([^"]+)"')
    ## Recoger los bytes ofuscados que contiene la url del m3u8
    b_m3u8_2,cookie_ses = get_obfuscated(id_video,at,urlEncode,headers)
    ## Obtener la url del m3u8
    url_m3u8 = tb(b_m3u8_2)
    print url_m3u8
    media_url = url_m3u8 +'|__cfduid='+cookie_ses #m3u8
    
    plugintools.play_resolved_url(media_url)  
    
####################################################################################
## Decodificación b64 para Netu
####################################################################################

## Decode
def b64(text, inverse=False):
    if inverse:
        text = text[::-1]
    return base64.decodestring(text)

## Doble decode y unicode-escape
def double_b64(data64):
    b64_data_inverse = b64(data64)
    data64_2 = plugintools.find_single_match(b64_data_inverse, "='([^']+)';")
    utf8_data_encode = b64(data64_2,True)
    utf8_encode = plugintools.find_single_match(utf8_data_encode, "='([^']+)';")
    utf8_decode = utf8_encode.replace("%","\\").decode('unicode-escape')
    
    return utf8_decode
    
## Recoger los bytes ofuscados que contiene el m3u8
def get_obfuscated(id_video,at,urlEncode,headers):
    
    url = "http://hqq.tv/sec/player/embed_player.php?vid="+id_video+"&at="+at+"&autoplayed=yes&referer=on&http_referer="+urlEncode+"&pass="
    #url = "http://hqq.tv/sec/player/embed_player.php?vid="+id_video+"&at="+at+"&autoplayed=yes&referer=on&http_referer="+urlEncode+"&pass="
    r=requests.get(url,headers=headers) 
    data =r.content
    cookie_ses = r.cookies['__cfduid']

    match_b_m3u8_1 = plugintools.find_single_match(data,'</div>.*?<script>document.write[^"]+"([^"]+)"')
    b_m3u8_1 = urllib.unquote(plugintools.find_single_match(data, match_b_m3u8_1))
    
    if b_m3u8_1 == "undefined": 
        b_m3u8_1 = urllib.unquote(data)
    match_b_m3u8_2 = plugintools.find_single_match(b_m3u8_1,'"#([^"]+)"')
    
    b_m3u8_2 = plugintools.find_single_match(b_m3u8_1, match_b_m3u8_2)
    return b_m3u8_2,cookie_ses

## Obtener la url del m3u8
def tb(b_m3u8_2):
    j = 0
    s2 = ""
    while j < len(b_m3u8_2):
        s2+= "\\u0"+b_m3u8_2[j:(j+3)]
        j+= 3
    return s2.decode('unicode-escape').encode('ASCII', 'ignore')

####################################################################################
## Fin Netu - Waaw - Hqq
####################################################################################


def videomega(params):
    plugintools.log('[%s %s] Videomega.tv %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        #http://videomega.tv/view.php?ref=07LR112DG6&width=100%&height=400
        ref = page_url.split("ref=")[1]
        page_url = 'http://videomega.tv/view.php?ref='+ref+'&width=100%&height=400'
        #post = premium = False , user="" , password="", video_password=""
        headers = {'Host':'videomega.tv','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0','Referer':page_url}        
        r = requests.get(page_url,headers=headers,allow_redirects=False)#,premium=False,user="",password="",video_password="")
        data = r.content
        #print data
        data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
        data = wiz.unpack(data)
        media_url = plugintools.find_single_match(data,'src\",\"([^"]+)"')
        if media_url =="":
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
        else:
            print '$'*52+'- By PalcoTV Team -'+'$'*52,media_url,'$'*123
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
      
    plugintools.play_resolved_url(media_url)


def flashx(params):
    plugintools.log("[%s %s] Flashx %s " % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        page_url = page_url.replace("http://www.flashx.tv/","http://www.flashx.tv/playvid-")#.replace('.html','')
        headers = {'Host':'www.flashx.tv','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'}
        r = requests.get(page_url,headers=headers)
        data = r.content
        if 'You try to access this video with Kodi' in data:
            url = plugintools.find_single_match(data,'(http://www.flashx.tv/reload.*?)">')
            r = requests.get(url,headers=headers);data = r.content
            r = requests.get(page_url,headers=headers);data = r.content   
        data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
        data = wiz.unpack(data)
        media = plugintools.find_multiple_matches(data,'file:\"([^"]+)"')
        try:
            for item in media:
                if "mp4" in item:
                        media_url = item.replace('\/','/')  
                        print '$'*49+'- By PalcoTV Team -'+'$'*49,media_url,'$'*117
                        plugintools.play_resolved_url(media_url)
                elif "flv" in item:
                        media_url = item.replace('\/','/')  
                        print '$'*49+'- By PalcoTV Team -'+'$'*49,media_url,'$'*117
                        plugintools.play_resolved_url(media_url)
        except:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
def okru(params):
    plugintools.log("[%s %s] Ok.ru %s " % (addonName, addonVersion, repr(params)))
    
    page_url=params.get("url")
    headers = {'Host': 'ok.ru','user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'}
    r = requests.get(page_url, headers=headers)
    data = r.content
    try:
        headers = {'Host': 'ok.ru','X-Requested-With': 'XMLHttpRequest','user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14',
        'Referer': page_url}
        hash_url=page_url.replace("http://ok.ru/videoembed/", "").strip()
        plugintools.log("hash= "+hash_url)
        url_json='http://ok.ru/dk?cmd=videoPlayerMetadata&mid='+hash_url
        r=requests.get(url_json,headers=headers) 
        data=r.content
        js=json.loads(data)
        videos=js["videos"]
        #opts={}
        for video in videos:
            #opts[video["name"]]=video["url"]
            if video['name'] == 'hd':
                media_url = video['url']
                plugintools.log("Url= "+media_url)
            elif video['name'] == 'sd':
                media_url = video['url']
                plugintools.log("Url= "+media_url)
            elif video['name'] == 'mobile':
                media_url = video['url']
                plugintools.log("Url= "+media_url)
            elif video['name'] == 'lowest':
                media_url = video['url']
                plugintools.log("Url= "+media_url)
            elif video['name'] == 'low':
                media_url = video['url']
                plugintools.log("Url= "+media_url)
        print '$'*84+'- By PalcoTV Team -'+'$'*84,media_url,'$'*187
        plugintools.play_resolved_url(media_url) 
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url  

def vidtome(params):
    plugintools.log("[%s %s] Vidto.me %s " % (addonName, addonVersion, repr(params)))

    page_url=params.get("url")
    try:
        page_url = page_url.replace('/embed-', '/')
        page_url = re.compile('//.+?/([\w]+)').findall(page_url)[0]
        page_url = 'http://vidto.me/embed-%s.html' % page_url
        r=requests.get(page_url)
        data=r.content
        result = re.compile('(eval.*?\)\)\))').findall(data)[-1]
        result = unpackerjs.unpackjs(result)
        quality=plugintools.find_multiple_matches(result, 'label:"([^"]+)')
        url_media=plugintools.find_multiple_matches(result, 'file:"([^"]+)')
        media_url=url_media[len(quality)-1]
        print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95 
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
        
    plugintools.play_resolved_url(media_url)   
       
    
def playwire(params):
    plugintools.log("[%s %s] Playwire en Ourmatch.net %s " % (addonName, addonVersion, repr(params)))

    url=params.get("url")
    r=requests.get(url)
    data=r.content
    video_contents=plugintools.find_single_match(data, 'var video_contents = {(.*?)</script>')
    items_video=plugintools.find_multiple_matches(video_contents, '{(.*?)}')
    for entry in items_video:        
        url_zeus=plugintools.find_single_match(entry, 'config.playwire.com/(.*?)&quot;')
        zeus='http://config.playwire.com/'+url_zeus
        type_item=plugintools.find_single_match(entry, "type\':\'([^']+)")
        lang=plugintools.find_single_match(entry, "lang:\'([^']+)")
        title_item='[COLOR white]'+type_item+' [/COLOR][I][COLOR lightyellow]'+lang+'[/I][/COLOR]'
        print zeus,title_item
        url_media=[];posters=[]
        r=requests.get(zeus)
        data=r.content
        url_f4m=plugintools.find_single_match(data, 'f4m\":\"(.*?)f4m');url_f4m=url_f4m+'f4m'
        poster=plugintools.find_single_match(data, 'poster\":\"(.*?)png');poster=poster+'png'
        posters.append(poster)
        url_media.append(url_f4m)
        url_videos=dict.fromkeys(url_media).keys()
        url_poster=dict.fromkeys(posters).keys()
        r=requests.get(url_videos[0])
        data=r.content
        #print data
        burl=plugintools.find_single_match(data, '<baseURL>([^<]+)</baseURL>')
        media_item=plugintools.find_multiple_matches(data, '<media(.*?)"/>')
        i=1
        while i<=len(media_item):
            for item in media_item:
                plugintools.log("item= "+item)
                media=plugintools.find_single_match(item, 'url="([^"]+)')
                bitrate=plugintools.find_single_match(item, 'bitrate="([^"]+)')
                url_media=burl+'/'+media
                title_fixed=title_item+' [COLOR lightblue][I]('+bitrate+' kbps)[/I][/COLOR]'
                plugintools.add_item(action="play", title=title_fixed, url=url_media, thumbnail=url_poster[0], fanart='http://images.huffingtonpost.com/2014-09-12-image1.JPG', folder=False, isPlayable=True)
                i=i+1                
    #http://config.playwire.com/17003/videos/v2/4225978/zeus.json
    #https://config.playwire.com/17003/videos/v2/4225978/manifest.f4m
    #https://cdn.phoenix.intergi.com/17003/videos/4225978/video-sd.mp4?hosting_id=17003
                  
def uptostream(params):
    plugintools.log('[%s %s] Uptostream %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        page_url = page_url.replace('http://uptobox.com/','http://uptostream.com/')
        if not "iframe" in page_url:
            page_url = page_url.replace("http://uptostream.com/","http://uptostream.com/iframe/")
        r = requests.get(page_url)
        data = r.content
        sources = plugintools.find_multiple_matches(data,"<source src='(.*?)'.*?data-res='(.*?)'.*?lang='(.*?)'")
        if len(sources) >1:
            options = []
            for item in sources:
                opct = '[COLORlightyellow]'+item[2]+' '+item[1]+'[/COLOR]'
                options.append(opct)
            select_option = plugintools.selector(options,'PalcoTV **Uptobox-Uptostream**')
            ######### Evitamos el error de cancelacion con valor -1 ########
            if select_option >=0:  
                i = select_option
                media_url = 'http:'+sources[i][0]
                print '$'*20+'- By PalcoTV Team -'+'$'*20,media_url,'$'*59
                plugintools.play_resolved_url(media_url)
            else: pass
            ################################################################
        elif len(sources) ==1:
            media_url = 'http:'+sources[0][0]
            print '$'*20+'- By PalcoTV Team -'+'$'*20,media_url,'$'*59
            plugintools.play_resolved_url(media_url)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
      
def youwatch(params):
    plugintools.log('[%s %s] YouWatch %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        page_url = page_url.replace("http://youwatch.org/","http://uroclm5d.xyz/")
        page_url = page_url.replace("http://chouhaa.info/","http://uroclm5d.xyz/")
        page_url = page_url.replace("http://msemen.info/","http://uroclm5d.xyz/")

        if not "http://uroclm5d.xyz/embed-" in page_url:
            page_url = page_url.replace("http://uroclm5d.xyz/","http://uroclm5d.xyz/embed-") + ".html"
        r = requests.get(page_url)
        data = r.content
        url_b64 = plugintools.find_single_match(data,'<iframe src="([^"]+)"')
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0','Referer': page_url}
        r = requests.get(url_b64,headers=headers)
        data = r.content
        media = plugintools.find_single_match(data,'file:"([^"]+)"').strip()
        if media !="":
            media_url = media +'|Referer='+ page_url
            print '$'*61+'- By PalcoTV Team -'+'$'*61,media_url,'$'*141
            plugintools.play_resolved_url(media_url)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
def vidggto(params):
    plugintools.log('[%s %s] Vidgg.to %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        r = requests.get(page_url)
        data = r.content
        # print data
        key = plugintools.find_single_match(data,'flashvars.filekey="(.*?)"')
        file_id = plugintools.find_single_match(data,'flashvars.file="(.*?)"')
        cid = plugintools.find_single_match(data,'flashvars.domain="(.*?)"')
        domain = plugintools.find_single_match(data,'flashvars.cid="(.*?)"')
        ref = "http://www.vidgg.to/player/cloudplayer.swf"

        headers = {"Host":"www.vidgg.to","User-Agent": '"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"', "Referer": ref}
        # http://www.vidgg.to/api/player.api.php?key=87.223.99.234-6e60102419de42e1a5550fd0119a211e&numOfErrors=0&user=undefined&pass=undefined&cid=1&file=288d5af5a64c0&cid3=seriesyonkis.sx&cid2=undefined
        url_new = "http://www.vidgg.to/api/player.api.php?key="+key+"&numOfErrors=0&user=undefined&pass=undefined&cid="+cid+"&file="+file_id+"&cid3="+domain+"&cid2=undefined"
    
        r = requests.get(url_new,headers=headers)
        data = r.content
        #print data
        #url=http://s240.zerocdn.to/dl/23a3e0c1ef50a88777fbee9ba554bc85/5686721b/ff1208c256562d03962845fb3af0655e16.flv&title=4N4T0M14.12x8.m720p%26asdasdas&site_url=http://www.vidgg.to/video/288d5af5a64c0&seekparm=&enablelimit=0
        media_url = plugintools.find_single_match(data,'url=(.*?)&title')
        print '$'*46+'- By PalcoTV Team -'+'$'*46,media_url,'$'*111
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url)

def vimple(params):
    plugintools.log('[%s %s] Vimple %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        page_url = page_url.replace('http://player.vimple.ru/content/preloader.swf?id=','http://player.vimple.ru/iframe/')
        r = requests.get(page_url)
        data = r.content
        # print data
        url = plugintools.find_single_match(data,"dataUrl:'(.*?)'")
        if url !="":
            url_new = "http://player.vimple.ru"+url
            ref = "http://videoplayer.ru/ru/player/spruto/player.swf?v=3.1.0.7" 
            headers = {"Host":"s13.vimple.ru:8081","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Referer":ref}
    
            r = requests.get(url_new)
            data = r.content
            user_id = r.cookies['UniversalUserID']
            #http://s13.vimple.ru:8081/vv52/716622.mp4?v=2c6a0a43-bfa1-469e-abf8-8b7d8df9769b&t=635872710621810000&d=7334&sig=6edab5d97959da7b3451444cb002a557
            #http://s15.vimple.ru:8081/vv65/698440.mp4?v=bfe4e467-2765-4be0-a479-22ee1e2ab515&t=635872785719935000&d=5987&sig=09ad419d594c1a674b4caaea3efca60f|Cookie=UniversalUserID=24259d8f030a42df9fe6eec1e80083b9
            js = json.loads(data)
            media = js['sprutoData']['playlist'][0]['video'][0]['url']
            media_url = media+"|Cookie=UniversalUserID="+user_id
            print '$'*92+'- By PalcoTV Team -'+'$'*92,media_url,'$'*203
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))   
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)

def idowatch(params):
    plugintools.log('[%s %s] IdoWatch %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        r = requests.get(page_url)
        data = r.content
        #bloq_url = plugintools.find_single_match(data,"<script type='text/javascript'>(.*?)</script>")
        #media = plugintools.find_multiple_matches(bloq_url,'file: "(.*?)"')
        if 'File Not Found' in data:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
            pass
        else:
            data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
            data = wiz.unpack(data)
            media = plugintools.find_multiple_matches(data,'file:"(.*?)"')
            for item in media:
                print item
                if item.endswith(".mp4"):
                        media_url = item.replace('\/','/')
                        plugintools.play_resolved_url(media_url)  
                        print '$'*36+'- By PalcoTV Team -'+'$'*36,media_url,'$'*91
                elif item.endswith(".flv"):
                        media_url = item.replace('\/','/') 
                        plugintools.play_resolved_url(media_url) 
                        print '$'*36+'- By PalcoTV Team -'+'$'*36,media_url,'$'*91
                else:pass                      
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url  

def cloudtime(params):
    plugintools.log('[%s %s] CloudTime %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        headers = {"Host": "www.cloudtime.to","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r = requests.get(page_url,headers=headers)
        data = r.content
        
        stepkey = plugintools.find_single_match(data,'name="stepkey" value="([^"]+)"')
        submit = plugintools.find_single_match(data,'name="submit" class="btn" value="([^"]+)"')
        post = "stepkey="+stepkey+"&submit="+submit
        headers = {"Host": "www.cloudtime.to","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Referer":page_url}
        body,response_headers = plugintools.read_body_and_headers(page_url,headers=headers,post=post)
        cid3 = "cloudtime%2Eto"
        file_id = plugintools.find_single_match(body,'flashvars.file="([^"]+)"').replace(".","%2E").replace("-","%2D")
        key = plugintools.find_single_match(body,'flashvars.filekey="([^"]+)"').replace(".","%2E").replace("-","%2D")
        new_url = "http://www.cloudtime.to/api/player.api.php?cid3="+cid3+"&file="+file_id+"&key="+key+"&numOfErrors=0&pass=undefined&user=undefined&cid2=undefined&cid=1"
        ref = "http://www.cloudtime.to/player/cloudplayer.swf"
        headers = {"Host": "www.cloudtime.to","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Referer":ref}
        r = requests.get(new_url,headers=headers)
        data = r.content
        try:
            media = data.replace("url=","").split('&')
            media_url = media[0]
            print '$'*44+'- By PalcoTV Team -'+'$'*44,media_url,'$'*107
        except:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
            pass 
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url)


def vidzitv(params):
    plugintools.log('[%s %s] Vidzi.tv %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        headers = {"Host": "vidzi.tv","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r=requests.get(page_url,headers=headers)
        data=r.text
        data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
        data = wiz.unpack(data)
        
        media = plugintools.find_multiple_matches(data,'file:"([^"]+)"')
        
        if media =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
        else:
            for item in media:
                try:
                    if "mp4" in item:
                            media_url = item.replace('\/','/')  
                            print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95
                except:
                    if "m3u8" in item:
                        media_url = item.replace('\/','/')  
                        print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95                
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url)


def vodlocker(params):
    plugintools.log('[%s %s] VodLocker %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    if not "embed" in page_url:
      page_url = page_url.replace("http://vodlocker.com/","http://vodlocker.com/embed-") + ".html"

    try:
        headers = {"Host": "vodlocker.com","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r = requests.get(page_url,headers=headers)
        data = r.content
        #print data
        media_url = plugintools.find_single_match(data,'file: "([^"]+)"')
        print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95 
        if media_url == "":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)


def streamenet(params):
    plugintools.log('[%s %s] Streame.net %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        page_url = page_url.replace("#","")
        if not "embed" in page_url:
            page_url = page_url.replace("http://streame.net/","http://streame.net/embed-") + ".html"
        headers = {"Host": "streame.net","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r = requests.get(page_url,headers=headers)
        data = r.content
        if 'File was deleted' in data:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
        else:
            media = plugintools.find_multiple_matches(data,'file:"([^"]+)"')
            for item in media:
                if item.endswith(".mp4"): media_url = item
                elif item.endswith(".m3u8"): media_url = item
                elif item.endswith(".flv"): media_url = item
        print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95 
        plugintools.play_resolved_url(media_url)
                  
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
       
def watchonline(params):
    plugintools.log('[%s %s] WatchOnLine %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            page_url = page_url.replace("http://www.watchonline.to/","http://www.watchonline.to/embed-") + ".html"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r = requests.get(page_url,headers=headers)
        data = r.content
        #data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
        #data = wiz.unpack(data)
        sources = plugintools.find_multiple_matches(data,'file:"([^"]+)"')
        for link in sources:
            if link.endswith(".mp4"):
                media_url = link+'|Referer='+page_url
            elif link.endswith(".m3u8"):
                media_url = link+'|Referer='+page_url
            elif link.endswith(".mpd"):
                media_url = link+'|Referer='+page_url
        media_url = media_url+'|Referer='+page_url
        print '$'*35+'- By PalcoTV Team -'+'$'*35,media_url,'$'*89
        plugintools.play_resolved_url(media_url)   
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
       
def allvid(params):
    plugintools.log('[%s %s] Allvid %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            page_url = page_url.replace("http://allvid.ch/","http://allvid.ch/embed-") + ".html"
        #headers = {"Host": "allvid.ch","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r=requests.get(page_url)
        data = r.content
        url_redirect = plugintools.find_single_match(data,'<iframe src="([^"]+)"')

        r=requests.get(url_redirect)
        data = r.text
        data = plugintools.find_single_match(data,"<script type='text/javascript'>(.*?)</script>")
        data = wiz.unpack(data)
        #plugintools.log("data="+data)
        try:        
            bloq_urls = plugintools.find_single_match(data,'sources:\[\{(.*?)\}\]')
            if bloq_urls == "":
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
            else:
                urls = plugintools.find_multiple_matches(bloq_urls,'file:"([^"]+)"')
                for item in urls:
                    if item.endswith(".mp4") == True:
                        media_url = item
                        print '$'*35+'- By PalcoTV Team -'+'$'*35,media_url,'$'*89
        except:
            url = plugintools.find_single_match(bloq_urls,'file:"([^"]+)')
            if url == "":
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
            else:
                media_url = url
                print '$'*35+'- By PalcoTV Team -'+'$'*35,media_url,'$'*89
        plugintools.play_resolved_url(media_url)         
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url 

def streamplay(params):
    plugintools.log('[%s %s] StreamPlay %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://streamplay.to/","http://streamplay.to/embed-") + ".html"  
    try:        
        headers = {"Host": "streamplay.to","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r = requests.get(page_url,headers=headers)
        data = r.text  
        #print data

        data = plugintools.find_single_match(data,"<script type='text/javascript'>(.*?)</script>")
        data = wiz.unpack(data)
        plugintools.log("data="+data)
        try:
            bloq_urls = plugintools.find_single_match(data,'sources:\[\{(.*?)\}\]')
            if bloq_urls == "":
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
            else:
                urls = plugintools.find_multiple_matches(bloq_urls,'file:"([^"]+)"')
                for item in urls:
                    if item.endswith(".mp4") == True:
                        media_url = item
                        print '$'*35+'- By PalcoTV Team -'+'$'*35,media_url,'$'*89
        except:
            url = plugintools.find_single_match(bloq_urls,'file:"([^"]+)')
            if url == "":
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
            else:
                media_url = url
                print '$'*35+'- By PalcoTV Team -'+'$'*35,media_url,'$'*89       
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url)

def myvideoz(params):
    plugintools.log('[%s %s] MyvideoZ %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        headers = {"Host": "myvideoz.net","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r = requests.get(page_url,headers=headers)
        data = r.content
        sess = r.cookies['PHPSESSID']
        
        url = plugintools.find_single_match(data,"<meta property=\"og:video\" content='([^']+)'")
        if url == "":
            plugintools.log("Archivo borrado: "+page_url)
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "El Archivo ha sido borrado", 3 , art+'icon.png'))
        #http://myvideoz.net/nuevo/player/player.swf?config=http%3A%2F%2Fmyvideoz.net%2Fnuevo%2Fplayer%2Ffsb.php%3Fv%3D70764%26autostart%3Dno
        ref = url.replace('%3A',':').replace('%2F','/').replace('%3D','=').replace('%3F','?').replace('%26','&')
        new_url = ref.replace('http://myvideoz.net/nuevo/player/player.swf?config=','') 
        #http://myvideoz.net/nuevo/player/fsb.php?v=70764&autostart=no
        
        headers = {"Host": "myvideoz.net","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
        "Referer": ref,"PHPSESSID":sess}

        r = requests.get(new_url,headers=headers)
        data = r.content 
        media_url = plugintools.find_single_match(data,"<file>([^<]+)</file>")
        print '$'*40+'- By PalcoTV Team -'+'$'*40,media_url,'$'*99 
        if media_url == "":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
   
    plugintools.play_resolved_url(media_url)

def rutube(params):
    plugintools.log('[%s %s] Rutube.ru %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        ###################################### Url tipos #########################################
        # http://rutube.ru/play/embed/8260464 "http://video.rutube.ru/3593338" 
        ########################################################################################## 
        if not "embed" in page_url:
            page_url = page_url.replace("http://rutube.ru/video/","http://rutube.ru/play/embed/")
            page_url = page_url.replace("http://video.rutube.ru/","http://rutube.ru/play/embed/")
        ##########################################################################################
        ###################################### Url tipo ##########################################
        # "http://rutube.ru/play/embed/8172108?p=fKHaOAcNeNsHKwDFWSu8bA" 
        ##########################################################################################
        if 'p=' in page_url:
            page = params.get("url")
            id_vid = plugintools.find_single_match(page,'http://rutube.ru/play/embed/(.*?)\?p=')
            patron = 'http://rutube.ru/play/embed/'+id_vid+'?p='
            id_p = page.replace(patron,'')
            print id_p
            #http://rutube.ru/api/play/options/8172108/?format=json&no_404=true&sqr4374_compat=1&referer=http://rutube.ru/play/embed/8172108?p=fKHaOAcNeNsHKwDFWSu8bA&p=fKHaOAcNeNsHKwDFWSu8bA
            url = 'http://rutube.ru/api/play/options/'+id_vid+'/?format=json&no_404=true&sqr4374_compat=1&referer='+page+'&p='+id_p
        else:
            id_vid = page_url.replace("http://rutube.ru/play/embed/","")
            #http://rutube.ru/api/play/options/3593338/?format=json&no_404=true&sqr4374_compat=1&referer=http://rutube.ru/play/embed/3593338
            url = 'http://rutube.ru/api/play/options/'+id_vid+'/?format=json&no_404=true&sqr4374_compat=1&referer='+page_url 
        ##########################################################################################
        r = requests.get(url)
        data = r.content
        #http://bl.rutube.ru/route/0c458bed8ae24747a0fcf2bf2178229d.m3u8?guids=5ea7c431-c830-4eda-b3a5-6c8c40e89353_768x416_700413_avc1.42c01e_mp4a.40.5&sign=yOeOwmU8kW3_KMYBd09T6g&expire=1454622396
        try:
            js = json.loads(data)
            media_url = js['video_balancer']['m3u8']
            print '$'*85+'- By PalcoTV Team -'+'$'*85,media_url,'$'*189
            plugintools.play_resolved_url(media_url)
        except:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
def dailymotion(params):
    plugintools.log('[%s %s] Dailymotion %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if 'jukebox' in page_url :
        r = requests.get(page_url)
        data = r.content
        id_vid = plugintools.find_single_match(data,'current_video\":\"([^"]+)\"')
        #http://www.dailymotion.com/widget/jukebox?list[]=%2Fplaylist%2Fx2u81l_djflakf1_confa%2F1&#038;skin=default&#038;autoplay=0&#038;automute=0
        page_url = "http://www.dailymotion.com/embed/video/"+id_vid

    if not "embed" in page_url:
        page_url = page_url.replace("http://www.dailymotion.com/video/","http://www.dailymotion.com/embed/video/")
    try:
        r = requests.get(page_url)
        data = r.content
    
        bloq_link = plugintools.find_single_match(data,'qualities"(.*?)"reporting"').replace('\/','/')
        if '1080' in bloq_link:
            media_url = plugintools.find_single_match(data,'1080".*?url":"(.*?)"').strip().replace('\/','/')
        elif '720' in bloq_link:
            media_url = plugintools.find_single_match(data,'720".*?url":"(.*?)"').strip().replace('\/','/')
        elif '480' in bloq_link:
            media_url = plugintools.find_single_match(data,'480".*?url":"(.*?)"').strip().replace('\/','/')
        elif '380' in bloq_link:
            media_url = plugintools.find_single_match(data,'380".*?url":"(.*?)"').strip().replace('\/','/')
        elif '240' in bloq_link:
            media_url = plugintools.find_single_match(data,'240".*?url":"(.*?)"').strip().replace('\/','/')
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
        print '$'*53+'- By PalcoTV Team -'+'$'*53,media_url,'$'*125
        plugintools.play_resolved_url(media_url)
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def spruto(params):
    plugintools.log('[%s %s] Spruto.tv %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        headers = {"Host":"www.spruto.tv","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"}
        r = requests.get(page_url,headers=headers)
        data = r.content
        file_vid = plugintools.find_single_match(data,'file:"([^"]+)"').strip()
    
        if 'mp4' in file_vid:
            media_url = file_vid
            print '$'*35+'- By PalcoTV Team -'+'$'*35,media_url,'$'*89
            plugintools.play_resolved_url(media_url)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def stormo(params):
    plugintools.log('[%s %s] Stormo.tv %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        headers = {"Host":"www.stormo.tv","User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"}
        r = requests.get(page_url,headers=headers)
        data = r.content
        file_vid = plugintools.find_single_match(data,'file:"([^"]+)"').strip()
    
        if 'mp4' in file_vid:
            media_url = file_vid
            print '$'*35+'- By PalcoTV Team -'+'$'*35,media_url,'$'*89
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)

def myviru(params):
    plugintools.log('[%s %s] Myvi.ru %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        r = requests.get(page_url)
        data = r.content
        # print data
        url = plugintools.find_single_match(data,"dataUrl:'(.*?)'")
        if url !="":
            url_new = "http://myvi.ru"+url
            ref = "http://videoplayer.ru/ru/player/spruto/player.swf?v=3.1.0.24" 
            headers = {"Host":"fs.myvi.ru","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Referer":ref}
    
            r = requests.get(url_new)
            data = r.content
            user_id = r.cookies['UniversalUserID']
    
            js = json.loads(data)
            media = js['sprutoData']['playlist'][0]['video'][0]['url']
            media_url = media+"|Cookie=UniversalUserID="+user_id
            print '$'*75+'- By PalcoTV Team -'+'$'*75,media_url,'$'*169
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)

def youtube(params):
    plugintools.log('[%s %s] Youtube %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        headers = {'Host': 'www.youtube.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'}
        if 'embed' in page_url:
            page_url = page_url.replace('http://www.youtube.com/embed/','https://www.youtube.com/watch?v=')
            page_url = page_url.replace('https://www.youtube.com/embed/','https://www.youtube.com/watch?v=')

        if (not 'http://www.youtube.com/' in page_url) and (not 'https://www.youtube.com/' in page_url):
            page_url = 'https://www.youtube.com/watch?v='+page_url
        try:
            ######## Utilizamos el addon de youtube como primera opción ###########
            id_vid = page_url.replace('https://www.youtube.com/watch?v=','')
            url_addon = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid='+id_vid
            print '<'*10+'- Metodo Repr: Addon_Youtube -'+'>'*10
            print '$'*42+'- By PalcoTV Team -'+'$'*42,media_url,'$'*103
            plugintools.play_resolved_url(media_url)
            #######################################################################
        except:
            r = requests.get(page_url,headers=headers)
            data = r.content
            fmt_stream_map = plugintools.find_single_match(data,'url_encoded_fmt_stream_map\":\"([^"]+)\"')
            if fmt_stream_map != "":
                fmt_stream_map = fmt_stream_map.split(",")
                urlfull = fmt_stream_map[0]
                url = urlfull.split('url=')
                url = url[-1]
                url = url.split("\\u")
                url_final = urllib.unquote(url[0])
                media_url = url_final
                print '<'*10+'- Metodo Repr: Conector -'+'>'*10
                print '$'*142+'- By PalcoTV Team -'+'$'*142,media_url,'$'*303
                plugintools.play_resolved_url(media_url)
            else:
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
def filmon(params):
    plugintools.log('[%s %s] Filmon %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    r = requests.get(page_url)
    data = r.content
    
    channel_id = plugintools.find_single_match(data,"current_channel_id= last_clicked_channel_id = '([^']+)'")
    ref = 'https://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FacebookPlayer.swf?channel_id='+channel_id
    page_url = 'https://www.filmon.com/tv/channel/info/'+channel_id
    headers = {'Host': 'www.filmon.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0','Referer': ref}
    r = requests.get(page_url,headers=headers)
    data_js = r.text
    try:
        js = json.loads(data_js)
        media = js['data']['streams'][1]['url'].replace('%3A',':').replace('%2F','/').replace('%3D','=').replace('%3F','?').replace('%26','&')
        playpath = channel_id+'.low.stream'
        #rtmp://live-1124.la2.edge.filmon.com/live/?id=0ad5aac39bb13fbe910be750d11648cd1aedd7c5c7e2d0f52da0f88e4fa3e187ac21fabfc99f21ed96082cfe1a7d2f867dd882388ab8dd1829db50331f560c8549517a080ce61bd696a4ae279fa693c48bc23fbb536041216e6ba552e8dbf731d82e0aeb8db654767bfb6d316e6f9aefdc8482cfe8bd8d0a931d5c53fa20b9d24bf0fa994fb0ec2df8b6f9af4b4667aed1e30b0cd0441e07<playpath>2984.low.stream <swfUrl>https://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf?v=d545aefd <pageUrl>https://www.filmon.com/tv/bikini-girls-showing-off

        media_url = media+'&playpath='+playpath+'&pageUrl=https://www.filmon.com/tv/channel/info/'+channel_id+'&swfUrl=https://www.filmon.com/tv/modules/FilmOnTV/files/flashapp/filmon/FilmonPlayer.swf?v=d545aefd'
        print '$'*255+'- By PalcoTV Team -'+'$'*255,media_url,'$'*529
    except:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Canal no disponible", 3 , art+'icon.png'))

    plugintools.play_resolved_url(media_url)

def thevideome(params):
    plugintools.log('[%s %s] TheVideo.me %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            page_url = page_url.replace("http://thevideo.me/","http://thevideo.me/embed-") + ".html" 
        r = requests.get(page_url)
        data = r.content
        key_tkn = plugintools.find_single_match(data,"var mpri_Key='(.*?)'")
        sources = plugintools.find_single_match(data,"sources: \[(.*?)\],")
        media_file = plugintools.find_multiple_matches(sources,"file: '([^']+)'")
        url_tkn = 'http://thevideo.me/jwv/'+key_tkn
        if sources =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
        else:
            if media_file > 1: 
                max_quality = media_file[-1]
                media_url = max_quality
            else: 
                media_url = media_file
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0","Referer":page_url}        
        r = requests.get(url_tkn,headers=headers)
        data = r.text
        tkn = plugintools.find_single_match(data,"jwConfig(.*?)return").replace('|','')
        media_url = media_url+'?direct=false&ua=1&vt='+tkn
        plugintools.play_resolved_url(media_url)
        print '$'*268+'- By PalcoTV Team -'+'$'*268,media_url,'$'*555
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    
##################################### VIDEOWOOD #########################################

def videowood(params):
    plugintools.log('[%s %s] Videowood.Tv %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://videowood.tv/video/","http://videowood.tv/embed/")
    try: 
        r = requests.get(page_url)
        data = r.content
        
        data_encode = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
        data_decode = decode_videowood(data_encode)
        if 'http' or 'https' in data_decode:
            media_url = plugintools.find_single_match(data_decode,"\'(.*?)\'")
            print '$'*36+'- By PalcoTV Team -'+'$'*36,media_url,'$'*91
            plugintools.play_resolved_url(media_url)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))                 
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url    

def decode_videowood(text):
    text = re.sub(r"\s+|/\*.*?\*/", "", text)
    data = text.split("+(ﾟДﾟ)[ﾟoﾟ]")[1]
    chars = data.split("+(ﾟДﾟ)[ﾟεﾟ]+")[1:]

    txt = ""
    for char in chars:
        char = char \
            .replace("(oﾟｰﾟo)","u") \
            .replace("c", "0") \
            .replace("(ﾟДﾟ)['0']", "c") \
            .replace("ﾟΘﾟ", "1") \
            .replace("!+[]", "1") \
            .replace("-~", "1+") \
            .replace("o", "3") \
            .replace("_", "3") \
            .replace("ﾟｰﾟ", "4") \
            .replace("(+", "(")
        char = re.sub(r'\((\d)\)', r'\1', char)

        c = ""; subchar = ""
        for v in char:
            c+= v
            try: x = c; subchar+= str(eval(x)); c = ""
            except: pass
        if subchar != '': txt+= subchar + "|"
    txt = txt[:-1].replace('+','')

    txt_result = "".join([ chr(int(n, 8)) for n in txt.split('|') ])

    return toStringCases(txt_result)

def toStringCases(txt_result):
    sum_base = ""
    m3 = False
    if ".toString(" in txt_result:
        if "+(" in  txt_result:
            m3 = True
            sum_base = "+"+find_single_match(txt_result,".toString...(\d+).")
            txt_pre_temp = find_multiple_matches(txt_result,"..(\d),(\d+).")
            txt_temp = [ (n, b) for b ,n in txt_pre_temp ]
        else:
            txt_temp = find_multiple_matches(txt_result, '(\d+)\.0.\w+.([^\)]+).')
        for numero, base in txt_temp:
            code = toString( int(numero), eval(base+sum_base) )
            if m3:
                txt_result = re.sub( r'"|\+', '', txt_result.replace("("+base+","+numero+")", code) )
            else:
                txt_result = re.sub( r"'|\+", '', txt_result.replace(numero+".0.toString("+base+")", code) )
    return txt_result

def toString(number,base):
    string = "0123456789abcdefghijklmnopqrstuvwxyz"
    if number < base:
        return string[number]
    else:
        return toString(number//base,base) + string[number%base]

#########################################################################################

def neodrive(params):
    plugintools.log('[%s %s] NeoDrive %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        
        page_url = page_url.replace('http://www.cloudzilla.to/','http://neodrive.co/')
        #if not "embed" in page_url:
            #page_url = page_url.replace("http://neodrive.co/share/file/","http://neodrive.co/embed/")
        r = requests.get(page_url,allow_redirects=False)
        data = r.content
        data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
        data = wiz.unpack(data)
        print data
        media = plugintools.find_single_match(data,'var vurl="([^"]+)"')
        if media !="":
            media_url = media
            print '$'*45+'- By PalcoTV Team -'+'$'*45,media_url,'$'*109
            plugintools.play_resolved_url(media_url)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
        
def thevideobee(params):
    plugintools.log('[%s %s] TheVideobee.to %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    
    if not "embed" in page_url:
        page_url = page_url.replace("http://thevideobee.to/","https://thevideobee.to/embed-")
        page_url = page_url.replace("https://thevideobee.to/","https://thevideobee.to/embed-")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    #try:
    print page_url 
    r = requests.get(page_url,headers=headers)#,allow_redirects=False)
    data = r.content
    print data
    #data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
    #data = wiz.unpack(data)
    #print data
    #bloq_media = plugintools.find_single_match(data,'sources: \[\{(.*?)\}\]')
    #media = plugintools.find_multiple_matches(data,'file:"([^"]+)"')
    '''
    if bloq_media =="":
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    else: 
        media_url = media[-1]
        print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95
        plugintools.play_resolved_url(media_url) 
       
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    '''
     
    
def fileshow(params):
    plugintools.log('[%s %s] Fileshow.Tv %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            id_vid = plugintools.find_single_match(page_url,'http://fileshow.tv/(.*?)/')
            page_url = "http://bestream.tv/plugins/mediaplayer/site/_embed_fileshow.php?u="+id_vid

        r = requests.get(page_url)
        data = r.content

        media = plugintools.find_single_match(data,'file: "([^"]+)"')
        if media !="":
            media_url = media
            print '$'*80+'- By PalcoTV Team -'+'$'*80,media_url,'$'*179
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)

def vid(params):
    plugintools.log('[%s %s] Vid.ag %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://vid.ag/","http://vid.ag/embed-") 

    try: 
        r = requests.get(page_url)
        data = r.text
        data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
        data = wiz.unpack(data)

        sources = plugintools.find_single_match(data,"sources:\[(.*?)\],")
        media_file = plugintools.find_multiple_matches(sources,'file:"([^"]+)"')
        if sources =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
        elif media_file > 1: max_quality = media_file[-1];media_url = max_quality
        else: media_url = media_file
        print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95   
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url)

def vidxtreme(params):
    plugintools.log('[%s %s] Vidxtreme.to %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://vidxtreme.to/","http://vidxtreme.to/embed-")+'.html' 
    try: 
        r = requests.get(page_url)
        data = r.text
        try:
            data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
            data = wiz.unpack(data)
            sources = plugintools.find_single_match(data,"sources:\[(.*?)\],")
            media_file = plugintools.find_multiple_matches(sources,'file:"([^"]+)"')   
            if media_file > 1: max_quality = media_file[-1];media_url = max_quality
            else: media_url = media_file
            print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95
            plugintools.play_resolved_url(media_url)
        except:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png')) 
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
      
def vidup(params):
    plugintools.log('[%s %s] Vidup.me %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            page_url = page_url.replace("http://beta.vidup.me/","http://beta.vidup.me/embed-")+'.html' 
        r = requests.get(page_url)
        data = r.content
    
        sources = plugintools.find_single_match(data,"sources: \[(.*?)\]")
        media_file = plugintools.find_multiple_matches(sources,"file: '([^']+)'")
        if sources =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
        elif media_file > 1: max_quality = media_file[-1];media_url = max_quality
        else: media_url = media_file
        print '$'*140+'- By PalcoTV Team -'+'$'*140,media_url,'$'*299
        plugintools.play_resolved_url(media_url)
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
def watchvideo(params):
    plugintools.log('[%s %s] watchvideo.us %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://watchvideo.us/","http://watchvideo.us/embed-")

    try:
        headers = {"Host": "watchvideo.us","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r=requests.get(page_url,headers=headers)
        data=r.text
        media = plugintools.find_multiple_matches(data,'file:"([^"]+)"')
        if media =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
        else:
            for item in media:
                try:
                    if "mp4" in item:
                            media_url = item.replace('\/','/')  
                            print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95
                except:
                    if "m3u8" in item:
                        media_url = item.replace('\/','/')  
                        print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95                
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url)

def speedvid(params):
    plugintools.log('[%s %s] Speedvid.net %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            page_url = page_url.replace("http://www.speedvid.net/","http://www.speedvid.net/embed-")+'.html'
        try:
            r = requests.get(page_url)
            data = r.content
            data_eval = plugintools.find_single_match(data,"<script type='text/javascript'>eval\(function\(p,a,c,k,e,d\)(.*?)\s+</script>")
            data_packed  = wiz.unpack(data_eval)
            n_files = plugintools.find_multiple_matches(data_packed,"file:'([^']+)'")
            if len(n_files)>1: media_url = n_files[0]
            else: media_url = plugintools.find_single_match(data_packed,"file:'([^']+)'")
            print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95
            plugintools.play_resolved_url(media_url)
        except: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url   

def exashare(params):
    plugintools.log('[%s %s] Exsahare %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        page_url = page_url.replace("http://chefti.info/","http://erd9x4.info/")
        page_url = page_url.replace("http://ajihezo.info/","http://erd9x4.info/")
        if not "embed" in page_url:
            page_url = page_url.replace("http://erd9x4.info/","http://erd9x4.info/embed-")+'.html' 
        r = requests.get(page_url)
        data = r.content
        url64 = plugintools.find_single_match(data,'<iframe src="(.*?)"')
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0','Referer': page_url}
        r = requests.get(url64,headers=headers)
        data = r.content
        sources = plugintools.find_single_match(data,"sources: \[\{(.*?)\}\],")
        media_file = plugintools.find_multiple_matches(sources,'file:"([^"]+)"')
        if sources =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
        elif media_file > 1: max_quality = media_file[-1];media_url = max_quality
        else: media_url = media_file
        print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95
        plugintools.play_resolved_url(media_url)
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
def vodbeast(params):
    plugintools.log('[%s %s] Vodbeast.com %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://vodbeast.com/","http://vodbeast.com/embed-")+'.html'   
    try: 
        r = requests.get(page_url)
        data = r.content

        sources = plugintools.find_single_match(data,"sources: \[\{(.*?)\}\],")
        media_file = plugintools.find_multiple_matches(sources,'file: "([^"]+)"')
        for item in media_file:
            try:
                if "mp4" in item:
                    media_url = item.replace('\/','/')  
                    print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95
                elif "m3u8" in item:
                    media_url = item.replace('\/','/')  
                    print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95
            except: 
                xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png')) 
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url)

def nosvideo(params):
    plugintools.log('[%s %s] Nosvideo.com %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        if not 'embed' in page_url:
            page_url = page_url.replace("http://nosvideo.com/","http://nosvideo.com/embed/")
            page_url = page_url.replace("http://noslocker.com/","http://nosvideo.com/embed/")
        r = requests.get(page_url)#,headers=headers)
        data = r.content
        #http://on14serverfiles.loma.com.nosvideo.com/alrso4krwu6xshtdgsdrq6b7o2s6aflrbvmlull6ldmpmkeqehwazff3w225tl7rppgr6jm7v64blshfmz2n3rxveokqbmjp2ammz3ro6bdzdyxtrts4xmv5ezqydbz5/v.mp4
        media_url = plugintools.find_single_match(data,'<script>var W2t=.*?(http:.*?mp4)')
        if media_url !="":
            print '$'*81+'- By PalcoTV Team -'+'$'*81,media_url,'$'*181
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
      
    plugintools.play_resolved_url(media_url)
        
def up2stream(params):
    plugintools.log('[%s %s] Up2stream.com %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        #http://up2stream.com/view.php?ref=L20vlMXyo22oyXMlv02L.php&width=100%&height=400
        page_url = page_url.replace('http://up2stream.com/','http://up2stream.com/view.php')+'.php&width=100%&height=400'
        r=requests.get(page_url)
        data=r.content
        try:
            data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
            data = wiz.unpack(data)
            #http://abi.cdn.vizplay.org/v2/21b2424f1826eedc944e1eddc3168ce6.mp4?st=o_J3dk6gSLduHjyZ4qtBCQ&hash=orl-amZyOR7ybXDOJ46XGg
            media_url = plugintools.find_single_match(data,'src","([^"]+)"')
            print '$'*53+'- By PalcoTV Team -'+'$'*53,media_url,'$'*125
            plugintools.play_resolved_url(media_url)
        except:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
                                
def smartvid(params):
    plugintools.log('[%s %s] Smartvid.Tv %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://smartvid.tv/","http://smartvid.tv/embed-")

    try: 
        r = requests.get(page_url)
        data = r.text
        sources = plugintools.find_single_match(data,"sources: \[(.*?)\],")
        media_file = plugintools.find_multiple_matches(sources,'file:"([^"]+)"')
        if sources =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
        elif media_file > 1: max_quality = media_file[-1];media_url = max_quality
        else: media_url = media_file
        print '$'*37+'- By PalcoTV Team -'+'$'*37,media_url,'$'*93
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

    plugintools.play_resolved_url(media_url)

def greevid(params):
    plugintools.log('[%s %s] Greevid.com %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        r=requests.get(page_url)
        data=r.content
        page_url = plugintools.find_single_match(data,'<iframe width="100%" height="500" frameborder="0" src="(.*?)"').split('?')
        page_url = page_url[-1]
   
        headers = {"Host": "vidzi.tv","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r=requests.get(page_url,headers=headers)
        data=r.text
        data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
        data = wiz.unpack(data)
        media = plugintools.find_multiple_matches(data,'file:"([^"]+)"')
        if media =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
        else:
            for item in media:
                try:
                    if "mp4" in item:
                            media_url = item.replace('\/','/')  
                            print '$'*35+'- By PalcoTV Team -'+'$'*35,media_url,'$'*89
                except:
                    if "m3u8" in item:
                        media_url = item.replace('\/','/')  
                        print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95                              
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
    plugintools.play_resolved_url(media_url)

def letwatch(params):
    plugintools.log('[%s %s] Letwatch.us %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("http://letwatch.us/","http://letwatch.us/embed-")+'.html'   
    try:
        r = requests.get(page_url)
        data = r.content
        sources = plugintools.find_single_match(data,'sources: \[\{file:"(.*?)"')
        if sources =="":
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
        else: media_url = sources
        print '$'*35+'- By PalcoTV Team -'+'$'*35,media_url,'$'*89 
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
        
    plugintools.play_resolved_url(media_url)

def yourupload(params):
    plugintools.log('[%s %s] Yourupload.com %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    if not "embed" in page_url:
        page_url = page_url.replace("/watch/","/embed/")   
    try:
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r = requests.get(page_url)
        data = r.content
        source = plugintools.find_single_match(data,"file: '(.*?)'")
        #http://cdn.oose.io/8Q35CHT5RSNP0Gi26M8c7N52ECSA87hvPNPO70GqapTb1wUum6gx4ny10J6lrkgG/video.mp4
        if source:
            headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
            "Referer":"http://www.yourupload.com/jwplayer/jwplayer.flash.swf"}
            r = requests.get(source,headers=headers,allow_redirects=False)
            data = r.headers
            media_url = data['Location']
            media_url = media_url.replace('?null&start=0','')
            print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95
            plugintools.play_resolved_url(media_url)       
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))          
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
         
def zalaa(params):
    plugintools.log('[%s %s] Zalaa.com %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
      
    if not "embed" in page_url:
        id_vid = plugintools.find_single_match(page_url,'zalaa.com/(.*?)/')
        page_url = 'http://www.zalaa.com/embed-'+id_vid+'.html'
    try:
        headers = {"Host": "www.zalaa.com","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r=requests.get(page_url,headers=headers)
        data=r.content
        media = plugintools.find_single_match(data,"file','([^']+)'")
        try:
            #http://ww1.zalaa.com:182/d/sigddcn5vsulzrqm5hnl5gvtbvh6qxq7qvxef5zb7zha5pqkz7tqkadc/greys.anatomy.1217.hdtv-lol.mp4?start=0
            media_url = media+'|Referer='+params.get("url")
            print '$'*87+'- By PalcoTV Team -'+'$'*87,media_url,'$'*193
            plugintools.play_resolved_url(media_url)
        except:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))                                
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
def uploadc(params):
    plugintools.log('[%s %s] Uploadc %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r=requests.get(page_url,headers=headers)
        data=r.content

        ipcount = plugintools.find_single_match(data,'id="ipcount_val" value="(.*?)"')
        idfile = plugintools.find_single_match(data,'name="id" value="(.*?)"')
        fname = plugintools.find_single_match(data,'name="fname" value="(.*?)"')
        post = {'ipcount_val': ipcount,'usr_login': '','id': idfile,'fname': fname,'referer': '','method_free':'Continue', 'op':'download22'}
        end_url = plugintools.find_single_match(data,'id="frmdownload" action="(.*?)"')
        #http://www.uploadc.com/4m5s0t4e3sr8?p=1
        url = page_url+end_url
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Referer": page_url} 
        r=requests.post(url,headers=headers,data=post)
        data=r.content
        media = plugintools.find_single_match(data,"file'\,'([^']+)'") 
        try:
            media_url = media+'|Referer='+params.get("url")
            print '$'*71+'- By PalcoTV Team -'+'$'*71,media_url,'$'*161
            plugintools.play_resolved_url(media_url)
        except: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))                             
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
def mp4upload(params):
    plugintools.log('[%s %s] Uploadc %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
      
    if not "embed" in page_url:
        page_url = page_url.replace("http://www.mp4upload.com/","http://www.mp4upload.com/embed-")+'.html'
    try:
        headers = {"Host": "www.mp4upload.com","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
        r=requests.get(page_url,headers=headers)
        data=r.content
        #http://www8.mp4upload.com:182/d/rwxt7m2pz3b4quuorkubypckiujjgfp63lucunp2gbkiiq2auoezqg3a/video.mp4
        media = plugintools.find_multiple_matches(data,'file": "([^"]+)"') 
        try:
            media_url = media[0]+'|Referer='+params.get("url")
            print '$'*68+'- By PalcoTV Team -'+'$'*68,media_url,'$'*155
            plugintools.play_resolved_url(media_url)
        except: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))                                    
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
def rapidvideo(params):
    plugintools.log('[%s %s] RapidVideo %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            page_url = page_url.replace("http://rapidvideo.ws/","http://rapidvideo.ws/embed-") + '.html'
        r = requests.get(page_url)
        data = r.content
        try:
            data_eval = plugintools.find_single_match(data,"<script type='text/javascript'>eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
            data_packed  = wiz.unpack(data_eval)
            n_files = plugintools.find_multiple_matches(data_packed,'file:"([^"]+)"')
            if len(n_files)>1: media_url = n_files[0]
            else: media_url = plugintools.find_single_match(data_packed,'file:"([^"]+)"')
            print '$'*35+'- By PalcoTV Team -'+'$'*35,media_url,'$'*89
            plugintools.play_resolved_url(media_url)
        except: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def yourvideohost(params):
    plugintools.log('[%s %s] YourVidoeHost %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")

    #if not "embed" in page_url:
        #page_url = page_url.replace("http://yourvideohost.com/","http://yourvideohost.com/embed-") + '.html'
    try:
        headers ={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0","Referer": page_url}
        r = requests.get(page_url,headers=headers)
        data = r.content
        post_url = plugintools.find_single_match(data,"<Form method=\"POST\" action='(.*?)'")
        post_op = plugintools.find_single_match(data,'name="op" value="(.*?)"') 
        post_id = plugintools.find_single_match(data,'name="id" value="(.*?)"') 
        post_fname = plugintools.find_single_match(data,'name="fname" value="(.*?)"')
        post_hash = plugintools.find_single_match(data,'name="hash" value="(.*?)"')
        post = {'op': post_op, 'usr_login': '', 'id': post_id, 'fname': post_fname, 'referer': '', 'hash': post_hash, 'imhuman': 'Proceed+to+video'}
        #post = "op="+post_op+"&usr_login="+"&id="+post_id+"&fname="+post_fname+"&referer="+"&hash="+post_hash+"&imhuman=Proceed+to+video"
        headers = {'Host':'yourvideohost.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Referer': page_url}
        print post
        r = requests.get(post_url,data=post)#,allow_redirects=False)
        data = r.content
        print data
        try:
            media_url = plugintools.find_single_match(data,'file: "([^"]+)"')
            print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95
            plugintools.play_resolved_url(media_url)
        except: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def watchers(params):
    plugintools.log('[%s %s] Watchers %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")

    if not "embed" in page_url:
        page_url = page_url.replace("http://watchers.to/","http://watchers.to/embed-") + '.html'
    try:
        r = requests.get(page_url)
        data = r.content
        try:
            data_eval = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
            data_packed  = wiz.unpack(data_eval)
            full_files = plugintools.find_single_match(data_packed,'sources:\[\{(.*?)\}\]')
            n_files = plugintools.find_multiple_matches(full_files,'file:"([^"]+)"')
            media_url = n_files[0]
            if 'm3u8' in media_url: print '$'*53+'- By PalcoTV Team -'+'$'*53,media_url,'$'*125
            elif 'mp4' in media_url: print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95 
            plugintools.play_resolved_url(media_url)   
        except: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def vidtodo(params):
    plugintools.log('[%s %s] Vidtodo.com %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")

    if not "embed" in page_url:
        page_url = page_url.replace("http://vidtodo.com/","http://vidtodo.com/embed-") + '.html'
    try:
        r = requests.get(page_url)
        data = r.content
        try:
            n_files = plugintools.find_single_match(data,'sources: \[\{(.*?)\}\]')
            sources = plugintools.find_multiple_matches(n_files,'file: "([^"]+)"')
            for item in sources:
                if 'mp4' in item: media_url = item
            else: media_url = sources[-1]
            print '$'*36+'- By PalcoTV Team -'+'$'*36,media_url,'$'*91
            plugintools.play_resolved_url(media_url)
        except: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def izanagi(params):
    plugintools.log('[%s %s] Izanagi %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14"}
        r = requests.get(page_url,headers=headers)
        data = r.content
        url_js = plugintools.find_single_match(data,"\.get\('(.*?)'")
        url_js = urllib.unquote(url_js) 
        r = requests.get(url_js,headers=headers)
        data_js = r.content
        try:
            js = json.loads(data_js)
            media_url = js["file"]
            print '$'*45+'- By PalcoTV Team -'+'$'*45,media_url,'$'*109
            plugintools.play_resolved_url(media_url)        
        except:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png')) 
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
    
def yotta(params):
    plugintools.log('[%s %s] Yotta %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14"}
        r = requests.get(page_url,headers=headers)
        data = r.content
        url_js = plugintools.find_single_match(data,"\.get\('(.*?)'")
        url_js = urllib.unquote(url_js) 
        r = requests.get(url_js,headers=headers)
        data_js = r.content
        try:
            js = json.loads(data_js)
            media_url = js["sources"][0]['file']
            print '$'*218+'- By PalcoTV Team -'+'$'*218,media_url,'$'*455
            plugintools.play_resolved_url(media_url)      
        except:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def kami(params):
    plugintools.log('[%s %s] Yotta %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14"}
        r = requests.get(page_url,headers=headers)
        data = r.content
        sources = plugintools.find_single_match(data,"sources: \[\{(.*?)\}\],")
        media_url = plugintools.find_multiple_matches(sources,'file: "([^"]+)"')
        try:
            media_url = media_url[0] 
            print '$'*43+'- By PalcoTV Team -'+'$'*43,media_url,'$'*105
            plugintools.play_resolved_url(media_url)    
        except:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url
       
def touchfile(params):
    plugintools.log('[%s %s] Touchfile.tv %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            id_vid = plugintools.find_single_match(page_url,'http://touchfile.tv/(.*?)/')
            page_url = 'http://bestream.tv/plugins/mediaplayer/site/_embed_touchfile.php?u='+id_vid
            #file: "http://bs131b1.bestream.tv/4Xav/file.webm?hash=9c2d02cdbf7ab9abf822834d84c9143c&time=1468663470&download_token=d0beec289188c131647ed6fbefc6c61435e90d05cf4966f35b41d682fd4eafbf",
        r = requests.get(page_url)
        data = r.text
        media_url = plugintools.find_single_match(data,'file: "([^"]+)"')
        if media_url !="":
            print '$'*80+'- By PalcoTV Team -'+'$'*80,media_url,'$'*179 
            plugintools.play_resolved_url(media_url)  
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def zstream(params):
    plugintools.log('[%s %s] Zstream.to %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            page_url = page_url.replace("http://zstream.to/","http://zstream.to/embed-") + ".html"
   
        r = requests.get(page_url)
        data = r.content
        media_url = plugintools.find_single_match(data,'file:"([^"]+)"')
        if media_url !="":
            print '$'*35+'- By PalcoTV Team -'+'$'*35,media_url,'$'*89
            plugintools.play_resolved_url(media_url)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url       
    
def vodlock(params):
    plugintools.log('[%s %s] Vodlock.co %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            page_url = page_url.replace("http://vodlock.co/","http://vodlock.co/embed-")
        if not 'html' in page_url: page_url = page_url+'.html'
        r = requests.get(page_url)
        data = r.content
        media_url = plugintools.find_single_match(data,'file:"([^"]+)"')
        if media_url !="":
            print '$'*35+'- By PalcoTV Team -'+'$'*35,media_url,'$'*89
            plugintools.play_resolved_url(media_url)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url       
    
def goodvideohost(params):
    plugintools.log('[%s %s] Goodvideohost.com %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            page_url = page_url.replace("http://goodvideohost.com/","http://goodvideohost.com/embed-") + '.html'
        r = requests.get(page_url)
        data = r.content
        media_url = plugintools.find_single_match(data,'file:"([^"]+)"')
        if media_url !="":
            print '$'*35+'- By PalcoTV Team -'+'$'*35,media_url,'$'*89
            plugintools.play_resolved_url(media_url)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url       
    
def happystreams(params):
    plugintools.log('[%s %s] Happystreams.net %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        r = requests.get(page_url)
        data = r.content
        post_url = plugintools.find_single_match(data,"<Form method=\"POST\" action='(.*?)'")
        post_op = plugintools.find_single_match(data,'name="op" value="(.*?)"') 
        post_id = plugintools.find_single_match(data,'name="id" value="(.*?)"') 
        post_fname = plugintools.find_single_match(data,'name="fname" value="(.*?)"')
        post_hash = plugintools.find_single_match(data,'name="hash" value="(.*?)"')
        post = {'op': post_op, 'usr_login': '', 'id': post_id, 'fname': post_fname, 'referer': '', 'hash': post_hash, 'imhuman': 'Proceed+to+video'} 
        headers = {'Host': 'happystreams.net','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Referer': page_url}
        r = requests.post(post_url,data=post)
        data = r.text
        data = plugintools.find_single_match(data,"eval\(function\(p,a,c,k,e,d\)(.*?)</script>")
        data = wiz.unpack(data)
        media_url = plugintools.find_single_match(data,'file:"([^"]+)"')
        if media_url !="":
            print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95
            plugintools.play_resolved_url(media_url)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def speedvideo(params):
    plugintools.log('[%s %s] SpeedVideo.net %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            page_url = page_url.replace('http://speedvideo.net/','http://speedvideo.net/embed-')+'.html'
        r = requests.get(page_url)
        data = r.content
        ##################### Copyright (C) 2014 TheHighway and tknorris ###################
        a = re.compile('var\s+linkfile *= *"(.+?)"').findall(data)[0]
        b = re.compile('var\s+linkfile *= *base64_decode\(.+?\s+(.+?)\)').findall(data)[0]
        c = re.compile('var\s+%s *= *(\d*)' % b).findall(data)[0]
        stream_url = a[:int(c)] + a[(int(c) + 10):]
        media_url = base64.b64decode(stream_url)
        ####################################################################################
        if media_url !="":
            print '$'*40+'- By PalcoTV Team -'+'$'*40,media_url,'$'*99
            plugintools.play_resolved_url(media_url)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def vidbull(params):
    plugintools.log('[%s %s] Vidbull %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        result = client.request(page_url, mobile=True)
        media_url = client.parseDOM(result, 'source', ret='src', attrs = {'type': 'video.+?'})[0]
        if media_url !="":
            print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95
            plugintools.play_resolved_url(media_url)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def filehoot(params):
    plugintools.log('[%s %s] Filehoot %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        id_vid = plugintools.find_single_match(page_url,'http://www.filehoot.com/([a-zA-Z0-9]+)')
        page_url = "http://filehoot.com/embed-"+id_vid+"-1046x562.html"
        r = requests.get(page_url)
        data = r.content
        media_url = plugintools.find_single_match(data,'file: "([^"]+)"')
        if media_url !="":
            print '$'*38+'- By PalcoTV Team -'+'$'*38,media_url,'$'*95
            plugintools.play_resolved_url(media_url)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

def thevideos(params):
    plugintools.log('[%s %s] Thevideos %s' % (addonName, addonVersion, repr(params)))

    page_url = params.get("url")
    try:
        if not "embed" in page_url:
            page_url = page_url.replace("http://thevideos.tv/","http://thevideos.tv/embed-")+".html"
        r = requests.get(page_url)
        data = r.content
        bloq_sources = plugintools.find_single_match(data,'sources: \[\{(.*?)\}\]')
        sources = plugintools.find_multiple_matches(bloq_sources,'file:"(.*?)",label:"(.*?)"')
        if len(sources) >1:
                options = []
                for item in sources:
                    opct = '[COLORlightyellow]Ver en Calidad '+item[1]+'[/COLOR]'
                    options.append(opct)
                select_option = plugintools.selector(options,'PalcoTV **TheVideos**')
                ######### Evitamos el error de cancelacion con valor -1 ########
                if select_option >=0:  
                    i = select_option
                    media_url = sources[i][0]
                    print '$'*35+'- By PalcoTV Team -'+'$'*35,media_url,'$'*89
                    plugintools.play_resolved_url(media_url)
                else: pass
                ################################################################
        elif len(sources) ==1:
            media_url = 'http:'+sources[0][0]
            print '$'*35+'- By PalcoTV Team -'+'$'*35,media_url,'$'*89
            plugintools.play_resolved_url(media_url)
    except:
        media_url=urlr(page_url)
        print 'URLR',media_url

##################################### OPENLOAD ############################################
############################## Copyright (C) 2015 tknorris ################################

def openload(params):
    plugintools.log('[%s %s] Openload %s' % (addonName, addonVersion, repr(params)))
    page_url = params.get("url")
    
    if '/f/' in page_url:
        #https://openload.co/f/zJZ9sxx7zB8/AnatGr3y.s12e20HDiTunes.YK.avi
        page_embed = plugintools.find_single_match(page_url,'(https://openload.co/f/.*?/)')
        page_url = page_embed.replace('/f/','/embed/')
        #https://openload.co/embed/zJZ9sxx7zB8/
    r = requests.get(page_url)
    data = r.content
    if 'We are sorry!' in data:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Archivo no disponible", 3 , art+'icon.png'))
    else:
        from HTMLParser import HTMLParser
        magic_number = 2
        enc_data=''
        n = re.findall('<span id="(.*?)">(.*?)</span>', data)
        for index, item in enumerate(n):
            print index
            print item
            '''
            if 'hiddenurl' in item:
                enc_data=n[index+1][1]
                print enc_data
            '''
        print  n
        enc_data = n[0][1]
        enc_data = HTMLParser().unescape(enc_data)
        res = []
        for c in enc_data:
            j = ord(c)
            if j >= 33 and j <= 126:
                j = ((j + 14) % 94) + 33
            res += chr(j)
        mynum = magic_number
        res = res[:-1] + [chr(ord(res[-1])+int(mynum))]
        #print "",res
        videoUrl = 'https://openload.co/stream/{0}?mime=true'.format(''.join(res))
        dtext = videoUrl.replace('https', 'http')
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        req = urllib2.Request(dtext, None, headers)
        res = urllib2.urlopen(req)
        media_url = res.geturl()
        res.close()
        print '$'*56+'- By PalcoTV Team -'+'$'*56,media_url,'$'*131
        plugintools.play_resolved_url(media_url)

###########################################################################################




