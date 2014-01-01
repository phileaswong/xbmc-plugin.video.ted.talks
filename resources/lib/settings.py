"""
Contains constants that we initialize to the correct values at runtime.
Should be usable as a testing shim.
"""
import model.language_mapping as language_mapping
import pickle
import os

__plugin_id__ = 'plugin.video.ted.talks'
__current_search__ = 'current_search'
__current_search_results__ = 'current_search_results'

profile_path = None
username = 'Ted'
password = 'Ted'
download_mode = True
download_path = '/tmp/'
video_quality = 3
enable_subtitles = True
xbmc_language = 'English'
subtitle_language = 'en'

def init():
    import xbmc, xbmcaddon
    addon = xbmcaddon.Addon(id=__plugin_id__)
    global profile_path, username, password, download_mode, download_path, video_quality, enable_subtitles, xbmc_language, subtitle_language
    profile_path = xbmc.translatePath(addon.getAddonInfo('profile') ).decode("utf-8")
    username = addon.getSetting('username')
    password = addon.getSetting('password')
    download_mode = addon.getSetting('downloadMode')
    download_path = addon.getSetting('downloadPath')
    video_quality = addon.getSetting('video_quality')
    enable_subtitles = addon.getSetting('enable_subtitles')
    xbmc_language = xbmc.getLanguage()
    subtitle_language = addon.getSetting('subtitle_language')

def get_subtitle_languages():
    '''
    Returns list of ISO639-1 language codes in order of preference,
    or None if disabled.
    '''
    if enable_subtitles == 'false':
        return None
    if not subtitle_language.strip():
        code = language_mapping.get_language_code(xbmc_language)
        return [code] if code else None
    else:
        return [code.strip() for code in subtitle_language.split(',') if code.strip()]

def __get_profile_path__(*segments):
    return os.path.join(profile_path, *segments)

def set_current_search(value):
    with open(__get_profile_path__('current_search'), 'w') as f:
        f.write(value)
    
def get_current_search():
    current_search_file = __get_profile_path__('current_search')
    if not os.path.exists(current_search_file):
        return ''
    with open(current_search_file, 'r') as f:
        return f.read()

def set_current_search_results(value):
    with open(__get_profile_path__('current_search_items'), 'w') as f:
        pickle.dump(value, f)
    
def get_current_search_results():
    with open(__get_profile_path__('current_search_items'), 'r') as f:
        return pickle.load(f)
