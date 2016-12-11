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

CATEGORIES = ['TV Series', 'Genres', 'Live TV']
GENRES_URL = "https://tv-api.9now.com.au/v1/genres?device=android&take=99999"
TVSERIES_URL = "https://tv-api.9now.com.au/v1/tv-series?device=android&take=99999"
EPISODEQUERY_URL = "https://tv-api.9now.com.au/v1/pages/tv-series/{0}/seasons/{1}?device=android"
LIVETV_URL = "https://tv-api.9now.com.au/v1/pages/livestreams?device=android"
BRIGHTCOVE_URL = "http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId={0}"
BRIGHTCOVE_DRM_URL = "https://edge.api.brightcove.com/playback/v1/accounts/{0}/videos/ref:{1}"
BRIGHTCOVE_ACCOUNT = "4460760524001"
BRIGHTCOVE_KEY = "BCpkADawqM1TWX5yhWjKdzhXnHCmGvnaozGSDICiEFNRv0fs12m6WA2hLxMHM8TGAEM6pv7lhJsdNhiQi76p4IcsT_jmXdtEU-wnfXhOBTx-cGR7guCqVwjyFAtQa75PFF-TmWESuiYaNTzg"
SYSTEM_DICT = { 'win32': 'Windows',
                'linux2': 'Linux',
                'darwin': 'OSX'}
SSD_WV_DICT = { 'win32': 'ssd_wv.dll',
                'linux2': 'libssd_wv.so',
                'darwin': 'libssd_wv.dylib'}
WIDEVINECDM_DICT = { 'win32': 'widevinecdm.dll',
                'linux2': 'libwidevinecdm.so',
                'darwin': 'libwidevinecdm.dylib'}