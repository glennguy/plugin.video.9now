# plugin.video.9now
Kodi add-on for Nine Network's 9now on demand catch-up service

## Requirements:

### Install the drm helper module [zip file](https://github.com/glennguy/script.module.drmhelper/archive/master.zip)

## Widevine DRM

Several programs are now protected with DRM, mainly big-ticket imported shows. Kodi 17/17.1 onwards is required to view DRM protected programs. Non-DRM protected shows are still watchable on Kodi 16.

For viewing protected shows you will need to have the inputstream-adaptive binary addon installed and enabled. The add-on will attempt to do this but at the moment it will only automatically happen with Windows and LibreELEC. For Linux you will need to either build it yourself or install it from a 3rd party repository. There is a 3rd party repository and pre-built binaries that you can use in the github repo here: https://github.com/vdrtuxnet/binary-repo . Installing the correct repo for your system and restarting Kodi should be enough, the add-on should then install inputstream.adaptive from there.

The remaining components needed are the Widevine Content Decryption Module and Single Sample Decrypter Module.

The add-on will detect whether you have these installed and if needed download them to the correct location. For LibreELEC/Windows/Mac this is only a small download but for Linux there will be a ~50MB download to get the widevinecdm module. The SSD comes from my reposistory. This add-on has not yet been tested on Mac, and I have not build any SSD modules for OSX however if you can supply it it should be fine.

## Installation:
Download the [zip](https://github.com/glennguy/plugin.video.9now/archive/master.zip) file and install through Kodi's interface

## Help

Visit us on the [Aussie Addon Slack channel](http://slack-invite.aussieaddons.com/)
