# -*- coding: utf-8 -*-
#------------------------------------------------------------
# ScraperX para PalcoTV
# Version 0.1 (08.04.2016)
# Creado por Juarrox & Aquilesserr
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------

import urlparse,urllib2,urllib,re,shutil
import os, sys

import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import plugintools, requests, json, time, zipfile, shutil

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

art = addonPath + "/art/"
playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

thumbnail = 'https://www.cubbyusercontent.com/pl/ScraperX_Logo.png/_2a871862a8014477aa550febc8e0839b'
thumbnail_nofound = 'https://www.cubbyusercontent.com/pl/PosterNoDispScraperLogo.png/_90a8df5244e149939c6f6aa8a9b1a4f0'
fanart = 'https://www.cubbyusercontent.com/pl/scraperx.png/_425ab9087a564c45ae6f216db8655e1a'



def seriepix(params):
    plugintools.log("[%s %s] Abriendo lista de capítulos ... %s " % (addonName, addonVersion, params))

    tvdb_id=params.get("extra")
    plugintools.add_item(action="", title=params.get("title").strip(), thumbnail=params.get("thumbnail"), fanart=params.get("fanart"), folder=False, isPlayable=False)
    
    infofile=open(temp+str(tvdb_id)+'/es.xml', "r")
    data = infofile.read()
    epix=plugintools.find_multiple_matches(data, '<Episode>(.*?)</Episode>')
    bannerpath='http://thetvdb.com/banners/'

    for entry in epix:
        director=plugintools.find_single_match(entry, '<Director>\|(.*?)\|</Director>').replace("|", ", ").strip()
        writer=plugintools.find_single_match(entry, '<Writer>\|(.*?)\|</Writer>').replace("|", ", ").strip()
        tvdb_id=plugintools.find_single_match(entry, '<id>([^<]+)')
        title=plugintools.find_single_match(entry, '<EpisodeName>([^<]+)')
        number=plugintools.find_single_match(entry, '<EpisodeNumber>([^<]+)')
        premiere=plugintools.find_single_match(entry, '<FirstAired>([^<]+)')
        sinopsis=plugintools.find_single_match(entry, '<Overview>([^<]+)')
        rating=plugintools.find_single_match(entry, '<Rating>([^<]+)')
        captura=bannerpath+plugintools.find_single_match(entry, '<filename>([^<]+)')
        fulltitle='[COLOR white]'+title+'[/COLOR][COLOR lightgreen][I][ '+tvdb_id+'][/I][/COLOR]'
        plugintools.add_item(action="", title=fulltitle, thumbnail=captura, fanart=params.get("fanart"), folder=False, isPlayable=False)

        
