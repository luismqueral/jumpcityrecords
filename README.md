![jump city records](http://i.imgur.com/jgJVyBk.png)

Jump City Records is an experimental, open-source record label that produces and releases its albums through a series of python bots. It was designed by Luis Queral (http://luisquer.al) and engineered by Michiel Overtoom (http://www.michielovertoom.com/).

## Process

**When run, the script begins by randomly assigning the 
following variables:**
* Album Title
* Number of Tracks
* Title of Tracks
* Duration of Tracks

***

### Album Titles
Track titles are generated via the Wikipedia API from random article titles.
* ex. Stanydale
* ex. Serua (Fijian Communal Constituency, Fiji)

### Number of Tracks
Each album is assigned a random number of tracks. They are officially set at 3-8 tracks, although this can be changed in jumpcity.py settings.

### Track Titles:
Track titles are generated via the Wikipedia API from random article titles.
* ex. Yuuka Maeda
* ex. Tartu Town Hall

### Duration of Tracks:
Track durations are assigned randomly. They are officially set at being no shorter than 15 seconds and no longer than 6 minutes. Again this can be altered in jumpcity.py settings.

***

## Output
The audio created by Jump City Records is entirely sample-based. Samples range from field recordings, avant garde / noise albums, among many other sources. Most of the audio was downloaded from[archive.org](archive.org), in addition to assorted torrent trackers. At this time, jump City Records does not have the capability to attribute the samples used, but assume that the manner in which they are manipulated (and by nature of their genre), they would be indistinguishable.

### Sample file structure
The samples are organized in a directory of folders filled with a variety of audio formats (_assets). When run, the script selects one folder and three random 
audio samples within it. It places each of these audio files on top of each other in SoX, applies a chain of effects to each track, and exports the master track as a .flac. It will do this (x) times, determined by the script.

The file location for the output would be within a folder named _albums.

![graph](http://i.imgur.com/15q5w2M.png)

***

## Installation Instructions
This program has been tested on both Linux and OSX systems.

### Linux (Ubuntu 14.04)
```sudo apt-get install git python-cairo lame sox libsox-fmt-all libav-tools flac```
Installation is admittadly easiest on Linux machines, but be advised that Linux has inferior type rendering to OSX machines. As a result, the typography found on album covers generated via Ciaro on Linux machines will look strange compated to OSX. Not sure if there's a work around for this!

###  OSX
Installing on OSX yields higher quality graphical results, but can be a bit of a pain to install. No fear though, it is absolutely doable!

*A word of warning:* this will override the Apple-supplied version of Python with the 2.7.8 that Homebrew supplies, at least in Terminal sessions. I don't know what other consequences this causes, but as far as I can see, everything works as usual.

*We used a fresh install of Yosemite on an external USB disk to test out the following:*

```
- install Xcode, via the AppStore
- visit http://brew.sh, scroll down, copy the install command and paste and run it in a Terminal.
$ brew update
$ brew install opencore-amr libvorbis flac libsndfile libao lame ffmpeg
$ brew install sox
$ sox -n test.wav synth 440 fade 0 2 1
$ play test.wav

$ python -V
$ brew install python
$ brew linkapps
$ exit

- start Terminal again
$ python -V

- visit https://xquartz.macosforge.org, download the DMG, open it, run the package installer
- log out
- log in
- install the fonts 'Apercu' and 'Transport Medium' (not part of the jumpcity repository; the software will run OK without these fonts)
- open a Terminal
$ brew install py2cairo
$ cd ~
$ git clone https://github.com/luismqueral/jumpcityrecords.git
$ cd jumpcityrecords/src
$ python albumart.py
$ open output/*
$ mkdir ~/jumpcityrecords/_albums
$ mkdir ~/jumpcityrecords/_albums/Samples
- place at least 5 audio samples (with the audio format mp3, wav, aiff or flac) in the ~/jumpcityrecords/_albums/Samples folder.
$ python jumpcity.py
- see if it works. Feel free to Control-C after a while.

- install Gtk3+ as follows:
$ cd ~/jumpcityrecords/src
$ brew install pygobject3 gtk+3
$ mkdir -p ~/Library/LaunchAgents
$ cp /usr/local/Cellar/d-bus/1.8.8/org.freedesktop.dbus-session.plist ~/Library/LaunchAgents/
$ launchctl load -w ~/Library/LaunchAgents/org.freedesktop.dbus-session.plist
$ python randomdraw.py  (could take some time, XQuartz has to start too)
- resize the app window to refresh the album art
$ python jumpcity.py
```
**If you installed it correctly, you'll see something that looks like this this:**

![success](http://i.imgur.com/sbBhW11.gif)

***

### Example Album
You can view all of the Jump City Records releases here http://soundcloud.com/jumpcityrecords

![Example Album Art](http://i.imgur.com/75DspsO.png)

```
░ jump city records, Jim Brigden (2015-01-14 17.24.14)
░ generated by jumpcity.py

░ (https://github.com/luismqueral/jumpcityrecords)

01 Tongren Fenghuang Airport         2:11
02 Rava Rajputs                      1:47
03 Fountains of Wayne discography    0:26
04 CATS Eyes                         4:14
05 Mahuawan                          0:55
06 Trombe wall                       2:01
07 Solar eclipse of January 17, 101  1:43
08 Ronald Hughes                     2:00
09 Chuman/Humanzee                   1:38
10 Malek Baghi                       2:46

a project by:
 • Michiel Overtoom (http://www.michielovertoom.com/)
 • Luis Queral (http://luisquer.al)

view more at: http://soundcloud.com/jumpcityrecords
```

*Listen here:* https://soundcloud.com/jumpcityrecords/sets/111614-2349a

***

### Colophon

**Dependencies used**
- *SoX* http://sox.sourceforge.net/
- *Cairo* http://cairographics.org/pycairo/
 



