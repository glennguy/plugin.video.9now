# Copyright 2016 Glenn Guy
# This file is part of 9now Kodi Addon
#
# 9now is free software: you can redistribute it and/or modify
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
import urllib

_url = sys.argv[0]
_handle = int(sys.argv[1])


def make_series_list(url):
    """ Make list of series Listitems for Kodi"""
    params = dict(urlparse.parse_qsl(url))
    series_list = comm.list_series()
    filtered = []
    if 'genre' in params:
        for s in series_list:
            if s.genre == urllib.unquote_plus(params['genre']):
                filtered.append(s)
    else:
        filtered = series_list

    listing = []
    for s in filtered:
        li = xbmcgui.ListItem(s.title, iconImage=s.thumb,
                              thumbnailImage=s.thumb)
        li.setArt({'fanart': s.fanart})
        url = '{0}?action=listseries{1}'.format(_url, s.make_kodi_url())
        is_folder = True
        listing.append((url, li, is_folder))

    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)
