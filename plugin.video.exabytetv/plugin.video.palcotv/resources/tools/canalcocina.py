# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de Canal Cocina DMax
# Version 0.1 (05.02.2016)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)
# Creditos a Juarrox.
# 

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
from resources.tools.resolvers import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")


url = "http://canalcocina.es/video-recetas"
fanart = 'http://amcnetworks.es/wp-content/uploads/2012/10/CanalCocina-SS01.png'
thumbnail = 'http://i.blogs.es/92a5b8/canal_cocina/650_1200.jpg'

def canalcocina(params):
	r = requests.get(url)	
	data = r.content

	categorias = plugintools.find_multiple_matches(data,'class="recipesTypesLnk(.*?)<')
	plugintools.add_item(action="",url="",title="[COLOR deepskyblue][B]Cocina... ¡¡A la Carta!![/B][/COLOR][COLOR gold][I]      *** By LReylist ***[/I][/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)

	for item in categorias:
		nom_categoria = item.replace('" rel="subsection">','').replace('">','')
		plugintools.add_item(action="cocina_listacategoria",url=url,title=nom_categoria,extra=item,thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
	
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
	plugintools.add_item(action="cocina_busqueda",url="",title="[COLOR red][B][I]····Buscar····[/I][/B][/COLOR]",thumbnail="https://www.cubbyusercontent.com/pl/buscar_cocina.jpg/_8149547852ab4d7288881970522446c4", extra="1", fanart=fanart, folder=True, isPlayable=False)
	
	
	
	
	
def cocina_listacategoria(params):
	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	url = params.get("url")
	categoria = params.get("title")
	titulo_cocinero = params.get("title")
	acotacion = params.get("extra")
	acotacion = 'class="recipesTypesLnk' + acotacion


	r = requests.get(url)	
	data = r.content

	plugintools.add_item(action="",url="",title="[COLOR lightgreen][B]        ·····Categoría: "+categoria+"·····[/B][/COLOR]",thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)
	
	bloque_categoria = plugintools.find_single_match(data,acotacion+'(.*?)</li>')
	if ">Cocineros" in acotacion:
		cada_grupo = plugintools.find_multiple_matches(bloque_categoria,'<dd class(.*?)</dd>')
		tipo_codigo = 2
	elif ">Programas" in acotacion:
		cada_grupo = plugintools.find_multiple_matches(bloque_categoria,'<dd class(.*?)</dd>')
		tipo_codigo = 2
	else:
		cada_grupo = plugintools.find_multiple_matches(bloque_categoria,'<dd>(.*?)</dd>')
		tipo_codigo = 1

	for item in cada_grupo:
		url_grupo = plugintools.find_single_match(item,'href="(.*?)"')
		url_grupo = "http://canalcocina.es"+url_grupo
		
		if tipo_codigo == 1:
			titulo = plugintools.find_single_match(item,'">(.*?)<')
			titulo = titulo.replace("(" , "   [COLOR red](").replace(")" , ")[/COLOR]")
		else:  # es de tipo 2
			titulo = plugintools.find_single_match(item,'title="(.*?)"')
			num_recetas1 = plugintools.find_single_match(item,titulo+'">(.*?)</a>').replace("(","QQQ").replace(")","WWW")
			num_recetas2 = plugintools.find_single_match(num_recetas1,'QQQ(.*?)WWW')
			if len(num_recetas2) == 0:
				num_recetas2 = "Nº Indeterminado"
				
			num_recetas2 = "   [COLOR red][I](" + num_recetas2 + ")[/I][/COLOR]"
			titulo = titulo + num_recetas2

		plugintools.add_item(action="cocina_listavideos",url=url_grupo,title=titulo,extra="",thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)

#**********************************Bloque para añadir otros cocineros que no están en Canal Cocina****************************************

	if "Cocineros" in titulo_cocinero:  # añadimos algunos de fuera
		titulo= "Karlos Arguiñano en tu Cocina    [COLOR red][I](Nº Indeterminado)[/I][/COLOR]"
		url_grupo = "plugin://plugin.video.tvalacarta/?eyJmdWxsdGl0bGUiOiAiS2FybG9zIEFyZ3VpXHUwMGYxYW5vIGVuIHR1IGNvY2luYSIsICJwbG90IjogIkxhcyByZWNldGFzIGRlbCBwcm9ncmFtYSBkZSBjb2NpbmEgZGUgS2FybG9zIEFyZ3VpXHUwMGYxYW5vIiwgImZhbmFydCI6ICJDOlxcVXNlcnNcXHVzdWFyaW9cXEFwcERhdGFcXFJvYW1pbmdcXEtvZGlcXGFkZG9uc1xccGx1Z2luLnZpZGVvLnR2YWxhY2FydGFcXGZhbmFydC5qcGciLCAidGl0bGUiOiAiS2FybG9zIEFyZ3VpXHUwMGYxYW5vIGVuIHR1IGNvY2luYSIsICJ1cmwiOiAiUEw4RUNDMjcxMzFCNDBDM0QxIiwgImZvbGRlciI6IHRydWUsICJhY3Rpb24iOiAidmlkZW9zIiwgImNoYW5uZWwiOiAieW91dHViZV9jaGFubmVsIiwgInRodW1ibmFpbCI6ICJodHRwczovL2kueXRpbWcuY29tL3ZpL0xMbGZQZDJteGQwL2hxZGVmYXVsdC5qcGcifQ%3d%3d"
		plugintools.add_item(action="runPlugin",url=url_grupo,title=titulo,extra="",thumbnail="http://static.hogarmania.com/archivos/201509/logo-karlos-2012-2013-1280x720x80xX.jpg?1", fanart=fanart, folder=True, isPlayable=True)

		titulo= "Recetas Exprés de Karlos Arguiñano    [COLOR red][I](Nº Indeterminado)[/I][/COLOR]"
		url_grupo = "plugin://plugin.video.tvalacarta/?action=videos&category=hogarutil&channel=youtube_channel&extradata&fulltitle=La%20receta%20expr%c3%a9s%20de%20Karlos%20Argui%c3%b1ano&plot=La%20receta%20del%20d%c3%ada%20de%20Karlos%20Argui%c3%b1ano%20en%20menos%20de%203%20minutos.&show&thumbnail=https%3a%2f%2fi.ytimg.com%2fvi%2fxOPVS6TftkA%2fhqdefault.jpg&title=La%20receta%20expr%c3%a9s%20de%20Karlos%20Argui%c3%b1ano&url=PLu2StT2f6eAtO71ydsvk3eMDLrMXJJPQM"
		plugintools.add_item(action="runPlugin",url=url_grupo,title=titulo,extra="",thumbnail="http://www.hogarmania.com/archivos/201601/caratula-receta-expres-karlos-2016-416x236x80xX.jpg?1", fanart=fanart, folder=True, isPlayable=True)

		titulo= "Cocina con Bruno Oteiza    [COLOR red][I](Nº Indeterminado)[/I][/COLOR]"
		url_grupo = "plugin://plugin.video.tvalacarta/?eyJmdWxsdGl0bGUiOiAiQ29jaW5hIGNvbiBCcnVubyBPdGVpemEiLCAicGxvdCI6ICJSZWNldGFzLCB0cnVjb3MgeSBjb25zZWpvcyBkZWwgY29jaW5lcm8gZGUgbGFTZXh0YSBCcnVubyBPdGVpemEiLCAiZmFuYXJ0IjogIkM6XFxVc2Vyc1xcdXN1YXJpb1xcQXBwRGF0YVxcUm9hbWluZ1xcS29kaVxcYWRkb25zXFxwbHVnaW4udmlkZW8udHZhbGFjYXJ0YVxcZmFuYXJ0LmpwZyIsICJ0aXRsZSI6ICJDb2NpbmEgY29uIEJydW5vIE90ZWl6YSIsICJ1cmwiOiAiUExFRUVFMzJERTJGREZBREI3IiwgImZvbGRlciI6IHRydWUsICJhY3Rpb24iOiAidmlkZW9zIiwgImNoYW5uZWwiOiAieW91dHViZV9jaGFubmVsIiwgInRodW1ibmFpbCI6ICJodHRwczovL2kueXRpbWcuY29tL3ZpL2wzVVVieHd0NDJBL2hxZGVmYXVsdC5qcGcifQ%3d%3d"
		plugintools.add_item(action="runPlugin",url=url_grupo,title=titulo,extra="",thumbnail="http://todotele.com/wp-content/uploads/2014/11/Cocina-con-Bruno-Bruno-Oteiza.jpg", fanart=fanart, folder=True, isPlayable=True)

		titulo= "Cocina con Sergio    [COLOR red][I](Nº Indeterminado)[/I][/COLOR]"
		url_grupo = "plugin://plugin.video.tvalacarta/?action=episodios&category=Recetas&channel=rtve&extradata=56310&fulltitle=Cocina%20con%20Sergio&plot&show=Cocina%20con%20Sergio&thumbnail&title=Cocina%20con%20Sergio&url=http%3a%2f%2fwww.rtve.es%2falacarta%2fvideos%2fcocina-con-sergio%2f"
		plugintools.add_item(action="runPlugin",url=url_grupo,title=titulo,extra="",thumbnail="http://uva-vinalopo.org/wp/wp-content/uploads/2012/10/COCINA-CON-SERGIO_300.jpg", fanart=fanart, folder=True, isPlayable=True)

		titulo= "Dulces de Eva Arguiñano    [COLOR red][I](Nº Indeterminado)[/I][/COLOR]"
		url_grupo = "plugin://plugin.video.tvalacarta/?action=videos&category=hogarutil&channel=youtube_channel&extradata&fulltitle=La%20receta%20expr%c3%a9s%20de%20Karlos%20Argui%c3%b1ano&plot=La%20receta%20del%20d%c3%ada%20de%20Karlos%20Argui%c3%b1ano%20en%20menos%20de%203%20minutos.&show&thumbnail=https%3a%2f%2fi.ytimg.com%2fvi%2fxOPVS6TftkA%2fhqdefault.jpg&title=La%20receta%20expr%c3%a9s%20de%20Karlos%20Argui%c3%b1ano&url=PLu2StT2f6eAtO71ydsvk3eMDLrMXJJPQM"
		plugintools.add_item(action="runPlugin",url=url_grupo,title=titulo,extra="",thumbnail="https://i.ytimg.com/vi/z1w4g_OiPCI/hqdefault.jpg", fanart=fanart, folder=True, isPlayable=True)

		titulo= "Las Recetas de Eva Arguiñano    [COLOR red][I](Nº Indeterminado)[/I][/COLOR]"
		url_grupo = "plugin://plugin.video.tvalacarta/?eyJmdWxsdGl0bGUiOiAiTGFzIHJlY2V0YXMgZGUgRXZhIEFyZ3VpXHUwMGYxYW5vIiwgInBsb3QiOiAiTG9zIHBvc3RyZXMgZGUgRXZhIEFyZ3VpXHUwMGYxYW5vIiwgImZhbmFydCI6ICJDOlxcVXNlcnNcXHVzdWFyaW9cXEFwcERhdGFcXFJvYW1pbmdcXEtvZGlcXGFkZG9uc1xccGx1Z2luLnZpZGVvLnR2YWxhY2FydGFcXGZhbmFydC5qcGciLCAidGl0bGUiOiAiTGFzIHJlY2V0YXMgZGUgRXZhIEFyZ3VpXHUwMGYxYW5vIiwgInVybCI6ICJQTDQ1Q0U0MjgxQzIwNzg3NkEiLCAiZm9sZGVyIjogdHJ1ZSwgImFjdGlvbiI6ICJ2aWRlb3MiLCAiY2hhbm5lbCI6ICJ5b3V0dWJlX2NoYW5uZWwiLCAidGh1bWJuYWlsIjogImh0dHBzOi8vaS55dGltZy5jb20vdmkvejF3NGdfT2lQQ0kvaHFkZWZhdWx0LmpwZyJ9"
		plugintools.add_item(action="runPlugin",url=url_grupo,title=titulo,extra="",thumbnail="http://www.eladerezo.com/wp-content/uploads/2011/02/eva-argui%C3%B1ano-nova-628x456.jpg", fanart=fanart, folder=True, isPlayable=True)

		titulo= "La Cocina de HogarManía    [COLOR red][I](Nº Indeterminado)[/I][/COLOR]"
		url_grupo = "plugin://plugin.video.tvalacarta/?eyJmdWxsdGl0bGUiOiAiQ29jaW5hIiwgInBsb3QiOiAiUmVjZXRhcyB5IHByb2dyYW1hcyBkZSBjb2NpbmEgZW4gSG9nYXJ1dGlsLmNvbSIsICJmYW5hcnQiOiAiQzpcXFVzZXJzXFx1c3VhcmlvXFxBcHBEYXRhXFxSb2FtaW5nXFxLb2RpXFxhZGRvbnNcXHBsdWdpbi52aWRlby50dmFsYWNhcnRhXFxmYW5hcnQuanBnIiwgInRpdGxlIjogIkNvY2luYSIsICJ1cmwiOiAiUEwxQTkyNEEwMzg2NEFENEY1IiwgImZvbGRlciI6IHRydWUsICJhY3Rpb24iOiAidmlkZW9zIiwgImNoYW5uZWwiOiAieW91dHViZV9jaGFubmVsIiwgInRodW1ibmFpbCI6ICJodHRwczovL2kueXRpbWcuY29tL3ZpL25IYjBYQ25fb2s4L2hxZGVmYXVsdC5qcGcifQ%3d%3d"
		plugintools.add_item(action="runPlugin",url=url_grupo,title=titulo,extra="",thumbnail="http://cdn0.bodas.com.mx/usr/6/5/8/1/cfb_259624.jpg", fanart=fanart, folder=True, isPlayable=True)

		titulo= "Ver y Cocinar.com    [COLOR red][I](Nº Indeterminado)[/I][/COLOR]"
		url_montada = "plugin://plugin.video.tvalacarta/?action=subcanales&category=adnstream&channel=adnstream&extradata&fulltitle=Ver%20y%20cocinar&plot&show=Cocina&thumbnail=http%3a%2f%2fwww.adnstream.com%2fimg%2fcanales%2fVer-y-cocinar_w320.jpg&title=Ver%20y%20cocinar&url=http%3a%2f%2fwww.adnstream.com%2fcanal%2fVer-y-cocinar%2f"
		plugintools.add_item(action="runPlugin",title=titulo,url=url_montada,thumbnail="http://www.adnstream.com/img/caratulas/Ver-y-cocinar.jpg", fanart=fanart,folder=True,isPlayable=True)



def cocina_listavideos(params):
	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	url = params.get("url")
	titulo = params.get("title")
	extra_cabecera = params.get("extra")

	pagina_actual = "1"
	if "/pag/" in url:  # viene de páginación
		pagina_actual = plugintools.find_single_match(url,'/pag/(.*?)/')
		
	
	r = requests.get(url)	
	data = r.content

	if pagina_actual == "1":
		extra_cabecera = titulo
		cabecera = "[COLOR lightgreen][B]·····"+titulo+"·····[/B][/COLOR]"
	else:
		cabecera ="[COLOR lightgreen][B]·····"+extra_cabecera+"[I]  Pag. "+pagina_actual+"[/I]·····[/B][/COLOR]"
		
	plugintools.add_item(action="",url="",title=cabecera,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)

	
	bloque_videos = plugintools.find_single_match(data,'<h3 class=(.*?)class="letter-filter cube pagination')
	cada_video = plugintools.find_multiple_matches(bloque_videos,'<a(.*?)/p>')

	for item in cada_video:
	
		titulo_vid = plugintools.find_single_match(item,'class="icon(.*?)/span>')
		titulo_video = plugintools.find_single_match(titulo_vid,'</i>(.*?)<')
		
		url_video = plugintools.find_single_match(item,'href="(.*?)"')
		url_video = "http://canalcocina.es"+url_video
		cocinero = plugintools.find_single_match(item,'chef20"></i>(.*?)<').strip()
		logo = plugintools.find_single_match(item,'src="(.*?)"')
		
		titulo_completo = titulo_video + "   [COLOR red][I](" + cocinero + ")[/I][/COLOR]"

		plugintools.add_item(action="lanza_video",url=url_video,title=titulo_completo,extra="",thumbnail=logo, fanart=fanart, folder=False, isPlayable=True)

	#Resuelvo la posibilidad de mas de 1 Página en la Categoría
	#Como la paginación no funciona en la web, tengo q hacerlo de forma "manual"... y como no se cual es la ultima página, no tengo mas remedio que
	#ir llamando a la sig. pág hasta que descubra que no existe.
	pagina_prox = str(int(pagina_actual) + 1)

	if pagina_actual == "1":
		url_proxima = url + "/pag/" + pagina_prox + "/"
	else:
		tex_actu = "/pag/" + pagina_actual
		tex_prox = "/pag/" + pagina_prox
		url_proxima = url.replace(tex_actu , tex_prox)

	plugintools.add_item(action="cocina_listavideos",url=url_proxima,title="[COLORFFFF0759]Página: " + pagina_prox + "  >>>[/COLOR]",extra=extra_cabecera,thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)
		



		
def lanza_video(params):
	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	url = params.get("url")
	titulo = params.get("title")

	r = requests.get(url)	
	data = r.content

	video_id = plugintools.find_single_match(data,'data-video-id="(.*?)"')
	pub_id = plugintools.find_single_match(data,'data-account="(.*?)"')
	
	url_lanza = "http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId=" + video_id + "&pubId=" + pub_id
	
	params["url"] = url_lanza
	plugintools.play_resolved_url(url_lanza)
	

def cocina_busqueda(params):
	fanart = params.get("fanart")
	thumbnail = params.get("thumbnail")
	title = params.get("title")
	recursividad = params.get("extra")

	if recursividad == "1":
		buscar=""
		buscar = plugintools.keyboard_input().replace(" ", "+")
		url_busca="http://canalcocina.es/video-recetas?buscarEn=videoRecetas&q="+buscar
		buscar = buscar.replace("+"," ")
		cabecera = "[COLOR lightgreen][B]Búsqueda: "+buscar+"    [COLOR yellow][I]Pag. 1"+"[/I][/B][/COLOR]"
	else:
		url_busca = params.get("url")
		buscar = plugintools.find_single_match(url_busca,'buscarEn=videoRecetas&q=(.*?)')
		cabecera = recursividad

	r = requests.get(url_busca)	
	data = r.content

	plugintools.add_item(action="",url="",title=cabecera,thumbnail=thumbnail,fanart=fanart,folder=False,isPlayable=False)
	plugintools.add_item(action="",url="",title="",thumbnail=thumbnail, fanart=fanart, folder=False, isPlayable=False)

	bloque_videos = plugintools.find_single_match(data,'<h3 class=(.*?)class="letter-filter cube pagination')
	cada_video = plugintools.find_multiple_matches(bloque_videos,'<a(.*?)/p>')

	for item in cada_video:
	
		titulo_vid = plugintools.find_single_match(item,'class="icon(.*?)/span>')
		titulo_video = plugintools.find_single_match(titulo_vid,'</i>(.*?)<')
		
		url_video = plugintools.find_single_match(item,'href="(.*?)"')
		url_video = "http://canalcocina.es"+url_video
		cocinero = plugintools.find_single_match(item,'chef20"></i>(.*?)<').strip()
		logo = plugintools.find_single_match(item,'src="(.*?)"')
		
		titulo_completo = titulo_video + "   [COLOR red][I](" + cocinero + ")[/I][/COLOR]"

		plugintools.add_item(action="lanza_video",url=url_video,title=titulo_completo,extra="",thumbnail=logo, fanart=fanart, folder=False, isPlayable=True)

	
	#Resuelvo la posibilidad de mas de 1 Página en la Búsqueda
	
	pag_sig = plugintools.find_single_match(data,'<!--<span>...</span>-->(.*?)title=')
	
	pagina_prox = plugintools.find_single_match(pag_sig,'href="(.*?)"')
	##if len(pagina_prox) <> 0:  # Es que hay otra página en la búsqueda
	if "http://canalcocina.es" in pagina_prox:  # Es que hay otra página en la búsqueda
		num_prox_pag = plugintools.find_single_match(pagina_prox,'/pag/(.*?)/')
		
		plugintools.add_item(action="cocina_busqueda",url=pagina_prox,title="[COLORFFFF0759]Página: " + num_prox_pag + "  >>>[/COLOR]",extra="[COLOR lightgreen][B]Búsqueda: "+buscar+"    [COLOR yellow][I]Pag. "+num_prox_pag+"[/I][/B][/COLOR]",thumbnail=thumbnail, fanart=fanart, folder=True, isPlayable=False)

	






















	