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
import classes
import config
import urllib
import urllib2
import json

def list_series():
    """ Create and return list of series objects"""
    req = config.TVSERIES_URL
    res = urllib2.urlopen(req)
    data = json.loads(res.read())
    listing = []
    for show in data['items']:
        x = len(show['containsSeason'])
        if x > 1: 
            multi_season = True
        else:
            multi_season = False
        while x >= 1:
            s = classes.series()
            s.multi_season = multi_season
            s.season_slug = show['containsSeason'][x-1]['slug']
            s.series_name = show['name']
            s.season_name = show['containsSeason'][x-1]['name']
            s.series_slug = show['containsSeason'][x-1]['partOfSeries']['slug']
            s.fanart = show['image']['sizes']['w1920']
            s.thumb = show['containsSeason'][x-1]['image']['sizes']['w480']
            s.genre = show['containsSeason'][x-1]['genre']['name']
            s.title = s.get_title()
            listing.append(s)
            x -= 1
    return listing

def list_genres():
    """ Create and return list of genre objects"""
    req = config.GENRES_URL
    res = urllib2.urlopen(req)
    data = json.loads(res.read())
    listing = []
    for genre in data['items']:
        g = classes.genre()
        g.fanart = (genre['image']['sizes']['w1920'])
        g.thumb = (genre['image']['sizes']['w480'])
        g.genre_slug = genre['slug']
        g.title = genre['name']
        g.genre = genre['name']
        listing.append(g)
    return listing

def list_episodes(params):
    """ Create and return list of episode objects"""       
    requrl = config.EPISODEQUERY_URL.format(params['series_slug'], params['season_slug'])
    req = urllib2.Request(requrl)
    xbmc.log('Fetching URL: {}'.format(requrl))
    res = urllib2.urlopen(req).read()
    data = json.loads(res)
    listing = []
    for section in data['items']:
        # filter extras etc for most shows.
        if section.get('callToAction'):
            if (section['callToAction']['link']['type'] not in 
                ['episode-index', 'external']):
                continue
        for episode in section['items']:
            # filter extras again as some show are unable to be filtered at the
            # previous step
            if not episode.get('episodeNumber'):
                continue
            # make sure season numbers match, some shows return all seasons.
            if episode['partOfSeason'].get('slug') != params['season_slug']:
                continue
            
            e = classes.episode()
            e.episode_no = str(episode['episodeNumber'])
            e.thumb = episode['image']['sizes']['w480']
            e.fanart = data['tvSeries']['image']['sizes']['w1920']
            e.episode_name = episode['name'].encode('utf8')
            e.title = e.get_title()
            e.desc = episode['description']
            e.duration = episode['video']['duration']//1000
            e.airdate = episode['airDate']
            e.id = episode['video']['referenceId']
            e.drm = episode['video']['drm'] == True
            listing.append(e)
    return listing

def list_live(params):
    """ Create and return list of channel objects""" 
    requrl = config.LIVETV_URL
    req = urllib2.Request(requrl)
    xbmc.log('Fetching URL: {}'.format(requrl))
    res = urllib2.urlopen(req).read()
    data = json.loads(res)
    listing = []
    for channel in data['channels']:
        c = classes.channel()
        c.title = channel['name']
        c.fanart = channel['image']['sizes']['w1920']
        c.thumb = channel['image']['sizes']['w480']
        c.desc = channel['listings'][0]['name']
        c.episode_name = channel['listings'][0]['episodeTitle']
        c.id = channel['referenceId']
        listing.append(c)
    return listing

def get_stream(url, live=False):
    """ Parse live tv JSON and return stream url""" 
    req = urllib2.Request(url, headers={'BCOV-POLICY': config.BRIGHTCOVE_KEY} )
    xbmc.log('Fetching URL: {}'.format(url))
    res = urllib2.urlopen(req).read()
    data = json.loads(res)
    if live:
        return data['sources'][0]['src']
    else:
        url = ''
        for source in data.get('sources'):
            if (source.get('container') == 'M2TS' or 
                source.get('type') == 'application/vnd.apple.mpegurl'):
                if 'https' in source.get('src'):
                    url = source.get('src')
                    if url:
                        return url
            
        
        
        
            
            

def get_widevine_auth(drm_url):
    """ Parse DRM JSON and return license auth URL and manifest URL"""
    req = urllib2.Request(drm_url, headers={'BCOV-POLICY': config.BRIGHTCOVE_KEY} )
    xbmc.log('Fetching URL: {}'.format(drm_url))
    res = urllib2.urlopen(req).read()
    data = json.loads(res)
    for source in data['sources']:
        if 'com.widevine.alpha' in source['key_systems']:
            url = source['src']
            key = source['key_systems']['com.widevine.alpha']['license_url']
            return {'url': url, 'key': key}

