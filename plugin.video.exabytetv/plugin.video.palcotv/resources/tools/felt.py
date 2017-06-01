# -*- coding: utf-8 -*-
#------------------------------------------------------------
# AgendaTV para PalcoTV
# Version 0.1 (18.10.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


from __main__ import *
from resources.tools.txt_reader import *

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

thumbnail = 'http://playtv.pw/wp-content/uploads/2015/05/logo1.png'
fanart = 'http://46wvda23y0nl13db2j3bl1yxxln.wpengine.netdna-cdn.com/wp-content/uploads/2013/06/tsn-dudes.jpg'

# URLs 
baloncesto='http://www.futbolenlatv.com/deporte/baloncesto'
balonmano='http://www.futbolenlatv.com/deporte/balonmano'
ciclismo='http://www.futbolenlatv.com/deporte/ciclismo'
tenis='http://www.futbolenlatv.com/deporte/tenis'
rugby='http://www.futbolenlatv.com/deporte/rugby'
amfutbol='http://www.futbolenlatv.com/deporte/futbol-americano'
futsal='http://www.futbolenlatv.com/deporte/futbol-sala'
motociclismo='http://www.futbolenlatv.com/deporte/motociclismo'
automovilismo='http://www.futbolenlatv.com/deporte/automovilismo'
todos='http://www.futbolenlatv.com/deporte'

# URLs TV por país
ger='http://www.fussball-im-tv.com/'
gbr='http://www.ukfootballontv.co.uk/'
usa='http://www.uslivesoccertv.com/'
ita='http://www.calciointv.com/'


hockey='http://liveonsat.com/los_other_ice_hockey.php'



def feltv0(params):
    
    filename = 'futboltv.txt'
    futboltv = open(temp + filename, "wb")
    
    feltv1(params, futboltv)
    futboltv.write('\n\n')
    #futbolenlatv_manana(params)
    #feltv1(params, futboltv)
    futboltv.close()
    params = plugintools.get_params()
    params["url"]=temp+'futboltv.txt'
    txt_reader(params)    


def feltv1(params, futboltv):
    plugintools.log('[%s %s] Fútbolenlatv.com %s' % (addonName, addonVersion, repr(params)))

    title = '[COLOR lightblue][B]FútbolenlaTV.com[/B][/COLOR]'
    futboltv.write(title+'\n\n');
    canales="";kanales="";url = params.get("url");r=requests.get(url);data=r.content
    schedule=plugintools.find_single_match(data, '<table class="table table-bordered tabla-partidos">(.*)</table>')
    daymatches=plugintools.find_multiple_matches(schedule, 'class=" dia-partido">(.*?)</td></tr>');i=0
    jornada=plugintools.find_multiple_matches(schedule, '<td colspan="5"(.*?)class=" dia-partido">')
    for dia in jornada:
        dia=dia.replace("&#241;", "ñ").replace("&#233;", "é").replace("&#243;", "ó").replace("&#225;", "á").replace("&#227;", "í").strip()
        events=plugintools.find_multiple_matches(dia, '<tr class="event-row hidden-xs">(.*?)</td></tr>');j=len(events)
        if j>0:
            plugintools.log("***** Día: "+dia)
            if "Hoy" in dia:
                title = '[COLOR lightyellow][I]Agenda para [B]hoy[/B][/I][/COLOR]'
                futboltv.write(title+'\n\n');
            elif "Mañana" in dia:
                daymatch=plugintools.find_single_match(dia, 'class="visible-md visible-lg dia-partido">(.*?)</td></tr>')
                title = '[COLOR lightyellow][I]'+daymatch+'[/I][/COLOR]'
                futboltv.write(title+'\n\n')
            else:
                title = '[COLOR lightyellow][I]'+ daymatches[i].replace("&#241;", "ñ").replace("&#233;", "é").replace("&#243;", "ó").replace("&#225;", "á").replace("&#227;", "í").strip() + '[/I][/COLOR]'
                futboltv.write(title+'\n\n')
                i=i+1
                
            for item in events:
                plugintools.log("*** Evento: "+item)
                idsport=plugintools.find_single_match(item, '<div class="ftvi-co-([^"]+)');plugintools.log("ID Deporte= "+idsport)
                deporte,thumbnail=feltv_id(idsport)
                hora=plugintools.find_single_match(item, '<td class="hora">(.*?)</td>').replace("<span>", "").replace("</span>", "").strip()
                blq_torneo=plugintools.find_single_match(item, '<li class="detalles-liga">(.*?)</li>')
                torneo=plugintools.find_single_match(blq_torneo, '<span title="([^"]+)')
                detalle=plugintools.find_single_match(blq_torneo, '<li class="detalles-jornada">(.*?)</li>')
                #liga=plugintools.find_single_match(item, '<li class="no-underline">(.*?)</li>');plugintools.log("liga= "+liga)
                match=plugintools.find_multiple_matches(item, 'class="no-underline">(.*?)</span>');rivales="";liga=match[0].replace("1l2l3", "1|2|3")       
                for entry in match:
                    if entry!=liga:
                        if rivales=="": rivales=entry
                        else: rivales=rivales+" vs "+entry
                canales=plugintools.find_single_match(item, '<td class="canales">(.*?)</td></tr>')
                free=plugintools.find_multiple_matches(item, '<li class="abierto" title="([^"]+)')  # Canales en abierto
                premium=plugintools.find_multiple_matches(item, '<li class="premium" title="([^"]+)')  # Canales de pago
                
                for canal in free:
                    if canales=="": canales=canal
                    else: canales=canales+', '+canal        
                
                for kanal in premium:
                    if kanales=="": kanales=kanal
                    else: kanales=kanales+', '+kanal

                if canales!="" and kanales!="":
                    title = hora + " H. " + '[COLOR white]' + deporte + ':[/COLOR] ' + '[COLOR lightgreen][B]' + liga.upper() + ':[/B][/COLOR]' + " " + '[COLOR lightyellow][I]' + rivales + '[/I][/COLOR]\n[COLOR white]En abierto: [B][I]' + canales + '[/B][/I][/COLOR]\nDe pago: [B][I]'+kanales+'[/I][/B]'
                elif canales!="" and kanales=="": title = hora + " H. " + '[COLOR white]' + deporte + ':[/COLOR] ' + '[COLOR lightgreen][B]' + liga.upper() + '[/B][/COLOR]' + " " + '[COLOR lightyellow][I]' + rivales + '[/I][/COLOR]\n[COLOR white]En abierto: [B][I]' + canales + '[/B][/I][/COLOR]'
                else:title = hora + " H. " + '[COLOR white]' + deporte + ':[/COLOR] ' + '[COLOR lightgreen][B]' + liga.upper() + '[/B][/COLOR]' + " " + '[COLOR lightyellow][I]' + rivales + '[/I][/COLOR]\nDe pago: [B][I]'+kanales+'[/I][/B]'
                futboltv.write(title+'\n\n')
                canales="";kanales=""        
        
		


