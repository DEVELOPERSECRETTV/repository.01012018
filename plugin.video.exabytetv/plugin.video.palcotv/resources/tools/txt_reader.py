# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# TXT_Reader para PalcoTV
# Version 0.1 (18.10.2014)
#----------------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)
#----------------------------------------------------------------------

import os
import sys
import urllib
import urllib2
import re

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools, requests
from __main__ import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")



def txt_reader(params):
    plugintools.log('[%s %s] TXT_reader %s' % (addonName, addonVersion, repr(params)))
    url=params.get("url")
    url = url.replace("txt:", "")

    if url.startswith("http") == True:  # Control para textos online
        plugintools.log("Iniciando descarga desde..."+url)
        h=urllib2.HTTPHandler(debuglevel=0)  # Iniciamos descarga...
        request = urllib2.Request(url)
        opener = urllib2.build_opener(h)
        urllib2.install_opener(opener)
        filename = url.split("/")
        max_len = len(filename)
        max_len = int(max_len) - 1
        filename = filename[max_len]
        fh = open(playlists + filename, "wb")  #open the file for writing
        connected = opener.open(request)
        meta = connected.info()
        filesize = meta.getheaders("Content-Length")[0]
        size_local = fh.tell()
        while int(size_local) < int(filesize):
            blocksize = 100*1024
            bloqueleido = connected.read(blocksize)
            fh.write(bloqueleido)  # read from request while writing to file
            size_local = fh.tell()
            print 'size_local',size_local
        filename = url.split("/")
        inde = len(filename);print inde
        filename = filename[inde-1]
        txt_file = filename
        txt_path = playlists + txt_file
        plugintools.log("Abriendo texto de "+txt_path)
        xbmc.sleep(100)
        TextBoxes("[B][COLOR lightyellow][I]playlists / [/B][/COLOR][/I] "+txt_file,txt_path)       
        
    else:
        txt_path = url
        plugintools.log("Abriendo texto de "+txt_path)
        xbmc.sleep(100)
        TextBoxes("[B][COLOR lightyellow][I]EPG Infotext [/B][/COLOR][/I] ",txt_path)       
        


    

def TextBoxes(heading,anounce):
    class TextBox():
        """Thanks to BSTRDMKR for this code :) """
        # constantes
        WINDOW = 10147
        CONTROL_LABEL = 1
        CONTROL_TEXTBOX = 5

        def __init__( self, *args, **kwargs):
            # activate the text viewer window
            xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
            # get window
            self.win = xbmcgui.Window( self.WINDOW )
            # give window time to initialize
            xbmc.sleep( 500 )
            self.setControls()

        def setControls( self ):
            # set heading
            self.win.getControl( self.CONTROL_LABEL ).setLabel(heading)
            try:
                f = open(anounce)
                text = f.read()
            except: text=anounce
            self.win.getControl( self.CONTROL_TEXTBOX ).setText(text)
            return
    TextBox()


def textmagic0(params):
    plugintools.add_item(action="textmagic1", title="prueba", folder=False, isPlayable=False)

def textmagic1(params):
    readerWindow = TextViewer.createTextViewer(title="prueba", isFirstChapter=True, isLastChapter=True)
    # Display the window
    readerWindow.show()
  
    
