#!/usr/bin/env python

import ConfigParser
import osascript
import os.path
import sys

from guessit import guess_file_info

sys.path.append('./vendor/shores')
from watchedli import WatchedLi

# Shared with shores
def get_credentials():
    cfg_path = os.path.expandvars('$HOME/.shores/config')
    cfg = ConfigParser.ConfigParser()
    cfg.read(cfg_path)
    watchedLiUser = cfg.get('shores', 'watchedLiUser')
    watchedLiPass = cfg.get('shores', 'watchedLiPass')
    return (watchedLiUser, watchedLiPass)

if __name__ == '__main__':
    wd = os.path.dirname(sys.argv[0])
    video_path = osascript.osascript(os.path.join(wd, 'QuickTimePlayer_Log.scpt'))
    if not video_path:
        print 'Could not get video from QuickTime Player.'
        sys.exit(1)

    video_info = guess_file_info(video_path, 'autodetect')
    if not video_info.has_key('type') or video_info['type'] != 'episode':
        print 'QuickTime Player is not playing a TV show episode.'
        sys.exit(1)

    show = video_info['series']
    episode_id = 'S%02dE%02d' % (int(video_info['season']),
            int(video_info['episodeNumber']))

    # FIXME: Workaround for 'Rizzoli & Isles', need a better solution
    show = show.replace('and ', '')

    credentials = get_credentials()
    client = WatchedLi(credentials[0], credentials[1])
    episodes = client.episodes(show)
    for episode in episodes:
        if episode['id'] == episode_id:
            try:
                if client.markEpisode(episode):
                    print 'Done.'
                    sys.exit(0)
            except Exception, e:
                print e
                sys.exit(1)

    print 'Failure.'
    sys.exit(1)
