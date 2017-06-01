# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Linker Pordede para PalcoTV
# Version 0.3 (02/09/2016)
# Autor By Aquilesserr ___ *** ___ aquilesserr@gmail.com
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Librerías Plugintools por Jesús (www.mimediacenter.info)

import urlparse,urllib2,urllib,re
import os, sys

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools, requests
from resources.tools.resolvers import *
from resources.tools.media_analyzer import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

thumbnail = 'https://www.cubbyusercontent.com/pl/pordede_logo.png/_848221f454af477db58b767a4511852d'
fanart = 'https://www.cubbyusercontent.com/pl/Pordede_fondo.jpg/_94ee5bb592be4af28e59aedc043dec4d'

post = "LoginForm[username]="+plugintools.get_setting("pordede_user")+"&LoginForm[password]="+plugintools.get_setting("pordede_pwd")
DEFAULT_HEADERS = []
DEFAULT_HEADERS.append( ["User-Agent","Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12"] )
DEFAULT_HEADERS.append( ["Referer","http://www.pordede.com"] )

sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR seagreen]";ec3 = "[/COLOR]"
sc4 = "[COLOR red]";ec4 = "[/COLOR]"
sc5 = "[COLOR yellowgreen]";ec5 = "[/COLOR]"
version = " [0.3]"

web = "http://www.pordede.com"
referer = "http://www.pordede.com/"

