# -*- coding: utf-8 -*-
#------------------------------------------------------------------
# PalcoTV EPG Sports
# Version 0.1 (11.11.2014)
#------------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------------


# EPG Sports
# EPG KHL TV SD/HD: http://en.khl.ru/tv/?sid=1703
# EPG Russia: https://betteam.ru/tv.php?id_channel=0&data=2016-06-15
# EPG-txt Russia: http://tvgid.net/
# EPG Russia: http://www.dvhab.ru/tv/grid/2014-06-13?time=day&channel=4
# EPG Russia: http://www.vl.ru/tv/grid/2015-06-24?channel=4



import os, sys, urllib, urllib2, re, time, calendar
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import plugintools

from datetime import datetime, date, timedelta
from __main__ import *
from dateutil import parser
#from dateutil.parser import parse

temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")


def epg_arena(title):
    plugintools.log("[%s %s] P2P Sports EPG Guide... %s " % (addonName, addonVersion, title))

    title=title.lower();horas = [];eventos = [];epg_channel = []
    if title.find("arenasport") >= 0 or title.find("sportklub") >= 0:
        epg_channel = epg_arenasports(horas, eventos, title)
    elif title.find("digi") >= 0 or title.find("dolce") >= 0:
        epg_channel = cinemagia_epg(horas, eventos, title)
    else: epg_channel = tvnu_epg(title, horas, eventos)

    return epg_channel
  
def epg_arenasports(horas, eventos, title):
    #plugintools.log("[%s %s] Arenasports EPG Guide ... %s " % (addonName, addonVersion, title))

    epg_channel = []   
    # Consultamos ruta del archivo de programación de TV.nu para hoy y mañana
    formatodia = "%Y-%m-%d"
    hoy = datetime.today();epg_arenasp_hoy = hoy.strftime(formatodia)
    epg_arenasp_hoy = temp + 'Guide_Arenasport-'+str(epg_arenasp_hoy)+'.txt'
    
    if os.path.exists(epg_arenasp_hoy):
        fepg = open(epg_arenasp_hoy, "r");data=fepg.read()
    else:
        plugintools.log("Creamos archivo EPG de Arenasport para hoy: "+epg_arenasp_hoy)
        fepg_arenasp = open(epg_arenasp_hoy, "wb")
        r=requests.get('http://tv.aladin.info/live');data=r.content;fepg_arenasp.write(data);fepg_arenasp.close()

    if title == "arenasport 1" or title == "arenasport 1 hd": id = '69'
    elif title == "arenasport 2" or title == "arenasport 2 hd": id = '70'
    elif title == "arenasport 3" or title == "arenasport 3 hd": id = '71'
    elif title == "arenasport 4" or title == "arenasport 4 hd": id = '72'
    elif title == "arenasport 5" or title == "arenasport 5 hd": id = '91'
    elif title == "sportklub 1" or title == "sportklub 1 hd": id = '57'
    elif title == "sportklub 2" or title == "sportklub 2 hd": id = '58'
    elif title == "sportklub 3" or title == "sportklub 3 hd": id = '92'
    elif title == "sportklub 4" or title == "sportklub 4 hd": id = '93'

    tablevents = plugintools.find_single_match(data, 'tv_source_'+id+'(.*?)</div><style>')
    eventos = plugintools.find_multiple_matches(tablevents, 'class=\'list-group-item(.*?)/li>')
    evento_ahora="";hora_ahora="";evento_luego="";evento_mastarde="";hora_luego="";hora_mastarde="";
    for entry in eventos:
        #plugintools.log("evento= "+entry)
        if evento_luego != "" and evento_mastarde=="":
            evento_mastarde = plugintools.find_single_match(entry, '</span>(.*?)<')
            hora_mastarde = plugintools.find_single_match(entry, 'block\'>(.*?)</span>').strip()
        if evento_ahora != "" and evento_luego =="":
            hora_luego = plugintools.find_single_match(entry, 'block\'>(.*?)</span>').strip()
            evento_luego = plugintools.find_single_match(entry, '</span>(.*?)<')            
        if entry.find("bg-warning") >= 0:
            hora_ahora = plugintools.find_single_match(entry, 'block\'>(.*?)</span>').strip()
            evento_ahora = plugintools.find_single_match(entry, '</span>(.*?)<')
             
    epg_channel = hora_ahora,evento_ahora,hora_luego,evento_luego,hora_mastarde,evento_mastarde  
    return epg_channel    

