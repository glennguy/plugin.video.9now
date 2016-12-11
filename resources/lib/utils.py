# Copyright 2016 Glenn Guy
# This file is part of 9now Kodi Addon
#
# tenplay is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# 9now is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with 9now.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import xbmc
import xbmcgui
import xbmcaddon
import config

def check_inputstream():
    """ Make sure all components required are available for DRM playback.
        Inform of missing components"""
    try:
        addon = xbmcaddon.Addon('inputstream.adaptive')
        
    
    except RuntimeError as e:
        xbmcgui.Dialog().ok('Missing inputstream.adaptive', 'inputstream.adaptive VideoPlayer InputStream add-on not found. This add-on is required to view DRM protected content.')
        return False
    plat = get_system()
    if not check_widevinecdm():
        
        xbmcgui.Dialog().ok('Missing widevinecdm module', '{0} not found in {1} ({2}). This module is required to view DRM protected content.'.format(config.WIDEVINECDM_DICT[plat], addon.getSetting('DECRYPTERPATH'), xbmc.translatePath(addon.getSetting('DECRYPTERPATH'))))
        return False
    if not check_ssd_wv():
        xbmcgui.Dialog().ok('Missing ssd_wv module', '{0} not found in {1} ({2}). This module is required to view DRM protected content.'.format(config.SSD_WV_DICT[plat], addon.getSetting('DECRYPTERPATH'), xbmc.translatePath(addon.getSetting('DECRYPTERPATH'))))
        return False
    return True
    
def check_widevinecdm():
    """ Check for (lib)widevinecdm.dll/so/dylib"""
    addon = xbmcaddon.Addon('inputstream.adaptive')
    cdm_path = xbmc.translatePath(addon.getSetting('DECRYPTERPATH'))
    for file in os.listdir(cdm_path):
        if 'widevinecdm' in file:
            return True
    return False

def check_ssd_wv():
    """ Check for (lib)ssd_wv.dll/so/dylib"""
    addon = xbmcaddon.Addon('inputstream.adaptive')
    cdm_path = xbmc.translatePath(addon.getSetting('DECRYPTERPATH'))
    for file in os.listdir(cdm_path):
        if 'ssd_wv' in file:
            return True
    return False

def get_system():
    return sys.platform

