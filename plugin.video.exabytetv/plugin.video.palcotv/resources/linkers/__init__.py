# -*- coding: utf-8 -*-
#-------------------------------------------------------------------
# PalcoTV - Kodi Add-on by Juarrox (juarrox@gmail.com)
#-------------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#-------------------------------------------------------------------
# Gracias a la librerías y tutoriales de Jesús (mimediacenter.info)
#-------------------------------------------------------------------


import os
import sys

try:
    import plugintools
except:
    sys.path.append( os.path.abspath( os.path.join( os.path.dirname(__file__) , ".." , ".." ) ) )