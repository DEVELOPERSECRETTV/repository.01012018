# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de Ivoox.com para PalcoTV
# Version 0.1 (31.01.2016)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)
#------------------------------------------------------------

import os
import sys
import urllib
import urllib2
import re

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools
import requests

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

art = addonPath + "/art/"
temp = xbmc.translatePath(os.path.join('special://home/userdata/playlists/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/userdata/playlists', ''))

thumbnail = 'https://www.cubbyusercontent.com/pl/dmrbvZOM.jpeg/_abb9cea697fa4317bed15895009bb91d'
fanart = 'https://www.cubbyusercontent.com/pl/Podcast1.jpg/_e50737800d444c48bccfb877f3f90166'

# Logos Categoria ---------------------------->>
logo_AlaCarta = 'https://www.cubbyusercontent.com/pl/Logo_AlaCarta.png/_99736fffc5f84995bdb08aac8a017505';logo_HC = 'https://www.cubbyusercontent.com/pl/HC.png/_8436de4186294abb9569eb79b23e3a84';logo_Deporte = 'https://www.cubbyusercontent.com/pl/Logo-Deportes.png/_4d681471556546f8a39a6d3acdb86bd6';logo_CC = 'https://www.cubbyusercontent.com/pl/ciencia-cultura_Logo.jpg/_12790dfe28304c4f87806521c9ef77c9';logo_Ocio = 'https://www.cubbyusercontent.com/pl/Logo_Ocio.png/_42139c43c4ee44f28eea765da28a1380';logo_Radio = 'https://www.cubbyusercontent.com/pl/Radio-en-linea_Logo.png/_548b938eddd94c0b9e3a555b869e8637'
logo_AS = 'https://www.cubbyusercontent.com/pl/Actualidad_sociedad_Logo.png/_fe054525ad9d4833ad496780ab3908fe';logo_Musica = 'https://www.cubbyusercontent.com/pl/Logo_Musica.png/_a38a75bec20b485091b86a31b0318ba0';logo_BF = 'https://www.cubbyusercontent.com/pl/Bienestar_Familia_Logo.png/_640f266c37874ab1a1ba8e82dfcc0fa4';logo_ET = 'https://www.cubbyusercontent.com/pl/empresas_tecnologia_Logo.png/_bdd47d242cde4b2799052e5d3339dde3';logo_AudioLibros = 'https://www.cubbyusercontent.com/pl/audiolibros_Logo.png/_5b1a50b83dd5454d9b3ff33d32841463'

# Fondos Categoria ---------------------------->>
fanart_HC = 'https://www.cubbyusercontent.com/pl/Fondo_Historias_Creencias.png/_64a9fc42e10741bbb7066369482fab99';fanart_Deporte = 'https://www.cubbyusercontent.com/pl/Fondo_Deportes.png/_f794a585c4e24e46b7d989f790859381';fanar_CC = 'https://www.cubbyusercontent.com/pl/Fondo_Ciencia_Cultura.png/_704cfa7d028f49869c6eebf338e54c2f';fanart_Ocio = 'https://www.cubbyusercontent.com/pl/Fondo_Ocio.png/_7621ee4396d343bd90c8e945286722b4';fanart_Radio = 'https://www.cubbyusercontent.com/pl/Fondo_radio.png/_bae63cfe7a3b45f79ba5c7f119b1e274'
fanart_AS = 'https://www.cubbyusercontent.com/pl/Fondo_Actualidad_Sociedad.png/_562a0563668d468bb1837e85739f2950';fanart_Musica = 'https://www.cubbyusercontent.com/pl/Fondo_Musica.png/_cdadbddcfc2d4288a54406d682d2aca9';fanart_BF = 'https://www.cubbyusercontent.com/pl/Fondo_Bienestar_Familia.png/_fa1e4edecd9747df85197fb75f181c02';fanart_ET = 'https://www.cubbyusercontent.com/pl/Fondo_Empresas_tecnologia.png/_6b3f7ebea4134a0c9a8c59e1bc0c3226';fanart_AudioLibros = 'https://www.cubbyusercontent.com/pl/Fondo_AudioLibros.png/_223fb11f60114b0094efafb7e1613c65'
# Colores Parser ------------------------------>>
sc = "[COLOR white]";ec = "[/COLOR]"
sc1 = "[COLOR red][I]";ec1 = "[/I][/COLOR]"
sc2 = "[COLOR yellowgreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR sienna]";ec3 = "[/COLOR]"
sc4 = "[COLOR palegreen]";ec4 = "[/COLOR]"
sc5 = "[COLOR blue][I]";ec5 = "[/I][/COLOR]"
version = " [0.2]"

