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
import sys
import urlparse
import urllib

_url = sys.argv[0]
_handle = int(sys.argv[1])

def make_genres_list(url):
    """ Make list of genre Listitems for Kodi"""
    params = dict(urlparse.parse_qsl(url))
    genres = comm.list_genres()
    listing = []
    for g in genres:
        li = xbmcgui.ListItem(g.title, iconImage=g.thumb,
                                    thumbnailImage=g.thumb)
        li.setArt({'fanart': g.fanart})
        url = '{0}?action=listgenres{1}'.format(_url, g.make_kodi_url())
        is_folder = True
        listing.append((url, li, is_folder))
            
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)