def tvnu_epg(title, horas, eventos):
    #plugintools.log("[%s %s] TV.nu EPG Guide ... " % (addonName, addonVersion))
    # Consultamos ruta del archivo de programación de TV.nu para hoy y mañana
    formatodia = "%Y-%m-%d"
    hoy = datetime.today();epg_tvnu_hoy = hoy.strftime(formatodia)
    manana = hoy + timedelta(days=1);epg_tvnu_manana = manana.strftime(formatodia)
    epg_tvnu_hoy = temp + 'Guide_TVnu-'+str(epg_tvnu_hoy)+'.txt'
    epg_tvnu_manana = temp + 'Guide_TVnu-'+str(epg_tvnu_manana)+'.txt'
    
    if os.path.exists(epg_tvnu_hoy):
        fepg = open(epg_tvnu_hoy, "r");data=fepg.read()

    elif not os.path.exists(epg_tvnu_hoy):
        plugintools.log("Creamos archivo EPG de TV.nu para hoy: "+epg_tvnu_hoy)
        fepg_tvnu = open(epg_tvnu_hoy, "wb")
        url = 'http://www.tv.nu/'
        r=requests.get(url);cookies = {'channelSelection': '[132,116,136,137,140,152,164,30178,30177,139,154,30124,30161,30160,30148,30153,30154,30172,30171,138,29,28,133,115,117,120,121,125,126,131,94,30186]', 'cookienotice': '1', 'scheduleCompact': 'false'}
        r=requests.get(url, cookies=cookies);data=r.content;fepg_tvnu.write(data);fepg_tvnu.close()

    elif not os.path.exists(epg_tvnu_manana):
        plugintools.log("Creamos archivo EPG de TV.nu para mañana: "+epg_tvnu_manana)
        fepg_tvnu = open(epg_tvnu_manana, "wb")
        url = 'http://www.tv.nu/imorgon'
        r=requests.get(url);cookies = {'channelSelection': '[132,116,136,137,140,152,164,30178,30177,139,154,30124,30161,30160,30148,30153,30154,30172,30171,138,29,28,133,115,117,120,121,125,126,131,94,30186]', 'cookienotice': '1', 'scheduleCompact': 'false'}
        r=requests.get(url, cookies=cookies);data=r.content;fepg_tvnu.write(data);fepg_tvnu.close()    

    # Calculamos hora actual para comparar horarios
    formatodia = "%Y-%m-%d %H:%m"
    hoy = datetime.today()
    ahora = hoy.strftime(formatodia)
    timenow = parser.parse(ahora)
    ts_local = time.mktime(timenow.timetuple())

    title=title.lower()
    if title.find("viasat hockey") >= 0: id = '140'
    elif title.find("viasat golf hd") >= 0: id = '30171'
    elif title.find("viasat fotboll hd") >= 0: id = '138'
    elif title.find("eurosport 1 hd") >= 0: id = '133'
    elif title.find("eurosport 2 hd") >= 0: id = '30172'
    elif title.find("viasat sport hd") >= 0: id = '154'
    elif title.find("c more sport hd") >= 0: id = '115'
    elif title.find("viasat motor hd") >= 0: id = '121'
    elif title.find("c more fotboll hd") >= 0: id = '30160'
    elif title.find("c more hockey") >= 0: id = '30161'  # Este ID corresponde a C More Hockey HD porque el ID de "C More Hockey SD" (126) no devuelve nada
    elif title.find("c more golf hd") >= 0: id = '30153'
    elif title.find("eurosport 1") >= 0: id = '132'
    #elif title.find("eurosport 2") >= 0: id = ''    
    elif title.find("c more golf") >= 0: id = '30154'
    elif title.find("viasat hockey hd") >= 0: id = '30148'
    elif title.find("c more sport") >= 0: id = '116'
    elif title.find("c more fotboll") >= 0: id = '125'
    #elif title.find("c more hockey") >= 0: id = '126'
    elif title.find("c more tennis") >= 0: id = '117'
    #elif title.find("c more sport sf-kanalen") >= 0: id = '164'
    elif title.find("viasat sport") >= 0: id = '136'
    elif title.find("viasat fotboll") >= 0: id = '137'
    elif title.find("viasat motor") >= 0: id = '120'
    elif title.find("viasat hockey") >= 0: id = '140'
    elif title.find("tv4 sport") >= 0: id = '152'    
    elif title.find("fight sports") >= 0: id = '30178'
    elif title.find("tv3 sport") >= 0: id = '30177'
    elif title.find("tv2") >= 0: id = '30124'
    elif title.find("viasat golf") >= 0: id = '139'
    elif title.find("motors tv") >= 0: id = '29'
    elif title.find("extreme sports") >= 0: id = '28'
        
    try: 
        bloque = plugintools.find_single_match(data, 'data-id=\"'+id+'(.*?)channel-schedule grid')
        plugintools.log("bloque= "+bloque)
        eventos = plugintools.find_multiple_matches(bloque, '<li(.*?)</li>')
        evento_ahora="";hora_ahora="";hora_luego = "";evento_luego = "";hora_mastarde="";evento_mastarde="";
        for entry in eventos:
            #plugintools.log("entry= "+entry)
            title = plugintools.find_single_match(entry, 'data-title="([^"]+)')
            start = plugintools.find_single_match(entry, 'data-start-time="([^"]+)')
            try: dia = start.split("T")[0];hora = plugintools.find_single_match(start, 'T([^\+]+)');plugintools.log("dia= "+dia);plugintools.log("hora= "+hora)
            except: pass
            end = plugintools.find_single_match(entry, 'data-end-time="([^"]+)')
            start_unix = plugintools.find_single_match(entry, 'data-start-time-unix="([^"]+)')
            end_unix = plugintools.find_single_match(entry, 'data-end-time-unix="([^"]+)')
            #plugintools.log("start_unix= "+start_unix);plugintools.log("end_unix= "+end_unix);plugintools.log("hoy= "+str(ahora));plugintools.log("ts_local= "+str(ts_local))
            if evento_ahora!="" and evento_luego=="":
                evento_luego = title;hora_luego = hora[0:5]
                continue
            elif evento_ahora!="" and evento_luego!="" and evento_mastarde=="":
                evento_mastarde=title;hora_mastarde = hora[0:5]
                continue
            elif evento_ahora=="":
                if int(end_unix) > int(ts_local) > int(start_unix):
                    evento_ahora = title;hora_ahora = hora[0:5]
                    #plugintools.log("evento_ahora= "+title);plugintools.log("hora_ahora= "+hora_ahora)
                    continue
      
        epg_channel = hora_ahora,evento_ahora,hora_luego,evento_luego,hora_mastarde,evento_mastarde
        plugintools.log("evento_luego= "+evento_luego)
        plugintools.log("hora_luego= "+hora_luego)
        return epg_channel

    except: pass


