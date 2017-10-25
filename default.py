import os
import sys
import xbmc
import xbmcgui
import xbmcaddon
import drmhelper
from urlparse import parse_qsl

from aussieaddonscommon import utils

addon = xbmcaddon.Addon()
cwd = xbmc.translatePath(addon.getAddonInfo('path')).decode("utf-8")
BASE_RESOURCE_PATH = os.path.join(cwd, 'resources', 'lib')
sys.path.append(BASE_RESOURCE_PATH)

import menu  # noqa: E402
import play  # noqa: E402


def router(paramstring):
    """
    Router function that calls other functions depending on the
    provided paramstring
    """
    params = dict(parse_qsl(paramstring))
    if paramstring:
        if paramstring != 'content_type=video':
            if params['action'] == 'listcategories':
                if params['category'] == 'All Shows':
                    menu.make_series_list(paramstring)
                elif params['category'] == 'Live TV':
                    menu.make_live_list(paramstring)
                else:
                    menu.make_series_list(paramstring)
            elif params['action'] == 'listseries':
                menu.make_episodes_list(paramstring)
            elif params['action'] == 'listepisodes':
                play.play_video(params)
            elif params['action'] == 'listchannels':
                play.play_video(params)
            elif params['action'] == 'settings':
                xbmcaddon.Addon().openSettings()
            elif params['action'] == 'reinstall_widevine_cdm':
                drmhelper.get_widevinecdm()
            elif params['action'] == 'reinstall_ssd_wv':
                drmhelper.get_ssd_wv()
            elif params['action'] == 'sendreport':
                utils.user_report()
            elif params['action'] == 'update_ia':
                addon = drmhelper.get_addon(drm=True)
                if not drmhelper.is_ia_current(addon, latest=True):
                    if xbmcgui.Dialog().yesno(
                        'Upgrade?', ('Newer version of inputstream.adaptive '
                                     'available ({0}) - would you like to '
                                     'upgrade to this version?'.format(
                                        drmhelper.get_latest_ia_ver()))):
                        drmhelper.get_ia_direct(update=True, drm=True)
                else:
                    ver = addon.getAddonInfo('version')
                    utils.dialog_message('Up to date: Inputstream.adaptive '
                                         'version {0} installed and enabled.'
                                         ''.format(ver))
    else:
        menu.list_categories()


if __name__ == '__main__':
    router(sys.argv[2][1:])