web = "http://www.ivoox.com/"
ref = "http://www.ivoox.com/"

def ivoox0(params):
    plugintools.log("[%s %s] Ivoox Parser... %s " % (addonName, addonVersion, repr(params)))

    name = 'Ivoox.com'
    update = '19/04/2016 21:00'
    Autor = 'V1k1ng0'
    url = 'https://www.cubbyusercontent.com/pl/ivoox.py/_9d46d7480ad7445286f1b6499a994b82'
    r = requests.get(web)
    data = r.content
    #print data
    infolabels = {}
    
# Secciones Home ------------------------------>>

    titulo =' '*21+ "[COLOR sienna][B]-IVOOX-[/B][/COLOR][COLOR red][I] "+version+"[/I][/COLOR]"
    infolabels["plot"] = sc5 +  "· Autor del Parser: V1k1ng0 · · Autor del Regex: Aquilesserr · " + ec5
    plugintools.add_item(action="",url="",title=titulo,thumbnail=thumbnail,info_labels=infolabels,fanart=fanart,folder=False,isPlayable=False)    
    plugintools.add_item(action="",url="",title="",thumbnail='https://www.cubbyusercontent.com/pl/LogoParser.png/_a6d13ccdcbce474eb2afb9707a01d78c',fanart=fanart,folder=False,isPlayable=False)
    plugintools.addDir(action="ivoox_search",url="http://www.ivoox.com/podcast_sc_f443.67_1.html",title='[COLOR lightyellow][B]Buscar podcast...[/B][/COLOR]',thumbnail=logo_AudioLibros,fanart=fanart_AudioLibros,folder=True,isPlayable=False)
    plugintools.addDir(action="Secciones_Ivoox",url="http://www.ivoox.com/audios_sa_f_1.html",title=sc + "· A La Carta ·" + ec + sc1 +  "[Podcast]" + ec1,thumbnail=logo_AlaCarta,fanart=fanart,folder=True,isPlayable=False)
    plugintools.addDir(action="Secciones_Ivoox",url="http://www.ivoox.com/audios-historia-creencias_sa_f31_1.html",title=sc + "· Historias y Creencias ·" + ec + sc1 +  "[Podcast]" + ec1,thumbnail=logo_HC,fanart=fanart_HC,folder=True,isPlayable=False)
    plugintools.addDir(action="Secciones_Ivoox",url="http://www.ivoox.com/audios-deporte_sa_f33_1.html",title=sc + "· Deporte ·" + ec + sc1 +  "[Podcast]" + ec1,thumbnail=logo_Deporte,fanart=fanart_Deporte,folder=True,isPlayable=False)
    plugintools.addDir(action="Secciones_Ivoox",url="http://www.ivoox.com/audios-ciencia-cultura_sa_f36_1.html",title=sc + "· Ciencia y Cultura ·" + ec + sc1 +  "[Podcast]" + ec1,thumbnail=logo_CC,fanart=fanar_CC,folder=True,isPlayable=False)  
    plugintools.addDir(action="Secciones_Ivoox",url="http://www.ivoox.com/audios-ocio_sa_f35_1.html",title=sc + "· Ocio ·" + ec + sc1 +  "[Podcast]" + ec1,thumbnail=logo_Ocio,fanart=fanart_Ocio,folder=True,isPlayable=False)
    plugintools.addDir(action="Secciones_Ivoox",url="http://www.ivoox.com/escuchar-radio-online_sr_f_1.html",title=sc + "· Radio On-Line ·" + ec + sc1 +  "[Radios Online]" + ec1,thumbnail=logo_Radio,fanart=fanart_Radio,folder=True,isPlayable=False)
    plugintools.addDir(action="Secciones_Ivoox",url="http://www.ivoox.com/audios-actualidad-sociedad_sa_f37_1.html",title=sc + "· Actualidad y Sociedad ·" + ec + sc1 +  "[Podcast]" + ec1,thumbnail=logo_AS,fanart=fanart_AS,folder=True,isPlayable=False)    
    plugintools.addDir(action="Secciones_Ivoox",url="http://www.ivoox.com/audios-musica_sa_f311_1.html",title=sc + "· Música ·" + ec + sc1 +  "[Podcast]" + ec1,thumbnail=logo_Musica,fanart=fanart_Musica,folder=True,isPlayable=False)
    plugintools.addDir(action="Secciones_Ivoox",url="http://www.ivoox.com/audios-bienestar-familia_sa_f39_1.html",title=sc + "· Bienestar y Familia ·" + ec + sc1 +  "[Podcast]" + ec1,thumbnail=logo_BF,fanart=fanart_BF,folder=True,isPlayable=False)
    plugintools.addDir(action="Secciones_Ivoox",url="http://www.ivoox.com/audios-empresa-tecnologia_sa_f38_1.html",title=sc + "· Empresas y Tecnologia ·" + ec + sc1 +  "[Podcast]" + ec1,thumbnail=logo_ET,fanart=fanart_ET,folder=True,isPlayable=False)
    plugintools.addDir(action="Secciones_Ivoox",url="http://www.ivoox.com/podcast_sc_f443.67_1.html",title=sc + "· Audio Libros ·" + ec + sc1 +  "[Podcast]" + ec1,thumbnail=logo_AudioLibros,fanart=fanart_AudioLibros,folder=True,isPlayable=False)
    
    