def pordede_linker0(params):
    plugintools.log("[%s %s] Linker Pordede %s" % (addonName, addonVersion, repr(params)))

    page_url = params.get("page")
    plugintools.log("URL= "+page_url)

    ############## Params Library #################
    source = params.get("extra")
    ###############################################

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

        url_list=[];option_list=[]

        #################################### Control for Linker ######################################
        if source == "linker":
            info_user = plugintools.find_single_match(body,'<div class="userinfo">(.*?)</div>')
            usuario = plugintools.find_single_match(info_user,'<div class="friendMini shadow" title="(.*?)"')
            avatar = plugintools.find_single_match(info_user,'src="(.*?)"')
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
                #url y parametros para marcar como visto (params Extra)
                parametros_ajax = 'http://www.pordede.com/ajax/mediaaction|model=peli&id='+id_ajax+'&action=status&value=3|'+page_url 
                status = plugintools.find_single_match(body,'controller.userStatus(.*?);').split(',') #marcada en la web
                #comprobado si esta marcada como vista
                if "3" in status[2]:
                    title = plugintools.find_single_match(info_vid,'<h1>(.*?)</h1>').replace("&amp;","&")#.upper()
                    titlefull = sc5+"[B]"+str(title)+"[/B]"+ec5+sc2+"[B][I] [Vista][/I][/B]"+ec2
                else:
                    titlefull = sc5+"[B]"+str(title)+"[/B]"+ec5 
            elif "serie" in page_url:
                title = plugintools.find_single_match(info_vid,'<h1>(.*?)<span class="titleStatus">').replace("&amp;","&")
                if title =="":
                    title = plugintools.find_single_match(info_vid,'<h1>(.*?)</h1>').replace("&amp;","&")
                status = plugintools.find_single_match(info_vid,'<h1>.*?<span class="titleStatus">(.*?)</span></h1>')
                if status =="": status = 'N/D'
                titlefull = sc5+"[B]"+str(title)+"[/B]"+" ("+str(status)+")"+ec5
                #except: pass
            punt = plugintools.find_single_match(bloq_fich,'<span class="puntuationValue" data-value="(.*?)"')
            year_duration = plugintools.find_single_match(bloq_fich,'<p class="info">(.*?)</p>.*?<p class="info">(.*?)</p>')
            bloq_genr = plugintools.find_single_match(body,'<h2 class="info genresTitle">Géneros</h2>(.*?)</p>')
            genrfull = plugintools.find_multiple_matches(bloq_genr,'href=".*?">([^<]+)<')
            genr = pordede_genr(genrfull)
            url_links = plugintools.find_single_match(info_vid,'<button class="defaultPopup big" href="(.*?)"')
            url_linksfull = web + url_links
            datamovie = {
            'rating': sc3+'[B]Puntuación: [/B]'+ec3+sc+str(punt)+', '+ec,
            'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
            'year': sc3+'[B]Año: [/B]'+ec3+sc+str(year_duration[0])+', '+ec,
            'duration': sc3+'[B]Duración: [/B]'+ec3+sc+str(year_duration[1])+'[CR]'+ec,
            'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
            datamovie["plot"]=datamovie["rating"]+datamovie["genre"]+datamovie["year"]+datamovie["duration"]+datamovie["sinopsis"]
            plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker Pordede"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
            plugintools.addPeli(action="",url="",title=sc2+"Usuario: "+usuario+ec2,info_labels=datamovie,thumbnail=avatar,fanart=fanart,folder=False,isPlayable=False)
            plugintools.add_item(action="",title=titlefull,plot="",url="",info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=False,isPlayable=False)
            if url_links !="":
                plugintools.add_item(action="pordede_server",url=url_linksfull,title=sc5+"Ir a los Enlaces >>"+ec5,info_labels=datamovie,thumbnail=logo,fanart=fondo,extra=parametros_ajax,folder=True,isPlayable=False)
            else:
                plugintools.add_item(action="pordede_serie",url=page_url,title=sc5+"Ir a los Episodios >>"+ec5,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=True,isPlayable=False)
        ##############################################################################################
        #################################### Control for Library #####################################
        elif source == "library":            
            url_linksfull = 'http://www.pordede.com'+plugintools.find_single_match(body,'<button class="defaultPopup big" href="(.*?)"')
            params['url']=url_linksfull;params['extra']="library"
            if "peli" in page_url:
                option_list,url_list = pordede_server(params)
                i=len(url_list);plugintools.log("i= "+str(i));j=len(option_list);plugintools.log("j= "+str(j))
        ##############################################################################################

    if params.get("extra") == "library": return option_list,url_list

def pordede_serie(params):
    plugintools.log("[%s %s] Linker Pordede %s" % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    logo = params.get("thumbnail")
    fondo = params.get("fanart")

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker Pordede"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    headers = DEFAULT_HEADERS[:]
    body,response_headers = plugintools.read_body_and_headers(url,headers=headers)

    temporada = '<div class="checkSeason"[^>]+>([^<]+)<div class="right" onclick="controller.checkSeason(.*?)\s+</div></div>'
    itemtemporadas = re.compile(temporada,re.DOTALL).findall(body)

    for nombre_temporada,bloque_episodios in itemtemporadas:
        patron  = '<span class="title defaultPopup" href="([^"]+)"><span class="number">([^<]+)</span>([^<]+)</span>(\s*</div>\s*<span[^>]*><span[^>]*>[^<]*</span><span[^>]*>[^<]*</span></span><div[^>]*><button[^>]*><span[^>]*>[^<]*</span><span[^>]*>[^<]*</span></button><div class="action([^"]*)" data-action="seen">)?'
        matches = re.compile(patron,re.DOTALL).findall(bloque_episodios)
        num_temp = nombre_temporada.replace("Temporada","").replace("Extras","Extras 0")
        plugintools.add_item(action="",url="",title=sc2+"-- "+nombre_temporada+" --"+ec2,thumbnail=logo,fanart=fondo,folder=True,isPlayable=False)
        for item in matches:
            id_ajax = plugintools.find_single_match(item[0],'/links/viewepisode/id/([0-9]*)')  #id necesario marcado como visto
            parametros_ajax = 'http://www.pordede.com/ajax/action|model=episode&id='+id_ajax+'&action=seen&value=1|'+url #url y parametros para marcar como visto (params Extra)
            visto = plugintools.find_single_match(item[3],'</button><div class="([^"]+)"')
            if 'action active' in visto:
                title = item[2]
                titlefull = sc+num_temp+"x"+item[1]+" -- "+title+ec+sc5+"[I] [Visto][/I]"+ec5
            else:
                title = item[2]
                titlefull = sc+num_temp+"x"+item[1]+" -- "+title+ec
            url = web+item[0]
            plugintools.add_item(action="pordede_server",url=url,title=sc+titlefull+ec,thumbnail=logo,fanart=fondo,extra=parametros_ajax,folder=True,isPlayable=False)
                                                         
def pordede_server(params):
    plugintools.log("[%s %s] Linker Pordede %s" % (addonName, addonVersion, repr(params)))

    url = params.get("url");source = params.get("extra")

    #################################### Control for Linker ######################################
    if not source == "library":
        parametros_ajax = params.get("extra")  #Recibe los parametros necesarios para marcar como visto (split '|')
        logo = params.get("thumbnail")
        fondo = params.get("fanart")
        plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker Pordede"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    ##############################################################################################
    #################################### Control for Library #####################################
    elif source == "library":
        url_list=[];option_list=[]
    ##############################################################################################
    
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
            #################################### Control for Linker ######################################
            if not params.get("extra") == "library":
                titlefull = sc+name_server+ec+" "+sc2+" ["+idioma+"] "+ec2+" "+sc3+"(OK: "+link_ok+") "+ec3+" "+sc4+"(KO: "+link_ko+") "+ec4+sc+"Video: "+ec+sc5+calidad_video+ec5+sc+"  Audio: "+ec+sc5+calidad_audio+ec5
                plugintools.add_item(action="pordede_checkvist",url=url_aport,title=titlefull,thumbnail=logo,fanart=fondo,extra=parametros_ajax,folder=False,isPlayable=True)
            ##############################################################################################
            #################################### Control for Library #####################################
            if source == "library":
                titlefull = '[COLOR white]'+name_server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+idioma.strip()+'] [/COLOR][COLOR lightblue]['+calidad_video+'] [/COLOR][COLOR gold][Pordede][/I][/COLOR]'
                plugintools.log("url= http://www.pordede.com"+url_aport);plugintools.log("option_list= "+titlefull)
                #params['extra']="library";params["url"]=url;url=pordede_getlink(params)  # La llamada a pordede_getlink para sacar la URL final se hace directamente en library_manager al seleccionar una opción para no ralentizar tanto la carga
                option_list.append(titlefull);url_list.append(url_aport)   
            ##############################################################################################

    if source == "library": return option_list,url_list
    
def pordede_checkvist(params):
    
    parametros_ajax = params.get("extra").split('|') #Recibe los parametros necesarios para marcar como visto (split '|')
    url_post = parametros_ajax[0]
    post = parametros_ajax[1] #El post viene montado desde la funcion
    url = parametros_ajax[2]
    #print url_post,post,url
    headers = {"Host":"www.pordede.com","User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Referer": url}
    body,response_headers = plugintools.read_body_and_headers(url_post,post=post,headers=headers) #Enviando los parametros para marcar visto
    url = params.get("url")
    title = params.get("title")
    params["url"] = url
    params["title"] = title
    pordede_getlink(params)    
         
def pordede_getlink(params):
    
    link = params.get("url");plugintools.log("link= "+link)
    title = params.get("title")
    source = params.get("extra")
    body,response_headers = plugintools.read_body_and_headers(link) #, post=post)
    goto = plugintools.find_single_match(body,'<p class="nicetry links">(.*?)target="_blank"')
    link_redirect = plugintools.find_single_match(goto,'<a href="(.*?)"')
    link_redirect = web + link_redirect
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0","Referer": link}
        body,response_headers = plugintools.read_body_and_headers(link_redirect) 
        for i in response_headers:
            if i[0]=='location': location=i[1]
        if location: print '$'*30+'- By PalcoTV Team -'+'$'*30,location,'$'*79
        url_final = location; params["url"]=url_final
        server_analyzer(params)
    except:
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PalcoTV', "Error al extraer el Conector", 3 , art+'icon.png'))

################################################# Tools for Linker ##############################################

def pordede_genr(genrfull):

    if len(genrfull) ==5: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]+', '+genrfull[4]
    elif len(genrfull) ==4: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]+', '+genrfull[3]
    elif len(genrfull) ==3: genrfull = genrfull[0]+', '+genrfull[1]+', '+genrfull[2]
    elif len(genrfull) ==2: genrfull = genrfull[0]+', '+genrfull[1]
    elif len(genrfull) ==1: genrfull = genrfull[0]
    return genrfull
     
######################################### @ By Aquilesserr PalcoTv Team #########################################


   
    
   


   
    


    
