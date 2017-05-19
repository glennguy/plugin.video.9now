import os
import sys
import re
import traceback
import time
import unicodedata
import urllib
import urlparse
import textwrap
import xbmc
import xbmcgui
import config
import issue_reporter

pattern = re.compile("&(\w+?);")

# This is a throwaway variable to deal with a python bug with strptime:
#   ImportError: Failed to import _strptime because the import lockis
#   held by another thread.
throwaway = time.strptime('20140101', '%Y%m%d')


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
    log('Available streams are: {0}'.format(sorted_m3u_list))
    stream = sorted_m3u_list[qual]['URL']
    return stream


def make_url(d):
    pairs = []
    for k, v in d.iteritems():
        k = urllib.quote_plus(k)
        v = ensure_ascii(v)
        v = urllib.quote_plus(v)
        pairs.append("%s=%s" % (k, v))
    return "&".join(pairs)


def ensure_ascii(s):
    if isinstance(s, unicode):
        return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
    else:
        return s


def log(s):
    xbmc.log("[%s v%s] %s" % (config.NAME, config.VERSION, s),
             level=xbmc.LOGNOTICE)


def dialog_error(err=None):
    """Generate a list of lines for use in XBMC dialog"""
    content = []
    exc_type, exc_value, exc_tb = sys.exc_info()
    content.append("%s v%s Error" % (config.NAME, config.VERSION))
    content.append(str(exc_value))
    return content


def dialog_message(msg, title=None):
    if not title:
        title = "%s v%s" % (config.NAME, config.VERSION)
    # Add title to the first pos of the textwrap list
    content = textwrap.wrap(msg, 60)
    content.insert(0, title)
    return content


def get_platform():
    """ Work through a list of possible platform types and return the first
        match. Ordering of items is important as some match more thant one
        type.

        E.g. Android will match both Android and Linux
    """
    platforms = [
        "Android",
        "Linux.RaspberryPi",
        "Linux",
        "XBOX",
        "Windows",
        "ATV2",
        "IOS",
        "OSX",
        "Darwin",
    ]

    for platform in platforms:
        if xbmc.getCondVisibility('System.Platform.'+platform):
            return platform
    return "Unknown"


def get_xbmc_build():
    return xbmc.getInfoLabel("System.BuildVersion")


def get_xbmc_version():
    build = get_xbmc_build()
    # Keep the version number, and strip the rest
    version = build.split(' ')[0]
    return version


def get_xbmc_major_version():
    """ Return the major version number of the running XBMC
    """
    version = get_xbmc_version().split('.')[0]
    return int(version)


def log_xbmc_platform_version():
    """ Log our XBMC version and platform for debugging
    """
    version = get_xbmc_version()
    platform = get_platform()
    log("XBMC/Kodi %s running on %s" % (version, platform))


def get_file_dir():
    """ Make our addon working directory if it doesn't exist and
        return it.
    """
    filedir = os.path.join(xbmc.translatePath('special://temp/'),
                           config.ADDON_ID)
    if not os.path.isdir(filedir):
        os.mkdir(filedir)
    return filedir


def save_last_error_report(trace):
    """ Save a copy of our last error report
    """
    try:
        rfile = os.path.join(get_file_dir(), 'last_report_error.txt')
        with open(rfile, 'w') as f:
            f.write(trace)
    except:
        log("Error writing error report file")


def can_send_error(trace):
    """ Check to see if our new error message is different from the last
        successful error report. If it is, or the file doesn't exist, then
        we'll return True
    """
    try:
        rfile = os.path.join(get_file_dir(), 'last_report_error.txt')

        if not os.path.isfile(rfile):
            return True
        else:
            f = open(rfile, 'r')
            report = f.read()
            if report != trace:
                return True
    except:
        log("Error checking error report file")

    log("Not allowing error report. Last report matches this one")
    return False


def handle_error(msg, exc=None):
    traceback_str = traceback.format_exc()
    log(traceback_str)
    report_issue = False

    # Don't show any dialogs when user cancels
    if traceback_str.find('SystemExit') > 0:
        return

    d = xbmcgui.Dialog()
    if d:
        message = dialog_error(msg)

        # Work out if we should allow an error report
        send_error = can_send_error(traceback_str)

        # Some transient network errors we don't want any reports about
        if ((traceback_str.find('The read operation timed out') > 0) or
                (traceback_str.find('IncompleteRead') > 0) or
                (traceback_str.find('HTTP Error 404: Not Found') > 0)):
            send_error = False

        # Any non-fatal errors, don't allow issue reporting
        # if (isinstance(exc, BigPondException) or
        #        isinstance(exc, TelstraAuthException)):
        #    send_error = False

        if send_error:
            latest_version = issue_reporter.get_latest_version()
            version_string = '.'.join([str(i) for i in latest_version])
            if not issue_reporter.is_latest_version(config.VERSION,
                                                    latest_version):
                message.append("Your version of this add-on is outdated. "
                               "Please try upgrading to the latest version: "
                               "v%s" % version_string)
                d.ok(*message)
                return

            # Only report if we haven't done one already
            try:
                message.append("Would you like to automatically "
                               "report this error?")
                report_issue = d.yesno(*message)
            except:
                message.append("If this error continues to occur, "
                               "please report it to our issue tracker.")
                d.ok(*message)
        else:
            # Just show the message
            d.ok(*message)

    if report_issue:
        log("Reporting issue to GitHub...")
        issue_url = issue_reporter.report_issue(traceback_str)
        if issue_url:
            # Split the url here to make sure it fits in our dialog
            split_url = issue_url.replace('/xbmc', ' /xbmc')
            d.ok("%s v%s Error" % (config.NAME, config.VERSION),
                 "Thanks! Your issue has been reported to: %s" % split_url)
            # Touch our file to prevent more than one error report
            save_last_error_report(traceback_str)