def cinemagia_epg(title, horas, eventos):
    #plugintools.log("[%s %s] CineMagia.ro EPG Guide ... " % (addonName, addonVersion))
    # Consultamos ruta del archivo de programación de CineMagia.ro para hoy y mañana
    formatodia = "%Y-%m-%d"
    hoy = datetime.today();epg_cmro_hoy = hoy.strftime(formatodia)
    manana = hoy + timedelta(days=1);epg_cmro_manana = manana.strftime(formatodia)
    epg_cmro_hoy = temp + 'Guide_CineMagia.ro-'+str(epg_cmro_hoy)+'.txt'
    epg_cmro_manana = temp + 'Guide_CineMagia.ro-'+str(epg_cmro_manana)+'.txt'
    
    if os.path.exists(epg_cmro_hoy):
        fepg = open(epg_cmro_hoy, "r");data=fepg.read()

    elif not os.path.exists(epg_cmro_hoy):
        plugintools.log("Creamos archivo EPG de CineMagia.ro para hoy: "+epg_cmro_hoy)
        fepg_cmro = open(epg_cmro_hoy, "wb")
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0', 'Referer': 'http://www.cinemagia.ro/', 'program_tv_vertical': '1'}
        b=requests.get('http://www.cinemagia.ro/program-tv/', headers=headers);cook=b.cookies;cookie=''
        for kuki in cook: cookie+=kuki.name+'='+kuki.value+'; ';
        headers.update({'Cookie':cookie, 'user_station_list': '%5B122%2C123%2C141%2C345%2C120%2C121%2C248%2C249%2C411%2C413%2C29%2C64%2C323%2C225%2C30%5D', 'Referer': 'http://www.cinemagia.ro/program-tv/'})
        url = 'http://www.cinemagia.ro/program-tv/post/digi-sport-1/'
        r=requests.get(url, headers=headers, verify=None);data=r.content;fepg_cmro.write(data);fepg_cmro.close()
        #user_station_list: [122,123,141,345,120,121,248,249,411,413,29,64,323,225,30]

    # Logos de canales
    digi1 = [];digi2=[];digi3=[];digi4=[]
    logo_bloque = plugintools.find_single_match(data, '<td class="container_logo"(.*?)</tr>')
    canales = plugintools.find_multiple_matches(logo_bloque, 'alt="([^"]+)')
    logos = plugintools.find_multiple_matches(logo_bloque, 'src="([^"]+)')
        
    #hora_ahora="",evento_ahora="",hora_luego="",evento_luego="",hora_mastarde="",evento_mastarde=""
    prog=[];current=0
    blq_eventos = plugintools.find_multiple_matches(data, '<td class="container_events"(.*?)</tbody>')  # El último evento de la lista será el evento "ahora"
    for bloque in blq_eventos:  #cada tramo de programación pertenece a un canal, luego hay que agregarlo a su correspondiente lista
        blq_evento=plugintools.find_multiple_matches(bloque, '<tr>(.*?)</tr>')
        for evento in blq_evento:
            #plugintools.log("evento= "+evento)
            hora=plugintools.find_single_match(evento, '<div>(.*?)</div>').strip()
            event=plugintools.find_single_match(evento, '<div class="title">(.*?)</div>').strip() 
            if evento.find("current") >= 0:
                title_fixed=hora+' '+event
                plugintools.log("evento actual: "+title_fixed)
                

    