def get_fecha():

    from datetime import datetime
    
    ahora = datetime.now()
    anno_actual = ahora.year
    mes_actual = ahora.month
    dia_actual = ahora.day
    fecha = str(dia_actual) + "/" + str(mes_actual) + "/" + str(anno_actual)
    plugintools.log("fecha de hoy= "+fecha)
    return fecha    
    
            
            
def decode_string(string):
    string = string.replace("&nbsp;&nbsp;", "")
    string = string.replace("indexf.php?comp=", "")
    string = string.replace('>', "")
    string = string.replace('"', "")
    string = string.replace("\n", "")
    string = string.strip()
    string = string.replace('\xfa', 'ú')
    string = string.replace('\xe9', 'é')
    string = string.replace('\xf3', 'ó')
    string = string.replace('\xfa', 'ú')
    string = string.replace('\xaa', 'ª')
    string = string.replace('\xe1', 'á')
    string = string.replace('&#241;', 'ñ')
    string = string.replace('&#237;', 'í')
    string = string.replace('&#250;', 'ú')
    string = string.replace('\xf1', 'ñ').strip()
    

    return string

    
def feltv_id(idsport):
    plugintools.log("ID: "+idsport)
	
    deporte="";thumb=""    
    if idsport=="1":
        deporte="Fútbol"
        thumb=art+'futbol.png'
    elif idsport=="93":
        deporte="Automovilismo"
        thumb=art+'motor.png'
    elif idsport=="94":
        deporte="Baloncesto"
        thumb=art+'baloncesto.png'
    elif idsport=="05":
        deporte="Balonmano"
        thumb=art+'balonmano.png'
    elif idsport=="96":
        deporte="Ciclismo"
        thumb=art+'ciclismo.png'
    elif idsport=="99":
        deporte="Fútbol Americano"
        thumb=art+'rugby.png'
    elif idsport=="100":
        deporte="Fútbol Sala"
        thumb=art+'futsal.png'
    elif idsport=="101":
        deporte="Golf"
        thumb=art+'golf.png'
    elif idsport=="104":
        deporte="Motociclismo"
        thumb=art+'motor.png'
    elif idsport=="106":
        deporte="Rugby"
        thumb=art+'rugby.png'
    elif idsport=="107":
        deporte="Tenis"
        thumb=art+'tenis.png'		
	
    return deporte, thumbnail
            
    