# Global Secciones ------------------------------>>
    
def Secciones_Ivoox(params):#Esta funcion me vale para casi todas las secciones
    plugintools.log("[%s %s] Ivoox Parser... %s " % (addonName, addonVersion, repr(params)))
    titulo =' '*21+ "[COLOR sienna][B]-IVOOX-[/B][/COLOR][COLOR red][I] "+version+"[/I][/COLOR]"
    infolabels = {}

    fanart_secc = params.get("fanart")
    if fanart_secc == "":
        fanart_secc = 'http://www.elandroidelibre.com/wp-content/uploads/2012/07/ivoox-splash.jpg'
    thumbnail = params.get("thumbnail")
    if thumbnail == "":
        thumbnail = "https://www.cubbyusercontent.com/pl/dmrbvZOM.jpeg/_abb9cea697fa4317bed15895009bb91d"
    logo_secc = params.get("thumbnail")    

    infolabels["plot"] = sc5 +  "· Autor del Parser: V1k1ng0 · · Autor del Regex: Aquilesserr · " + ec5
    plugintools.add_item(action="",url="",title=titulo,info_labels=infolabels,thumbnail='https://www.cubbyusercontent.com/pl/dmrbvZOM.jpeg/_abb9cea697fa4317bed15895009bb91d',fanart='https://www.cubbyusercontent.com/pl/Podcast1.jpg/_e50737800d444c48bccfb877f3f90166',folder=False,isPlayable=False)
    plugintools.add_item(action="",url="",title="",thumbnail='https://www.cubbyusercontent.com/pl/LogoParser.png/_a6d13ccdcbce474eb2afb9707a01d78c',fanart='https://www.cubbyusercontent.com/pl/Podcast1.jpg/_e50737800d444c48bccfb877f3f90166',folder=False,isPlayable=False)
    
    headers = {"Host": "www.ivoox.com","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
    "Referer": ref}
    url = params.get("url")
    r = requests.get(url,headers=headers)
    data = r.content
    #print data
    
    bloque_podcast = plugintools.find_single_match(data,'<div class="wrapper-modulo-lista">(.*?)<footer>')
    
    if 'ESCUCHAR RADIO' in bloque_podcast:
        podcast = plugintools.find_multiple_matches(bloque_podcast,'<div class="flip-container">(.*?)<span>ESCUCHAR RADIO</span>')
    else:
        podcast = plugintools.find_multiple_matches(bloque_podcast,'<div class="flip-container">(.*?)</ul>')

    for item in podcast:

        if 'ESCUCHAR RADIO' in bloque_podcast:
            title = plugintools.find_single_match(item,'<div class="header-modulo">\s+<a href=".*?title="([^"]+)"').replace("&quot;","").replace("#","")
            #logo = params.get("thumbnail")
            #if logo == "" or logo.endswith("icon.png") == True:
            logo = plugintools.find_single_match(item,'<img src="(.*?)"')
            url = plugintools.find_single_match(item,'<div class="header-modulo">\s+<a href="([^"]+)"')
            mode_rad = plugintools.find_single_match(item,'<strong>(.*?)</strong>').strip()
            episfull = sc4+mode_rad+ec4+sc1+" -   Escuchar Emisora >>"+ec1
 
            plugintools.add_item(action="",url="",title=sc3+"[B]"+title+"[/B]"+ec3,thumbnail=logo,fanart=fanart_secc,folder=False,isPlayable=False)
            plugintools.addShow(action="ivoox_regex",url=url,title=episfull,thumbnail=logo,fanart=fanart_secc,folder=False,isPlayable=True)
            plugintools.add_item(action="",url=url,title="",thumbnail=logo,fanart=fanart_secc,folder=False,isPlayable=False)
            
        elif 'IR AL PROGRAMA' in bloque_podcast:
            title = plugintools.find_single_match(item,'<div class="header-modulo">\s+<a href=".*?title="([^"]+)"').replace("&quot;","").replace("#","")
            #logo = params.get("thumbnail")
            #if logo == "" or logo.endswith("icon.png") == True:
            logo = plugintools.find_single_match(item,'<img src="(.*?)"')
            url = plugintools.find_single_match(item,'<div class="header-modulo">\s+<a href="([^"]+)"')
            mode_prog = plugintools.find_single_match(item,'<strong>(.*?)</strong>').strip()
            episfull = sc4+mode_prog+ec4+sc1+" -   Ir A Programa >>"+ec1
            desc = plugintools.find_single_match(item,'<meta itemprop="description" content="(.*?)"/>').strip().replace("\n","").replace("\t","")  
            aud = plugintools.find_single_match(item,'Audios">(.*?)</a></li>')
            infofull = sc+"Descripción: "+desc +" - Audios: " +aud+ec

            infolabels["plot"]=infofull            
            plugintools.add_item(action="ivoox_audiolibro_secc",url="",title=sc3+"[B]"+title+"[/B]"+ec3,thumbnail=logo,info_labels=infolabels,fanart=fanart_secc,folder=True,isPlayable=False)

            if 'podcast_sc_f443.67_1.html' in params.get("url"):
                plugintools.add_item(action="ivoox_audiolibro_secc",url=url,info_labels=infolabels,title=episfull,thumbnail=logo,fanart=fanart_secc,folder=True,isPlayable=False) 
            else:
                plugintools.add_item(action="ivoox_audiolibro_secc",url=url,info_labels=infolabels,title=episfull,thumbnail=logo,fanart=fanart_secc,folder=True,isPlayable=False)
            plugintools.add_item(action="",url=url,title="",thumbnail=logo,fanart=fanart_secc,folder=False,isPlayable=False)
        
        else:
            title = plugintools.find_single_match(item,'<div class="header-modulo">\s+<a href=".*?title="([^"]+)"').replace("&quot;","").replace("#","")
            logo = params.get("thumbnail")
            if logo == "" or logo.endswith("icon.png") == True:
                logo = plugintools.find_single_match(item,'<img src="(.*?)"')
            url = plugintools.find_single_match(item,'<div class="header-modulo">\s+<a href="([^"]+)"')
            epis = plugintools.find_single_match(item,'<strong>\s+(.*?)</strong>').strip().replace("\n","").replace("\t","")
        
            gen = plugintools.find_single_match(item,'<p class="time">.*?<a class="rounded-label.*?">\s+(.*?)</a>').strip().replace("\n","").replace("\t","")
            durac = plugintools.find_single_match(item,'<p class="time">([^<]+)<')
            episfull = sc4+"Episodio en "+epis+ec4+sc2+" -   Escuchar Podcast >>"+ec2
            infofull = sc+"Género: "+gen +" - Duración: " +durac+ec
            url = plugintools.find_single_match(item,'<div class="header-modulo">\s+<a href="([^"]+)"')

            infolabels["plot"]=infofull
            plugintools.addShow(action="ivoox_regex",title='[COLOR white]'+title+'[/COLOR]',url=url,info_labels=infolabels,thumbnail=logo,fanart=fanart_secc,folder=False,isPlayable=True)
             