#blq_eventos = plugintools.find_multiple_matches(data, '<tr id="showContainer-NEXT">(.*?)</tbody>')  # Eventos futuros (para coger el luego, después y más tarde)
# Los bloques de programación carecen de nombre, luego no hay forma de identificarlos más que por el orden en el que aparecen éstos o bien llamar a la URL .../digi-sport-2/ (etc)
        

    

    '''

    r=requests.get(url);data=r.content
    channel = plugintools.find_multiple_matches(body, '<td class=\'text-center strong \'>(.*?)</td>')
    event = plugintools.find_multiple_matches(body, '<td class=\'\'>(.*?)</td></tr>')
    evento_ahora = plugintools.find_single_match(body, '<td class=\'bg-warning\'>(.*?)</td></tr>')
    next_matches = plugintools.find_single_match(body, evento_ahora+'(.*?)</div>')
    evento_luego = plugintools.find_single_match(next_matches, '<td class=\'\'>(.*?)</td></tr>')
    hora_luego = plugintools.find_single_match(next_matches, '<td class=\'text-center strong \'>(.*?)</td>')
    hora_ahora = plugintools.find_single_match(body, 'class=\'text-center strong bg-warning\'>(.*?)</td><td class=\'bg-warning\'>'+evento_ahora)

    epg_channel = hora_ahora,evento_ahora,hora_luego,evento_luego
    return epg_channel

00:42:01 T:6808  NOTICE: title= Eurosport 1
00:42:01 T:6808  NOTICE: title= C More Sport
00:42:01 T:6808  NOTICE: title= Viasat Sport
00:42:01 T:6808  NOTICE: title= Viasat Fotboll
00:42:01 T:6808  NOTICE: title= Viasat Hockey
00:42:01 T:6808  NOTICE: title= TV4 Sport
00:42:01 T:6808  NOTICE: title= C More Sport SF-Kanalen
00:42:01 T:6808  NOTICE: title= Fight Sports
00:42:01 T:6808  NOTICE: title= TV3 Sport HD
00:42:01 T:6808  NOTICE: title= Viasat Golf
00:42:01 T:6808  NOTICE: title= Viasat Sport HD
00:42:01 T:6808  NOTICE: title= TV2
00:42:01 T:6808  NOTICE: title= C More Hockey HD
00:42:01 T:6808  NOTICE: title= C More Fotboll HD
00:42:01 T:6808  NOTICE: title= Viasat Hockey HD
00:42:01 T:6808  NOTICE: title= C More Golf HD
00:42:01 T:6808  NOTICE: title= C More Golf
00:42:01 T:6808  NOTICE: title= Eurosport 2 HD
00:42:01 T:6808  NOTICE: title= Viasat Golf HD
00:42:01 T:6808  NOTICE: title= Viasat Fotboll HD
00:42:01 T:6808  NOTICE: title= Motors TV Europe
00:42:01 T:6808  NOTICE: title= Extreme Sports Europe
00:42:01 T:6808  NOTICE: title= Eurosport 1 HD
00:42:01 T:6808  NOTICE: title= C More Sport HD
00:42:01 T:6808  NOTICE: title= C More Tennis
00:42:01 T:6808  NOTICE: title= Viasat Motor
00:42:01 T:6808  NOTICE: title= Viasat Motor HD
00:42:01 T:6808  NOTICE: title= C More Fotboll


00:43:01 T:1184  NOTICE: title= 132
00:43:01 T:1184  NOTICE: title= 116
00:43:01 T:1184  NOTICE: title= 136
00:43:01 T:1184  NOTICE: title= 137
00:43:01 T:1184  NOTICE: title= 140
00:43:01 T:1184  NOTICE: title= 152
00:43:01 T:1184  NOTICE: title= 164
00:43:01 T:1184  NOTICE: title= 30178
00:43:01 T:1184  NOTICE: title= 30177
00:43:01 T:1184  NOTICE: title= 139
00:43:01 T:1184  NOTICE: title= 154
00:43:01 T:1184  NOTICE: title= 30124
00:43:01 T:1184  NOTICE: title= 30161
00:43:01 T:1184  NOTICE: title= 30160
00:43:01 T:1184  NOTICE: title= 30148
00:43:01 T:1184  NOTICE: title= 30153
00:43:01 T:1184  NOTICE: title= 30154
00:43:01 T:1184  NOTICE: title= 30172
00:43:01 T:1184  NOTICE: title= 30171
00:43:01 T:1184  NOTICE: title= 138
00:43:01 T:1184  NOTICE: title= 29
00:43:01 T:1184  NOTICE: title= 28
00:43:01 T:1184  NOTICE: title= 133
00:43:01 T:1184  NOTICE: title= 115
00:43:01 T:1184  NOTICE: title= 117
00:43:01 T:1184  NOTICE: title= 120
00:43:01 T:1184  NOTICE: title= 121
00:43:01 T:1184  NOTICE: title= 125


    

    '''

