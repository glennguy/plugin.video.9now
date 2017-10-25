import classes
import config
import json

from aussieaddonscommon import session


def fetch_url(url, headers={}):
    """
    Use custom session to grab URL and return the text
    """
    with session.Session(force_tlsv1=True) as sess:
        res = sess.get(url, headers=headers)
        return res.text


def list_series():
    """
    Create and return list of series objects
    """
    res = fetch_url(config.TVSERIES_URL)
    data = json.loads(res)
    listing = []
    for show in data['items']:
        for season in reversed(show['containsSeason']):
            s = classes.series()
            s.multi_season = len(show['containsSeason']) > 1
            s.season_slug = season['slug']
            s.series_name = show['name']
            s.season_name = season['name']
            s.series_slug = season['partOfSeries']['slug']
            s.fanart = show['image']['sizes']['w1920']
            s.thumb = season['image']['sizes']['w480']
            s.genre = season['genre']['name']
            s.title = s.get_title()
            listing.append(s)
    return listing


def list_genres():
    """
    Create and return list of genre objects
    """
    res = fetch_url(config.GENRES_URL)
    data = json.loads(res)
    listing = []
    for genre in data['items']:
        g = classes.genre()
        g.fanart = (genre['image']['sizes']['w1920'])
        g.thumb = (genre['image']['sizes']['w480'])
        g.genre_slug = genre['slug']
        g.title = genre['name']
        listing.append(g)
    return listing


def list_episodes(params):
    """
    Create and return list of episode objects
    """
    url = config.EPISODEQUERY_URL.format(
        params['series_slug'], params['season_slug'])
    res = fetch_url(url)
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
            e.drm = episode['video']['drm'] is True
            listing.append(e)
    return listing


def list_live(params):
    """
    Create and return list of channel objects
    """
    res = fetch_url(config.LIVETV_URL)
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
    """Parse live tv JSON and return stream url
    """
    res = fetch_url(url, headers={'BCOV-POLICY': config.BRIGHTCOVE_KEY})
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
    """
    Parse DRM JSON and return license auth URL and manifest URL
    """
    res = fetch_url(drm_url, headers={'BCOV-POLICY': config.BRIGHTCOVE_KEY})
    data = json.loads(res)
    for source in data['sources']:
        if 'com.widevine.alpha' in source['key_systems']:
            url = source['src']
            key = source['key_systems']['com.widevine.alpha']['license_url']
            return {'url': url, 'key': key}
