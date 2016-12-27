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

SSD_WV_REPO = "https://github.com/glennguy/decryptmodules/raw/master/"
WIDEVINECDM_URL = { 'Linuxx86_64': 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb',
                    'Linuxarmv7': 'http://odroidxu.leeharris.me.uk/xu3/chromium-widevine-1.4.8.823-2-armv7h.pkg.tar.xz',
                    'Linuxarmv7': 'http://odroidxu.leeharris.me.uk/xu3/chromium-widevine-1.4.8.823-2-armv7h.pkg.tar.xz'}

UNARCHIVE_COMMAND = { 'Linuxx86_64': "(cd {1} && ar x {0} data.tar.xz && tar xJfO data.tar.xz ./opt/google/chrome/libwidevinecdm.so >{1}/{2} && chmod 755 {1}/{2} && rm -f data.tar.xz {0})",
                      'Linuxarmv7': "(cd {1} && tar xJfO {0} usr/lib/chromium/libwidevinecdm.so >{1}/{2} && chmod 755 {1}/{2} && rm -f {0})",
                      'Linuxarmv8': "(cd {1} && tar xJfO {0} usr/lib/chromium/libwidevinecdm.so >{1}/{2} && chmod 755 {1}/{2} && rm -f {0})"}
SSD_WV_DICT = { 'Windows': 'ssd_wv.dll',
                'Linux': 'libssd_wv.so',
                'Darwin': 'libssd_wv.dylib'}
WIDEVINECDM_DICT = { 'Windows': 'widevinecdm.dll',
                     'Linux': 'libwidevinecdm.so',
                     'Darwin': 'libwidevinecdm.dylib'}
SUPPORTED_PLATFORMS = [ 'WindowsAMD64',
                        'Windowsx86',
                        'Darwinx86_64',
                        'Linuxx86_64',
                        'Linuxarmv7',
                        'Linuxarmv8']

XML_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?><request protocol="3.0" 
version="chrome-55.0.2883.87" prodversion="55.0.2883.87" requestid="{{{0}}}" 
lang="en-US" updaterchannel="" prodchannel="" os="{1}" arch="{2}" 
nacl_arch="x86-64" wow64="1"><hw physmemory="12"/><os platform="Windows" 
arch="x86_64" version="10.0.0"/><app appid="oimompecagnajdejgnnjijobebaeigek" 
version="0.0.0.0" installsource="ondemand"><updatecheck/><ping rd="-2" 
ping_freshness=""/></app></request>"""

CRX_UPDATE_URL = "https://clients2.google.com/service/update2?cup2key=6:{0}&cup2hreq={1}"