def encode_string(txt):
    plugintools.log("[PalcoTV-0.3.0].encode_string: "+txt)
    
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
    txt = txt.replace('&#246;',"ö")
    txt = txt.replace('&#228;', "ä")
    
    return txt


def gethttp_noref(url):
    plugintools.log("[PalcoTV-0.3.0.gethttp_noref] "+url)    

    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    return body

# Esta función devuelve el evento en emisión ahora
def compara_times(horas, eventos):
    plugintools.log("[PalcoTV-0.3.1].compara_times")
    print horas, eventos

    from datetime import datetime  

    # Determinamos fecha actual para construir URL
    ahora = datetime.now()
    if int(ahora.minute) < 10:
        minutos = "0" + str(ahora.minute)
    else:
        minutos = str(ahora.minute)
    time_now = str(ahora.hour) + ":" + minutos  # Lo pasamos a minutos para comparar
    #plugintools.add_item(action="", title="Son las "+time_now, url="", folder=False, isPlayable=False)
    
    #Iniciamos comparación de horas
    if int(ahora.hour) <= 12:
        time_now = ((ahora.hour + 12) * 60) + ahora.minute
        plugintools.log("Antes de mediodía= "+str(time_now))
    else:
        time_now = (ahora.hour * 60) + ahora.minute
        plugintools.log("Después de mediodía= "+str(time_now))
    
    plugintools.log("time_now= "+str(time_now))
    i = 0
    try:
        while i < len(horas):
            time_event = horas[i]
            time_event = ( int(time_event[0:2]) * 60 ) + int(time_event[3:5])
            plugintools.log("time_event= "+str(time_event))
            if int(ahora.hour) <= 12:
                time_now = ((ahora.hour + 12) * 60) + ahora.minute
                plugintools.log("Antes de mediodía= "+str(time_now))
                diff = time_event - time_now
                print diff
                if diff <= 0:
                    hora_ahora = horas[i-1]
                    evento_ahora = eventos[i-1]
                    plugintools.log("evento_ahora= "+evento_ahora)
                    hora_luego = horas[i]
                    evento_luego = eventos[i]
                    plugintools.log("evento_luego= "+evento_luego)
                    return hora_ahora,evento_ahora,hora_luego,evento_luego
                    break
                else:                    
                    i = i + 1
            if int(ahora.hour) >= 12:
                time_now = ((ahora.hour + 12) * 60) + ahora.minute
                plugintools.log("Antes de mediodía= "+str(time_now))
                diff = time_now - time_event
                print diff
                if diff >= 0:
                    hora_ahora = horas[i-1]
                    evento_ahora = eventos[i-1]
                    plugintools.log("evento_ahora= "+evento_ahora)
                    hora_luego = horas[i]
                    evento_luego = eventos[i]
                    plugintools.log("evento_luego= "+evento_luego)
                    return hora_ahora,evento_ahora,hora_luego,evento_luego
                    break
                else:                    
                    i = i + 1                    
            
    except:
        pass
    

