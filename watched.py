#!/usr/bin/env python

import ConfigParser
import osascript
import os.path
import sys

from guessit import guess_file_info

wd = os.path.dirname(sys.argv[0])
sys.path.append(os.path.join(wd, 'vendor/shores'))
from watchedli import WatchedLi

def debug(thing):
    #print thing
    return

# Shared with shores
def get_config():
    cfg_path = os.path.expandvars('$HOME/.shores/config')
    cfg = ConfigParser.ConfigParser(defaults={'videoplayer': 'QuickTimePlayer'})
    cfg.read(cfg_path)
    return cfg

def get_credentials():
    cfg = get_config()
    watchedLiUser = cfg.get('shores', 'watchedLiUser')
    watchedLiPass = cfg.get('shores', 'watchedLiPass')
    return (watchedLiUser, watchedLiPass)

def get_videoplayer():
    cfg = get_config()
    return cfg.get('watched', 'videoPlayer')

if __name__ == '__main__':
    video_player = get_videoplayer()
    debug(video_player)

    video_path = osascript.osascript(os.path.join(wd, '%s_Log.scpt' % video_player))
    if not video_path:
        print 'Could not get video from %s.' % video_player
        sys.exit(1)

    video_info = guess_file_info(video_path, 'autodetect')
    if not video_info.has_key('type') or video_info['type'] != 'episode':
        debug(video_info)
        print '%s is not playing a TV show episode.' % video_player
        sys.exit(1)

    show = video_info['series']
    episode_id = 'S%02dE%02d' % (int(video_info['season']),
            int(video_info['episodeNumber']))
    debug(show + ' ' + episode_id)

    # FIXME: Workaround for 'Rizzoli & Isles', need a better solution
    show = show.replace('and ', '')

    credentials = get_credentials()

    try:
        client = WatchedLi(credentials[0], credentials[1])
        episodes = client.episodes(show)
    except BaseException, e:
        print e
        sys.exit(1)

    for episode in episodes:
        if episode['id'] == episode_id:
            debug('marking ' + episode['wid'])
            try:
                if client.markEpisode(episode):
                    print 'Done.'
                    sys.exit(0)
            except Exception, e:
                print e
                sys.exit(1)

    print 'Failure.'
    sys.exit(1)
