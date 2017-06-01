# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Linker Tv-vip para PalcoTV
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

import plugintools, requests, time
from resources.tools.resolvers import *
from resources.tools.media_analyzer import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

web = "http://tv-vip.com"
referer = "http://tv-vip.com"

thumbnail = 'https://www.cubbyusercontent.com/pl/Tvvip_logo_palco.png/_d28a6ee58a744c4d96862f47cea0891f'
fanart = 'https://www.cubbyusercontent.com/pl/Tvvip_fanart_palco.jpg/_3a17847aee76411b8348b451a05e138a' 

sc = "[COLOR white]";ec = "[/COLOR]"
sc2 = "[COLOR palegreen]";ec2 = "[/COLOR]"
sc3 = "[COLOR seagreen]";ec3 = "[/COLOR]"
sc4 = "[COLOR red]";ec4 = "[/COLOR]"
sc5 = "[COLOR yellowgreen]";ec5 = "[/COLOR]"
version = " [0.3]"

def tvvip_linker0(params):
    plugintools.log("[%s %s] Linker TV-vip %s" % (addonName, addonVersion, repr(params)))

    page_url = params.get("page")
    page_url = page_url.replace('%C3%A1','á').replace('%C3%A9','é').replace('%C3%AD','í').replace('%C3%B1','ñ')
  
    if 'film' in page_url:
        params['url']=page_url
        tvvip_peli(params)
    if 'section' in page_url:
        params['url']=page_url
        tvvip_serie_temp(params)
    
# Peliculas -------------------------->>

def tvvip_peli(params):
    plugintools.log("[%s %s] Linker TV-vip %s" % (addonName, addonVersion, repr(params)))

    ##################### Params Library ###########################
    url_list=[];option_list=[];source=params.get("extra")
    ################################################################
    cookie_sess = tvvip_cookie_sess(web)
    url = params.get("url")
    headers = {'Host': 'tv-vip.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01','Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3','Accept-Encoding': 'gzip, deflate',
    'DNT': '1','X-Requested-With': 'XMLHttpRequest','Referer': referer,'Connection': 'keep-alive','Cache-Control': 'max-age=0','__cfduid':cookie_sess}
    url = url.replace('film','json/repo')+'index.json'
    r = requests.get(url,headers=headers)   
    data_js = r.text.encode('utf8')
    js = json.loads(data_js)
    lang = tvvip_lang(url)
    subtitle = tvvip_lang_sub(url)

    ####################################### Control for Linker ##########################################
    if source == "linker":
        plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker TV-vip"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
        logo = params.get("url").replace('film','json/repo')+'poster.jpg'
        fondo = params.get("url").replace('film','json/repo')+'thumbnail.jpg'
        title = js['name'].encode('utf8').strip().replace("\n","").replace("\t","")
        title = title.replace('Ã¡','á').replace('Ã©','é').replace('Ã­','í').replace('Ã³','ó').replace('Âº','ú').replace('Ã±','ñ') 
        genr = tvvip_genr(url)
        if genr =="": genr = 'N/D'
        year = js['year'].encode('utf8').strip().replace("\n","").replace("\t","")
        if year =="": year = 'N/D'
        durac = js['durationHuman'].encode('utf8').strip().replace("\n","").replace("\t","")
        if durac =="": durac = 'N/D'
        punt = js['rate'].encode('utf8').strip().replace("\n","").replace("\t","")
        if punt =="": punt = 'N/D'
        sinopsis = js['description'].encode('utf8').strip().replace("\n","").replace("\t","")
        if sinopsis =="": sinopsis = 'N/D'
        datamovie = {
        'rating': sc3+'[B]Puntuación: [/B]'+ec3+sc+str(punt)+', '+ec,
        'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
        'year': sc3+'[B]Año: [/B]'+ec3+sc+str(year)+', '+ec,
        'duration': sc3+'[B]Duración: [/B]'+ec3+sc+str(durac)+', '+ec,
        'audiochannels': sc3+'[B]Audio: [/B]'+ec3+sc+str(lang)+', '+ec,
        'subtitleslanguage': sc3+'[B]Subtitulos: [/B]'+ec3+sc+str(subtitle)+'[CR]'+ec,
        'sinopsis': sc3+'[B]Sinopsis: [/B]'+ec3+sc+str(sinopsis)+ec}
        datamovie["plot"]=datamovie["rating"]+datamovie["genre"]+datamovie["year"]+datamovie["duration"]+datamovie["audiochannels"]+datamovie["subtitleslanguage"]+datamovie["sinopsis"]
        plugintools.add_item(action="",url="",title=sc5+"[B]"+title+"[/B]"+ec5,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)  
    #####################################################################################################

    quality_grup = js['profiles']
    for quality in quality_grup:
        quality_max = js['profiles'][quality]['videoResolution'].encode('utf8')
        peso = js['profiles'][quality]['sizeHuman'].encode('utf8')
        videouri = js['profiles'][quality]['videoUri'].encode('utf8')
        server = js['profiles'][quality]['servers']
        i=0
        for item in server:
            transcoder = js['profiles'][quality]['servers'][i]['url'].encode('utf8')
            ####################################### Control for Linker ##########################################
            if source == "linker": 
                plugintools.addPeli(action="play_resolvers",url=transcoder,page=videouri,title=sc+title+' (Serv.'+str(i+1)+')'+ec+sc2+"  ["+str(quality_max)+"]"+ec2+sc5+" ["+peso+"]"+ec5,extra= cookie_sess,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)        
                i=i+1
            #####################################################################################################
            ####################################### Control for Library #########################################
            elif source == "library":
                server = 'Tv-vip Serv.'+str(i+1)
                titlefull = '[COLOR white]'+server.title()+' '+'[/COLOR][COLOR lightyellow][I]['+lang.strip()+'] [/COLOR][COLOR lightblue]['+quality_max+'] [/COLOR][COLOR gold][TV-Vip][/I][/COLOR]'
                url_list.append(transcoder+videouri);option_list.append(titlefull)
                i=i+1
            #####################################################################################################

    if params.get("extra") == "library": return option_list,url_list
        