# Handles the simple text display window
class TextViewer(xbmcgui.WindowXMLDialog):
    TEXT_BOX_ID = 202
    TEXT_BOX_WHITE_BACKGROUND_ID = 204
    WHITE_BACKGROUND = 104
    TITLE_LABEL_ID = 201
    CLOSE_BUTTON = 302
    READ_BUTTON = 301
    PREVIOUS_BUTTON = 305
    NEXT_BUTTON = 304

    def __init__(self, *args, **kwargs):
        self.isClosedFlag = False
        self.markedAsRead = False
        self.nextSelected = False
        self.previousSelected = False
        self.textControlId = TextViewer.TEXT_BOX_ID
        self.title = kwargs.get('title', '')
        #self.content = kwargs.get('content', '')
        self.isFirstChapter = kwargs.get('firstChapter', False)
        self.isLastChapter = kwargs.get('lastChapter', False)
        xbmcgui.WindowXMLDialog.__init__(self)

    @staticmethod
    def createTextViewer(title, isFirstChapter, isLastChapter):
        plugintools.log("Inicializando ventana...")
        return TextViewer(temp+"script-ebook-text-window.xml", addonId, title="prueba", firstChapter=False, lastChapter=False)
        plugintools.log("Inicializada ventana?")
        

    # Called when setting up the window
    def onInit(self):
        # Check if the user wants a white background
        if Settings.useWhiteBackground():
            xbmcgui.Window(10000).setProperty("EBooks_WhiteBackground", "true")
            self.textControlId = TextViewer.TEXT_BOX_WHITE_BACKGROUND_ID
        else:
            xbmcgui.Window(10000).clearProperty("EBooks_WhiteBackground")
            self.textControlId = TextViewer.TEXT_BOX_ID

        # Update the dialog to show the correct data
        self.updateScreen(self.title, self.isFirstChapter, self.isLastChapter)
        xbmcgui.WindowXMLDialog.onInit(self)

    # Handle any activity on the screen, this will result in a call
    # to close the screensaver window
    def onAction(self, action):
        # actioncodes from https://github.com/xbmc/xbmc/blob/master/xbmc/input/Key.h
        ACTION_PREVIOUS_MENU = 10
        ACTION_NAV_BACK = 92
        ACTION_PAGE_UP = 5
        ACTION_PAGE_DOWN = 6

        if (action == ACTION_PREVIOUS_MENU) or (action == ACTION_NAV_BACK):
            log("TextViewer: Close Action received: %s" % str(action.getId()))
            self.close()
        elif action == ACTION_PAGE_UP:
            log("TextViewer: Page Up Action received: %s" % str(action.getId()))
            # Page up is going to the previous page
            self.onClick(TextViewer.PREVIOUS_BUTTON)
        elif action == ACTION_PAGE_DOWN:
            log("TextViewer: Page Down Action received: %s" % str(action.getId()))
            # Page down is going to the next page
            self.onClick(TextViewer.NEXT_BUTTON)

    def onClick(self, controlID):
        # Play button has been clicked
        if controlID == TextViewer.CLOSE_BUTTON:
            log("TextViewer: Close click action received: %d" % controlID)
            self.close()
        elif controlID == TextViewer.READ_BUTTON:
            log("TextViewer: Mark as read action received: %d" % controlID)
            self.markedAsRead = True
            self.close()
        elif controlID == TextViewer.NEXT_BUTTON:
            log("TextViewer: Request to view next chapter: %d" % controlID)
            self.nextSelected = True
            # Check if we should mark this chapter as read when we navigate to the next one
            if Settings.isMarkReadWhenNavToNextChapter():
                self.markedAsRead = True
        elif controlID == TextViewer.PREVIOUS_BUTTON:
            log("TextViewer: Request to view previous chapter: %d" % controlID)
            self.previousSelected = True

    def close(self):
        log("TextViewer: Closing window")
        self.isClosedFlag = True
        xbmcgui.WindowXMLDialog.close(self)
        xbmcgui.Window(10000).clearProperty("EBooks_WhiteBackground")

    def isClosed(self):
        return self.isClosedFlag

    def isRead(self):
        return self.markedAsRead

    def isNext(self):
        return self.nextSelected

    def isPrevious(self):
        return self.previousSelected

    def updateScreen(self, title, firstChapter=True, lastChapter=True):
        # If new data is being displayed, reset the status flags
        self.markedAsRead = False
        self.nextSelected = False
        self.previousSelected = False

        textControl = self.getControl(self.textControlId)
        #textControl.setText(content)

        labelControl = self.getControl(TextViewer.TITLE_LABEL_ID)
        labelControl.setLabel(title)

        previousControl = self.getControl(TextViewer.PREVIOUS_BUTTON)
        if firstChapter:
            previousControl.setVisible(False)
        else:
            previousControl.setVisible(True)

        nextControl = self.getControl(TextViewer.NEXT_BUTTON)
        if lastChapter:
            nextControl.setVisible(False)
        else:
            nextControl.setVisible(True)
