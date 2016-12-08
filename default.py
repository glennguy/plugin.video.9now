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
import xbmcplugin

import urllib
import urllib2
from urlparse import parse_qsl

addon = xbmcaddon.Addon()
cwd = xbmc.translatePath(addon.getAddonInfo('path')).decode("utf-8")
BASE_RESOURCE_PATH = os.path.join(cwd, 'resources', 'lib')
sys.path.append(BASE_RESOURCE_PATH)

import config
import series
import genres
import episodes
import play
import live

_url = sys.argv[0]
_handle = int(sys.argv[1])

addonname = addon.getAddonInfo('name')
addonPath = xbmcaddon.Addon().getAddonInfo("path")
fanart = os.path.join(addonPath, 'fanart.jpg')

def list_categories():
    """ Make initial list"""
    listing = []
    categories = config.CATEGORIES
    for category in categories:
        li = xbmcgui.ListItem(category)
        urlString = '{0}?action=listcategories&category={1}'
        url = urlString.format(_url, category)
        is_folder = True
        listing.append((url, li, is_folder))
        
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)
              

def router(paramstring):
    """ Router function that calls other functions depending on the 
    provided paramstring"""
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'listcategories':
            if params['category'] == 'Genres':
                genres.make_genres_list(paramstring)
            elif params['category'] == 'TV Series':
                series.make_series_list(paramstring)
            elif params['category'] == 'Live TV':
                live.make_live_list(paramstring)
        elif params['action'] == 'listgenres':
            series.make_series_list(paramstring)
            
        elif params['action'] == 'listseries':
            episodes.make_episodes_list(paramstring)
        elif params['action'] == 'listepisodes':
            play.play_video(params)
        elif params['action'] == 'listchannels':
            play.play_video(params)
    else:
        list_categories()

if __name__ == '__main__':
    router(sys.argv[2][1:])

