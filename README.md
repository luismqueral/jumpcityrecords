```

    /$$$$$ /$$   /$$ /$$      /$$ /$$$$$$$                            
   |__  $$| $$  | $$| $$$    /$$$| $$__  $$                           
      | $$| $$  | $$| $$$$  /$$$$| $$  \ $$                           
      | $$| $$  | $$| $$ $$/$$ $$| $$$$$$$/                           
 /$$  | $$| $$  | $$| $$  $$$| $$| $$____/                            
| $$  | $$| $$  | $$| $$\  $ | $$| $$                                 
|  $$$$$$/|  $$$$$$/| $$ \/  | $$| $$                                 
 \______/  \______/ |__/     |__/|__/                                 
                                                                      
                                                                      
                                                                      
  /$$$$$$  /$$$$$$ /$$$$$$$$ /$$     /$$                              
 /$$__  $$|_  $$_/|__  $$__/|  $$   /$$/                              
| $$  \__/  | $$     | $$    \  $$ /$$/                               
| $$        | $$     | $$     \  $$$$/                                
| $$        | $$     | $$      \  $$/                                 
| $$    $$  | $$     | $$       | $$                                  
|  $$$$$$/ /$$$$$$   | $$       | $$                                  
 \______/ |______/   |__/       |__/                                  
                                                                      
                                                                      
                                                                      
 /$$$$$$$  /$$$$$$$$  /$$$$$$   /$$$$$$  /$$$$$$$  /$$$$$$$   /$$$$$$ 
| $$__  $$| $$_____/ /$$__  $$ /$$__  $$| $$__  $$| $$__  $$ /$$__  $$
| $$  \ $$| $$      | $$  \__/| $$  \ $$| $$  \ $$| $$  \ $$| $$  \__/
| $$$$$$$/| $$$$$   | $$      | $$  | $$| $$$$$$$/| $$  | $$|  $$$$$$ 
| $$__  $$| $$__/   | $$      | $$  | $$| $$__  $$| $$  | $$ \____  $$
| $$  \ $$| $$      | $$    $$| $$  | $$| $$  \ $$| $$  | $$ /$$  \ $$
| $$  | $$| $$$$$$$$|  $$$$$$/|  $$$$$$/| $$  | $$| $$$$$$$/|  $$$$$$/
|__/  |__/|________/ \______/  \______/ |__/  |__/|_______/  \______/ 
                                                                      
```

Jump City Records is an experimental, open-source record label that produces and releases its albums through a series of python bots. It was designed by Luis Queral (http://luisquer.al) and engineered by Michiel Overtoom (http://www.michielovertoom.com/).

## Process

**When run, the script begins by randomly assigning the 
following variables:**
* Album Title
* Number of Tracks
* Title of Tracks
* Duration of Tracks

——————————————————————————————————————————

**Album Title:** album titles are 8 character, alphanumeric 
combinations with both upper and lowercase characters.
ex. 2Pgiw3tW
ex. TkQ2pz2k

**Number of Tracks:** each album should contain anywhere from 
3-23 tracks.
ex. Yuuka Maeda
ex. Tartu Town Hall

**Track Titles:** generated via the Wikipedia API from random article titles.

**Duration of Tracks:** each track should be no shorter than 15 seconds and no longer than 15 minutes.

The audio created by Jump City Records is entirely sample-based. The samples are organized in a directory of 
folders filled with a variety of audio formats (_assets). When run, the script selects one folder and three random 
audio samples within it. It places each of these audio files on top of each other in SoX, applies a chain of effects to each track, and exports the master track as a .flac. It will do this (x) times, determined by the script.
The file location for the output would be within a folder named _albums.

![graph](http://i.imgur.com/15q5w2M.png)

## Installing on Linux (Ubuntu 14.04)
```sudo apt-get install git python-cairo lame sox libsox-fmt-all libav-tools flac```

## Installing on OSX
Installing software for running jumpcity on OSX Yosemite:

A word of warning: this will override the Apple-supplied version of Python with the 2.7.8 that Homebrew supplies, at least in Terminal sessions. I don't know what other consequences this causes, but as far as I can see, everything works as usual.

I used a fresh install of Yosemite on an external USB disk to test out the following:

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
```

### Example Album
You can view all of the Jump City Records releases here http://jumpcityrecords.bandcamp.com

![Example Album Art](https://i1.sndcdn.com/artworks-000097400822-xhvfd3-t500x500.jpg)

░ [11.16.14 / 23:49]

01 Pervomaiske 3:04

02 Alexander Johnston 1:10

03 Petter Rudi 3:48

04 Living Planet Report 4:21

05 Andrea Chenier 2:54

*Listen here:* https://soundcloud.com/jumpcityrecords/sets/111614-2349a



### Colophon
- *SoX* http://sox.sourceforge.net/
- *Cairo* http://cairographics.org/pycairo/


