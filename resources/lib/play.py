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

import xbmc
import xbmcgui
import xbmcplugin
import comm
import utils
import config
import sys
import urllib2

_url = sys.argv[0]
_handle = int(sys.argv[1])

def play_video(params):
    xbmc.log(str(params))
    xbmc.log('askdjhaskdjhsad')
    """ Determine content and pass url to Kodi for playback"""
    if params['action'] == 'listchannels':
        json_url = config.BRIGHTCOVE_DRM_URL.format(config.BRIGHTCOVE_ACCOUNT, 
                                                  params['id'])
        url = comm.get_stream(json_url, live=True)
        play_item = xbmcgui.ListItem(path=url)
        
    elif params['drm'] == 'True':
        import wvhelper
        if wvhelper.check_inputstream():
            acc = config.BRIGHTCOVE_ACCOUNT
            drm_url = config.BRIGHTCOVE_DRM_URL.format(acc, params['id'])
            widevine = comm.get_widevine_auth(drm_url)
            url = widevine['url']
            play_item = xbmcgui.ListItem(path=url)
            play_item.setProperty('inputstream.adaptive.manifest_type', 'mpd')
            play_item.setProperty('inputstream.adaptive.license_type', 'com.widevine.alpha')
            play_item.setProperty('inputstream.adaptive.license_key', widevine['key']+'|Content-Type=application%2Fx-www-form-urlencoded|A{SSM}|')
        else:
            xbmcplugin.setResolvedUrl(_handle, True, xbmcgui.ListItem(path=None))
            return

    else:
        json_url = config.BRIGHTCOVE_DRM_URL.format(config.BRIGHTCOVE_ACCOUNT, 
                                                  params['id'])
        m3u8 = comm.get_stream(json_url)
        data = urllib2.urlopen(m3u8).read().splitlines()
        url = utils.parse_m3u8(data, m3u8_path=m3u8)
        play_item = xbmcgui.ListItem(path=url)

    xbmcplugin.setResolvedUrl(_handle, True, play_item)