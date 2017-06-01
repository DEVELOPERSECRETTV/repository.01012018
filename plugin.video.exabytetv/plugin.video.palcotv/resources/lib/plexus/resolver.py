# -*- coding: utf-8 -*-

""" Plexus  (c)  2015 enen92

    Este archivo contiene funciones para enlazar con acestream o sopcast dependiendo del argumento dado (id o url)
    Esta función se usa en los elementos del menú principal
    
    Funciones:
    
    go_to_id(p2p_type) -> Recibe el tipo de stream (sop o ace) y activa el teclado para recibir el argumento que puede ser un id de sopcast o un hash de acestream o la url de sopcast.


    *** Esta función irá en media_analyzer
"""
    
import xbmc,sys
from plexusutils.pluginxbmc import *
import sopcast as sop
import acestream as ace
    
def go_to_id(p2p_type):
	if p2p_type=='ace':
		keyb = xbmc.Keyboard('', translate(30022))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText()
			if search=='': sys.exit(0)
			else:
				channel_id = search
				ace.acestreams(translate(30020) + ' ( ' + str(channel_id) + ')','',str(channel_id))
	elif p2p_type=='sop_id':
		channel_id = xbmcgui.Dialog().numeric(0, translate(30018))
		sop.sopstreams(translate(30020) + ' ( ' + str(channel_id) + ')','',str(channel_id))
	elif p2p_type=='sop_url':
		keyb = xbmc.Keyboard('sop://', translate(30019) + ' sop://')
		keyb.doModal()
		if (keyb.isConfirmed()):
			search = keyb.getText()
			if search=='': sys.exit(0)
			else:
				channel_id = search
				sop.sopstreams(translate(30021) + ' ( ' + str(channel_id) + ')','',str(channel_id))
