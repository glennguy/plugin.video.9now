# plugin.video.9now
Kodi add-on for Nine Network's 9now on demand catch-up service

#Requirements:

Several programs are now protected with DRM, mainly big-ticket imported shows. Kodi 17 Beta 6 is the minimum version that is compatible with DRM protected programs, Kodi 17 Beta 7 is recommended. Non-DRM protected shows should still be fine for Kodi 14 onwards.

You will need to have the inputstream-adaptive binary addon installed and enabled. It is packaged with Windows and LibreELEC installations. For Linux distrubutions you will need to either build it yourself or install it from a repository. There is also this unofficial source for pre-built binaries: https://github.com/vdrtuxnet/kodi-17.binary.addons

The remaining components needed are the Widevine Content Decryption Module and Single Sample Decrypter Module.

The add-on will detect whether you have these installed and if needed download them to the correct location. For LibreELEC/Windows/Mac this is only a small download but for Linux there will be a ~50MB download to get the widevinecdm module. The SSD comes from my reposistory. This routine is not yet tested with Mac, hopefully it works.

#Installation:
Download the zip file and install through Kodi's interface

