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
import urlparse

def parse_m3u8(data, m3u8_path, qual=-1):
    """ Parse the retrieved m3u8 stream list into a list of dictionaries
        then return the url for the highest quality stream."""
    ver = 0
    if '#EXT-X-VERSION:3' in data:
        ver = 3
        data.remove('#EXT-X-VERSION:3')
    if '#EXT-X-VERSION:4' in data:
        ver = 4
        data.remove('#EXT-X-VERSION:4')
    count = 1
    m3u_list = []
    for line in data:
        xbmc.log(line)
    while count < len(data):
        if ver == 3 or ver == 0:
            line = data[count]
            line = line.strip('#EXT-X-STREAM-INF:')
            line = line.strip('PROGRAM-ID=1,')
            line = line[:line.find('CODECS')]
    
            if line.endswith(','):
                line = line[:-1]
    
            line = line.strip()
            line = line.split(',')
            linelist = [i.split('=') for i in line]
            linelist.append(['URL', data[count + 1]])
            m3u_list.append(dict((i[0], i[1]) for i in linelist))
            count += 2

        if ver == 4: 
            line = data[count]
            line = line.strip('#EXT-X-STREAM-INF:')
            line = line.strip('PROGRAM-ID=1,')
            values = line.split(',')
            xbmc.log(str(values))
            for value in values:
                if value.startswith('BANDWIDTH'):
                    bw = value
                elif value.startswith('RESOLUTION'):
                    res = value
            url = urlparse.urljoin(m3u8_path, data[count + 1])
            m3u_list.append(dict([bw.split('='), res.split('='), ['URL', url]]))
            count += 3
    
    sorted_m3u_list = sorted(m3u_list, key=lambda k: int(k['BANDWIDTH']))
    stream = sorted_m3u_list[qual]['URL']
    return stream

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

