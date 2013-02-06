# watched

Automatically mark TV shows as watched on [watched.li][1] when you watched them.

### Plan of attack

1. Query QuickTime Player for the currently open video file.
2. Extract information on the TV show episode from that.
3. Find a matching thing on [watched.li][1] and mark it as watched.
4. Build a proper app from this mess.

### Prerequisites

Tested on Mac OS X 10.8.2 Mountain Lion.

    $ sudo easy_install pip
    $ sudo pip install BeautifulSoup
    $ sudo pip install guessit
    $ sudo pip install osascript

Running *watched.py* should now mark the video currently playing in QuickTime
as watched on [watched.li][1]. Credentials are shared with [shores][2], so make
sure you have that properly configured as well. Yeah, it's a mess.


[1]: http://watched.li
[2]: https://github.com/neonichu/shores
