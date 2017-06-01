# -*- coding: utf-8 -*-
#----------------------------------------------------------
#  Log Reader para PalcoTV
#  Version 0.1 (14/04/2016)
#----------------------------------------------------------
#  License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#----------------------------------------------------------

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
from __main__ import *
from resources.tools.txt_reader import *

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
tempfolder = xbmc.translatePath(os.path.join('special://temp/', ''))
home = xbmc.translatePath(os.path.join('special://home/', ''))


def logreader0(params):
    plugintools.log("Iniciando Log Reader...")

    kodilog=home+'kodi.log';blokerr=""
    plugintools.log("Abriendo archivo: "+kodilog)

    if os.path.exists(kodilog) is True:
        TextBoxes("[B][COLOR lightyellow][I]Kodi.log[/B][/COLOR][/I]",kodilog)

    elif os.path.exists(tempfolder+'kodi.log') is True:
        TextBoxes("[B][COLOR lightyellow][I]Kodi.log[/B][/COLOR][/I]",tempfolder+'kodi.log')
    