# Series ----------------------------->>

def tvvip_serie_temp(params):
    plugintools.log("[%s %s] Linker TV-vip %s" % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker TV-vip"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    
    cookie_sess = tvvip_cookie_sess(web)
    url = params.get("url")

    url = url.replace('section','json/playlist')+'/index.json'
    headers = {'Host': 'tv-vip.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01','Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3','Accept-Encoding': 'gzip, deflate',
    'DNT': '1','X-Requested-With': 'XMLHttpRequest','Referer': referer,'Connection': 'keep-alive','Cache-Control': 'max-age=0','__cfduid':cookie_sess}
    
    r = requests.get(url,headers=headers)
    
    if 'refresh' in r.headers:
        time.sleep(int(r.headers['refresh'][:1]))
        url = web + '/' + r.headers['refresh'][7:]
        r = requests.get(url,headers=headers)

    data_js = r.text.encode('utf8')
    js = json.loads(data_js)
    
    logo = params.get("url").replace('section','json/playlist')+'/thumbnail_300x300.jpg'
    fondo = params.get("url").replace('section','json/playlist')+'/background.jpg'
    title = js['name'].encode('utf8').strip().replace("\n","").replace("\t","")
    title = title.replace('Ã¡','á').replace('Ã©','é').replace('Ã­','í').replace('Ã³','ó').replace('Âº','ú').replace('Ã±','ñ') 
    genr = tvvip_genr(url)
    if genr =="": genr = 'N/D'
    year = js['year'].encode('utf8').strip().replace("\n","").replace("\t","")
    if year =="": year = 'N/D'
    durac = js['runtime'].encode('utf8').strip().replace("\n","").replace("\t","")
    if durac =="": durac = 'N/D'
    punt = js['rate'].encode('utf8').strip().replace("\n","").replace("\t","")
    if punt =="": punt = 'N/D'
    lang = tvvip_lang(url)
    n_epis = js['number']
    n_temp = js['numberOfSeasons']
    datamovie = {
    'season': sc3+'[B]Temporadas Disponibles: [/B]'+ec3+sc+str(n_temp)+', '+ec,
    'genre': sc3+'[B]Género: [/B]'+ec3+sc+str(genr)+', '+ec,
    'year': sc3+'[B]Año: [/B]'+ec3+sc+str(year)+', '+ec,
    'duration': sc3+'[B]Duración: [/B]'+ec3+sc+str(durac)+ec}
    datamovie["plot"]=datamovie["season"]+datamovie["genre"]+datamovie["year"]+datamovie["duration"]
    plugintools.addPeli(action="",url="",title=sc5+"[B]"+title+"[/B]"+ec5,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)  
    try:
        plugintools.add_item(action="",url="",title=sc2+"Extras"+ec2,thumbnail=logo,fanart=fondo,folder=False,isPlayable=False)
        extras = js['sortedRepoChilds']
        i = 0
        epis = js['sortedRepoChilds'][i]
        for epis in extras:
            title = epis['name'].encode('utf8').replace('Ã¡','á').replace('Ã©','é').replace('Ã­','í').replace('Ã³','ó').replace('Âº','ú').replace('Ã±','ñ') 
            durac = epis['runtime']#.encode('utf8')
            if durac =="":
                durac = "N/D"
            url = 'http://tv-vip.com/film/'+epis['id']+'/' # / necesaria para enviar a tvvip_peli
            plugintools.add_item(action="tvvip_peli",url=url,title=sc+title+ec+sc3+" ["+durac+"]"+ec3,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=True,isPlayable=False)
            epis = int(i)+1
    except: pass
    try:
        tempfull = js['playListChilds']
        i = 0
        temp = js['playListChilds'][i]
        for temp in tempfull:
            logo = 'http://tv-vip.com/json/playlist/'+temp+'/thumbnail_300x300.jpg'
            title_temp = temp.replace('-',' ').title()
            url = 'http://tv-vip.com/section/'+temp+'/'
            plugintools.add_item(action="tvvip_serie_epis",url=url,title=sc2+title_temp+" >>"+ec2,extra= cookie_sess,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=True,isPlayable=False)
    except: pass

def tvvip_serie_epis(params):
    plugintools.log("[%s %s] Linker TV-vip %s" % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker TV-vip"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    title_temp = '[B]'+params.get("title").replace('>>','')+'[/B]'
    logo = params.get('thumbnail')
    fondo = params.get("url").replace('section','json/playlist')+'/background.jpg' 
    plugintools.add_item(action="",url="",title=sc2+title_temp+ec2,thumbnail=logo,fanart=fondo,folder=False,isPlayable=False)

    url = params.get("url")
    cookie_sess = params.get("extra")

    headers = {'Host': 'tv-vip.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01','Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3','Accept-Encoding': 'gzip, deflate',
    'DNT': '1','X-Requested-With': 'XMLHttpRequest','Referer': referer,'Connection': 'keep-alive','Cache-Control': 'max-age=0','__cfduid':cookie_sess}

    url = url.replace('section','json/playlist')+'index.json'
    r = requests.get(url,headers=headers)
    data = r.text.encode('utf8')
    js = json.loads(data)
    try:
        episfull = js['sortedRepoChilds']
        i = 0
        epis = js['sortedRepoChilds'][i]
        for epis in episfull:
            title_epis = epis['name'].encode('utf8').strip().replace("\n","").replace("\t","")
            titlefull = sc+title_epis+ec
            url = 'http://tv-vip.com/film/'+epis['id'].encode('utf8')+'/' # / necesaria para enviar a tvvip_serie_resolvers
        
            plugintools.addPeli(action="tvvip_serie_resolvers",url=url,title=titlefull,extra= cookie_sess,thumbnail=logo,fanart=fondo,folder=True,isPlayable=False)
            epis = int(i)+1
    except: pass

def tvvip_serie_resolvers(params):
    plugintools.log("[%s %s] Linker TV-vip %s" % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="",url="",title="[COLOR lightblue][B]Linker TV-vip"+version+"[/B][COLOR lightblue]"+sc4+"[I] *** By Aquilesserr/PalcoTV Team ***[/I]"+ec4,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
    

    url = params.get("url")
    cookie_sess = params.get("extra")

    headers = {'Host': 'tv-vip.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01','Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3','Accept-Encoding': 'gzip, deflate',
    'DNT': '1','X-Requested-With': 'XMLHttpRequest','Referer': referer,'Connection': 'keep-alive','Cache-Control': 'max-age=0','__cfduid':cookie_sess}
    
    url = url.replace('film','json/repo')+'index.json'
    r = requests.get(url,headers=headers)
    data = r.text.encode('utf8')
    
    data_js = r.text
    js = json.loads(data_js)
    
    logo = params.get("thumbnail")
    fondo = params.get("url").replace('film','json/repo')+'thumbnail.jpg'
    title = js['name'].encode('utf8').strip().replace("\n","").replace("\t","")
    title = title.replace('Ã¡','á').replace('Ã©','é').replace('Ã­','í').replace('Ã³','ó').replace('Âº','ú').replace('Ã±','ñ') 
    genr = tvvip_genr(url)
    if genr =="": genr = 'N/D'
    year = js['year'].encode('utf8').strip().replace("\n","").replace("\t","")
    if year =="": year = 'N/D'
    durac = js['durationHuman'].encode('utf8').strip().replace("\n","").replace("\t","")
    if durac =="": durac = 'N/D'
    punt = js['rate'].encode('utf8').strip().replace("\n","").replace("\t","")
    if punt =="": punt = 'N/D'
    lang = tvvip_lang(url)
    subtitle = tvvip_lang_sub(url)
    datamovie = {
    'duration': sc3+'[B]Duración: [/B]'+ec3+sc+str(durac)+', '+ec,
    'audiochannels': sc3+'[B]Audio: [/B]'+ec3+sc+str(lang)+', '+ec,
    'subtitleslanguage': sc3+'[B]Subtitulos: [/B]'+ec3+sc+str(subtitle)+ec}
    datamovie["plot"]=datamovie["duration"]+datamovie["audiochannels"]+datamovie["subtitleslanguage"]
    plugintools.addPeli(action="",url="",title=sc5+"[B]"+title+"[/B]"+ec5,info_labels=datamovie,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)  
    quality_grup = js['profiles']
    
    for quality in quality_grup:
        quality_max = js['profiles'][quality]['videoResolution'].encode('utf8')
        peso = js['profiles'][quality]['sizeHuman'].encode('utf8')
        videouri = js['profiles'][quality]['videoUri'].encode('utf8');print videouri
        server = js['profiles'][quality]['servers']
        i=0
        for item in server: 
            transcoder = js['profiles'][quality]['servers'][i]['url'].encode('utf8')  
            plugintools.addPeli(action="play_resolvers",url=transcoder,page=videouri,title=sc+title+' (Serv.'+str(i+1)+')'+ec+sc2+"  ["+str(quality_max)+"]"+ec2+sc5+" ["+peso+"]"+ec5,extra= cookie_sess,info_labels=datamovie,thumbnail=logo,fanart=fondo,folder=False,isPlayable=True)        
            i=i+1

################################################# Tools for Linker ##############################################

def tvvip_cookie_sess(url):

    headers = {'Host': 'tv-vip.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01','Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3','Accept-Encoding': 'gzip, deflate',
    'DNT': '1','X-Requested-With': 'XMLHttpRequest','Referer': referer,'Connection': 'keep-alive','Cache-Control': 'max-age=0'}
    r = requests.get(url,headers=headers)
    cookie_sess = r.cookies['__cfduid']
    return cookie_sess

def tvvip_genr(url):
    
    try:
        headers = {'Host': 'tv-vip.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0','Referer': url}
        r = requests.get(url,headers=headers)
        data_js = r.text.encode('utf8')
        js = json.loads(data_js)
        genr = js['tags']
        if len(genr) ==5: genr = genr[0]+', '+genr[1]+', '+genr[2]+', '+genr[3]+', '+genr[4]
        elif len(genr) ==4: genr = genr[0]+', '+genr[1]+', '+genr[2]+', '+genr[3]
        elif len(genr) ==3: genr = genr[0]+', '+genr[1]+', '+genr[2]
        elif len(genr) ==2: genr = genr[0]+', '+genr[1]
        elif len(genr) ==1: genr = genr[0]
        elif len(genr) >5: genr = genr[0]+', '+genr[1]+', '+genr[2]+', '+genr[3]+', '+genr[4]
        return genr.encode('utf8')
    except: return 'N/D'
    
def tvvip_lang(url):
    
    try:
        headers = {'Host': 'tv-vip.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0','Referer': url}
        r = requests.get(url,headers=headers)
        data_js = r.text.encode('utf8')
        js = json.loads(data_js)
        lang = js['languages']
        if len(lang) ==5: lang = lang[0]+', '+lang[1]+', '+lang[2]+', '+lang[3]+', '+lang[4]
        elif len(lang) ==4: lang = lang[0]+', '+lang[1]+', '+lang[2]+', '+lang[3]
        elif len(lang) ==3: lang = lang[0]+', '+lang[1]+', '+lang[2]
        elif len(lang) ==2: lang = lang[0]+', '+lang[1]
        elif len(lang) ==1: lang = lang[0]
        elif len(genr) >5: genr = genr[0]+', '+genr[1]+', '+genr[2]+', '+genr[3]+', '+genr[4]
        lang = lang.replace('1','').replace('2','').replace('3','').replace('4','').replace('5','')
        lang = lang.replace('6','').replace('7','').replace('8','').replace('9','').replace('0','')
        lang = lang.replace('spa','[ESP]').replace('eng','[ENG]').replace('-','').replace('und','N/D')
        return lang.encode('utf8')    
    except: return 'N/D'
    
def tvvip_lang_sub(url):
    
    try:
        headers = {'Host': 'tv-vip.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0','Referer': url}
        r = requests.get(url,headers=headers)
        data_js = r.text.encode('utf8')
        js = json.loads(data_js)
        lang_sub = js['subtitles']
        if len(lang_sub) ==5: lang_sub = lang_sub[0]+', '+lang_sub[1]+', '+lang_sub[2]+', '+lang_sub[3]+', '+lang_sub[4]
        elif len(lang_sub) ==4: lang_sub = lang_sub[0]+', '+lang_sub[1]+', '+lang_sub[2]+', '+lang_sub[3]
        elif len(lang_sub) ==3: lang_sub = lang_sub[0]+', '+lang_sub[1]+', '+lang_sub[2]
        elif len(lang_sub) ==2: lang_sub = lang_sub[0]+', '+lang_sub[1]
        elif len(lang_sub) ==1: lang_sub = lang_sub[0]
        elif len(genr) >5: genr = genr[0]+', '+genr[1]+', '+genr[2]+', '+genr[3]+', '+genr[4]
        lang_sub = lang_sub.replace('1','').replace('2','').replace('3','').replace('4','').replace('5','')
        lang_sub = lang_sub.replace('6','').replace('7','').replace('8','').replace('9','').replace('0','')
        lang_sub = lang_sub.replace('spa','[ESP]').replace('eng','[ENG]').replace('-','')
        return lang_sub.encode('utf8')    
    except: return 'N/D'

def play_resolvers(params):

    transcoder = params.get("url"); videouri = params.get("page"); cookie_sess = params.get("extra")
    transcoder = plugintools.find_single_match(transcoder,'(http.*?)transcoder')+'s/transcoder'
    headers = {'Host': 'tv-vip.com','User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01','Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3','Accept-Encoding': 'gzip, deflate',
    'DNT': '1','X-Requested-With': 'XMLHttpRequest','Referer': referer,'Connection': 'keep-alive','Cache-Control': 'max-age=0','__cfduid':cookie_sess}
    #http://tv-vip.com/video-prod/s/uri?uri=/transcoder/La_colina_de_la_hamburguesa.mp4/default/La_colina_de_la_hamburguesa.mp4&_=1468107896
    videouri_request ='http://tv-vip.com/video-prod/s/uri?uri=/transcoder'+urllib.quote_plus(videouri)+'&_='+timestp()
    r = requests.get(videouri_request,allow_redirects=False,headers=headers)
    resp = r.text
    heads = r.headers
    data_js =json.loads(resp)
    #print data_js
    #http://hs.tv-vip.com/s/transcoder/Ocho_apellidos_catalanes_1.mp4/360-mp4/Ocho_apellidos_catalanes_1.mp4.mp4?tt=1472864848&mm=_vJaInv0MpPyacxeztLg5Q&bb=qGNSVGzVRIL_qbLzNgztuw
    media_url = transcoder+videouri+"?tt=" + str(data_js['tt']) + "&mm=" + data_js['mm'] + "&bb=" + data_js['bb'] 
    print '$'*78+'- By PalcoTV Team -'+'$'*78,media_url,'$'*175
    plugintools.play_resolved_url(media_url)
    
def timestp():
    timest=int(time.time())
    return str(timest+60*60)+'000'
    
######################################### @ By Aquilesserr PalcoTv Team ######################################### 

    