# Paginación ------------------------>>            


    bloque_paginacion = plugintools.find_single_match(data, '<ul class="pagination">(.*?)</ul>')
    if bloque_paginacion !="":
   
       pag_actual = plugintools.find_single_match(bloque_paginacion,'<a href="#" class="disabled">\s+(.*?)\s+</a>').strip().replace("\n","").replace("\t","")

       if int(pag_actual) > 1:
           pag_ant = int(pag_actual)-1
           url_prev = plugintools.find_single_match(bloque_paginacion,'<a rel="nofollow" href="([^"]+)"')
           plugintools.addDir(action="Secciones_Ivoox",url=url_prev,title="[COLOR blue][I]"+str(pag_ant)+" « Página anterior ·"+ec5+' '*25,thumbnail=logo,fanart=fanart_secc,folder=True,isPlayable=False)
       pag_sig = plugintools.find_single_match(bloque_paginacion,'<a href="#" class="disabled">.*?title=".*?">\s+(.*?)\s+</a>')
       if pag_sig !="":
           url_next = plugintools.find_single_match(bloque_paginacion,'<a href="#" class="disabled">.*?href="([^"]+)"')
           plugintools.addDir(action="Secciones_Ivoox",url=url_next,title=' '*25+"[COLOR blue][I]Página siguiente » "+str(pag_sig)+"[/I][/COLOR]",thumbnail=logo,fanart=fanart_secc,folder=True,isPlayable=False)

