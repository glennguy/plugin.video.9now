import xbmcgui
import xbmcaddon
import xbmcplugin
import comm
import config
import sys
import urllib2
import urlparse
import drmhelper

from aussieaddonscommon import utils

_url = sys.argv[0]
_handle = int(sys.argv[1])


def parse_m3u8(data, m3u8_path, qual=-1):
    """
    Parse the retrieved m3u8 stream list into a list of dictionaries
    then return the url for the highest quality stream.
    """
    ver = 0
    if '#EXT-X-VERSION:3' in data:
        ver = 3
        data.remove('#EXT-X-VERSION:3')
    if '#EXT-X-VERSION:4' in data:
        ver = 4
        data.remove('#EXT-X-VERSION:4')
    count = 1
    m3u_list = []
    while count < len(data):
        if ver == 3 or ver == 0:
            line = data[count]
            line = line.strip('#EXT-X-STREAM-INF:')
            line = line.strip('PROGRAM-ID=1,')
            if 'CODECS' in line:
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
            for value in values:
                if value.startswith('BANDWIDTH'):
                    bw = value
                elif value.startswith('RESOLUTION'):
                    res = value
            url = urlparse.urljoin(m3u8_path, data[count + 1])
            m3u_list.append(
                dict([bw.split('='), res.split('='), ['URL', url]]))
            count += 3

    sorted_m3u_list = sorted(m3u_list, key=lambda k: int(k['BANDWIDTH']))
    utils.log('Available streams are: {0}'.format(sorted_m3u_list))
    stream = sorted_m3u_list[qual]['URL']
    return stream


def play_video(params):
    """
    Determine content and pass url to Kodi for playback
    """
    if params['action'] == 'listchannels':
        json_url = config.BRIGHTCOVE_DRM_URL.format(config.BRIGHTCOVE_ACCOUNT,
                                                    params['id'])
        url = comm.get_stream(json_url, live=True)
        play_item = xbmcgui.ListItem(path=url)

    elif params['drm'] == 'True':
        if xbmcaddon.Addon().getSetting('ignore_drm') == 'false':
            if not drmhelper.check_inputstream():
                return
        acc = config.BRIGHTCOVE_ACCOUNT
        drm_url = config.BRIGHTCOVE_DRM_URL.format(acc, params['id'])
        widevine = comm.get_widevine_auth(drm_url)
        url = widevine['url']
        play_item = xbmcgui.ListItem(path=url)
        play_item.setProperty('inputstream.adaptive.manifest_type',
                              'mpd')
        play_item.setProperty('inputstream.adaptive.license_type',
                              'com.widevine.alpha')
        play_item.setProperty(
            'inputstream.adaptive.license_key',
            widevine['key']+('|Content-Type=application%2F'
                             'x-www-form-urlencoded|A{SSM}|'))
    else:
        json_url = config.BRIGHTCOVE_DRM_URL.format(config.BRIGHTCOVE_ACCOUNT,
                                                    params['id'])
        m3u8 = comm.get_stream(json_url)
        data = urllib2.urlopen(m3u8).read().splitlines()
        url = parse_m3u8(data, m3u8_path=m3u8)
        play_item = xbmcgui.ListItem(path=url)

    xbmcplugin.setResolvedUrl(_handle, True, play_item)
