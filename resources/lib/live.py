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

import xbmcgui
import xbmcplugin
import comm
import sys
import urlparse

_url = sys.argv[0]
_handle = int(sys.argv[1])


def make_live_list(url):
    """ Make list of channel Listitems for Kodi"""
    params = dict(urlparse.parse_qsl(url))
    channels = comm.list_live(params)
    listing = []
    for c in channels:
        li = xbmcgui.ListItem(c.title, iconImage=c.thumb,
                              thumbnailImage=c.thumb)
        li.setArt({'fanart': c.fanart})
        url = '{0}?action=listchannels{1}'.format(_url, c.make_kodi_url())
        is_folder = False
        li.setProperty('IsPlayable', 'true')
        li.setInfo('video', {'plot': c.desc, 'plotoutline': c.episode_name})
        listing.append((url, li, is_folder))

    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)