def ivoox_audiolibro_secc(params):
    plugintools.log("[%s %s] Ivoox Parser... %s " % (addonName, addonVersion, repr(params)))
    titulo = '[COLOR white][B]IVOOX[/B][/COLOR]'+version+'[COLOR blue][B]| AudioLibros |[/B][/COLOR]'
    plugintools.add_item(action="",url="",title=titulo,thumbnail=logo_AudioLibros,fanart=fanart_AudioLibros,folder=False,isPlayable=False)
    infolabels = {}

    fanart_secc = params.get("fanart")
    if fanart_secc == "":
        fanart_secc = 'http://www.elandroidelibre.com/wp-content/uploads/2012/07/ivoox-splash.jpg'
    thumbnail = params.get("thumbnail")
    if thumbnail == "":
        thumbnail = "https://www.cubbyusercontent.com/pl/dmrbvZOM.jpeg/_abb9cea697fa4317bed15895009bb91d"
    logo = params.get("thumbnail")
    headers = {"Host": "www.ivoox.com","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"}

    url = params.get("url")
    r=requests.get(url, headers=headers)
    data = r.content
    
    bloque_podcast = plugintools.find_single_match(data,'<div class="wrapper-modulo-lista">(.*?)<footer>')
    podcast = plugintools.find_multiple_matches(bloque_podcast,'<div class="flipper">(.*?)<!-- END Parche -->')
    #print podcast
    
    for item in podcast:    
     title = plugintools.find_single_match(item,'<meta itemprop="name" content="(.*?)"/>').replace("&quot;","").replace("#","")
     logo = plugintools.find_single_match(item,'<img src="(.*?)"')
     url = plugintools.find_single_match(item,'<meta itemprop="url" content="(.*?)"/>')
     mode_prog = plugintools.find_single_match(item,'<span>(.*?)</span>').strip()
     episfull = sc4+mode_prog+ec4+sc1+" -   Reproducir AudioLibro >>"+ec1
     desc = plugintools.find_single_match(item,'<meta itemprop="description" content="(.*?)"/>').strip().replace("\n","").replace("\t","").replace("&quot;","")  
     dur = plugintools.find_single_match(item,'<p class="time">(.*?)</p>')
     infofull = sc+"Descripción: "+desc +" - Duración: " +dur+ec

     infolabels["plot"]=infofull            
     plugintools.addShow(action="audiolibro_regex",url=url,info_labels=infolabels,title=sc3+"[B]"+title+"[/B]"+ec3,thumbnail=logo,fanart=fanart_secc,folder=False,isPlayable=True)

# Paginación ------------------------>>            


    bloque_paginacion = plugintools.find_single_match(data, '<ul class="pagination">(.*?)</ul>')
    if bloque_paginacion !="":
   
       pag_actual = plugintools.find_single_match(bloque_paginacion,'<a href="#" class="disabled">\s+(.*?)\s+</a>').strip().replace("\n","").replace("\t","")

       if int(pag_actual) > 1:
           pag_ant = int(pag_actual)-1
           url_prev = plugintools.find_single_match(bloque_paginacion,'<a rel="nofollow" href="([^"]+)"')
           plugintools.addDir(action="ivoox_audiolibro_secc",url=url_prev,title="[COLOR blue][I]"+str(pag_ant)+" « Página anterior ·"+ec5+' '*25,thumbnail=logo,fanart=fanart_secc,folder=True,isPlayable=False)
       pag_sig = plugintools.find_single_match(bloque_paginacion,'<a href="#" class="disabled">.*?title=".*?">\s+(.*?)\s+</a>')
       if pag_sig !="":
           url_next = plugintools.find_single_match(bloque_paginacion,'<a href="#" class="disabled">.*?href="([^"]+)"')
           plugintools.addDir(action="ivoox_audiolibro_secc",url=url_next,title=' '*25+"[COLOR blue][I]Página siguiente » "+str(pag_sig)+"[/I][/COLOR]",thumbnail=logo,fanart=fanart_secc,folder=True,isPlayable=False)




                       
# Regex ------------------------------>>
        
def ivoox_regex(params):
    plugintools.log("[%s %s] Ivoox Parser... %s " % (addonName, addonVersion, repr(params)))

    headers = {"Host": "www.ivoox.com","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
    "Referer": "http://www.ivoox.com/audios_sa_f_1.html"}

    url = params.get("url")
    r=requests.get(url, headers=headers)
    data = r.content
    
    paramet = plugintools.find_single_match(data,"function getmail.*?load\('([^']+)'\)")

    if paramet == "":
        media_url = plugintools.find_single_match(data,"m4a:.*?'([^']+)'")
        if media_url == "":
            media_url = plugintools.find_single_match(data,'flashvars.stream.*?"([^"]+)"')     
    else:
        new_url = 'http://www.ivoox.com/'+paramet
        #http://www.ivoox.com/downloadlink_mm_10268848_57_b_1.html?tpl2=ok
        headers = {"Host": "www.ivoox.com","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
        "Referer": url}
        r=requests.get(new_url, headers=headers)
        data = r.content     
        media_url = plugintools.find_single_match(data,'<div class="text-center">\s+<a href="([^"]+)"').replace('%3D','=')   
    
    if media_url == "":
        plugintools.log("Archivo borrado: "+url)
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "El Archivo no esta disponible", 3 , art+'icon.png'))

    print '$'*50 + '- By Vikingo -'+'&'*50,media_url,'$'*114     
    plugintools.play_resolved_url(media_url)

def audiolibro_regex(params):
    plugintools.log('[%s %s] Audio Libro Ivoox %s' % (addonName, addonVersion, repr(params)))
    
    page_url = params.get("url")
    r = requests.get(page_url)
    data = r.content
    
    id_file = plugintools.find_single_match(page_url,'http://www.ivoox.com/.*?rf_(.*?)_')
    media_url = 'http://files.ivoox.com/listen/'+id_file
    plugintools.play_resolved_url(media_url)

def ivoox_search(params):
    texto="";texto = plugintools.keyboard_input(texto);texto = texto.lower()
    if texto == "": errormsg = plugintools.message("PalcoTV","Por favor, introduzca el término de búsqueda")
    else:
        texto=texto.lower();texto_a=texto.replace(" ", "+").strip();texto_b=texto.replace(" ", "-").strip()
        url = 'http://www.ivoox.com/'+texto_a+'_sb.html?sb='+texto_b;params["url"]=url
        Secciones_Ivoox(params)        
    
    


# ------------------------------------------------------- By V1k1ng0 & Aquilesserr PalcoTv Team---------------------------------------------------
