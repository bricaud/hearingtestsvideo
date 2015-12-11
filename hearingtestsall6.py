#! /usr/bin/python

#
# Qt example for VLC Python bindings
# Copyright (C) 2009-2010 the VideoLAN team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
#

import sys
import os.path
import vlc
from PyQt4 import QtGui, QtCore
from random import random
import json
import time

class Player(QtGui.QMainWindow):
    """A simple Media Player using VLC and Qt
    """
    def __init__(self, master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.setWindowTitle("Tests audio")

        # creating a basic vlc instance
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()

        self.createUI()
        self.isPaused = False
        self.Scenario1()
        self.Stop()
        n_rand = random()
        if n_rand<0.5:
            self.Scenario1()
            self.Stop()



    def createUI(self):
        """Set up the user interface, signals & slots
        """
        self.widget = QtGui.QWidget(self)
        self.setCentralWidget(self.widget)
        ##########
        # Parameters to be saved for the record
        seed=random()
        localtime = time.asctime( time.localtime(time.time()) )
        datadic = {
                'Session time': localtime,
                'Seed:': seed,
                }
        with open("hearsessions.json","a") as file_save:
            json.dump(datadic,file_save)

        # In this widget, the video will be drawn
        if sys.platform == "darwin": # for MacOS
            self.videoframe = QtGui.QMacCocoaViewContainer(0)
        else:
            self.videoframe = QtGui.QFrame()
        self.palette = self.videoframe.palette()
        self.palette.setColor (QtGui.QPalette.Window,
                               QtGui.QColor(0,0,0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)


        # DISPLAY BOX
        self.hbuttonbox = QtGui.QHBoxLayout()
        #self.textbox = QtGui.QHBoxLayout()

        # WIDGETS TO DISPLAY
        self.label = QtGui.QLabel("Scenario 1")
        #self.textbox = QtGui.QHBoxLayout()
        #self.textbox.addWidget(self.label)
        self.playbutton = QtGui.QPushButton("Play")
        self.stopbutton = QtGui.QPushButton("Stop")
        self.Scenario1button = QtGui.QPushButton("File 1")
        self.Scenario2button = QtGui.QPushButton("File 2")
        self.switchbutton = QtGui.QPushButton("SwitchTrack")
        self.labelend = QtGui.QLabel("Version 1")
        
        

        # PUT THE WIDGETS IN THE BOX
        self.hbuttonbox.addWidget(self.label)
        self.hbuttonbox.addWidget(self.playbutton)
        #self.hbuttonbox.addWidget(self.stopbutton)
        #self.hbuttonbox.addWidget(self.Scenario1button)
        #self.hbuttonbox.addWidget(self.Scenario2button)
        #self.hbuttonbox.addWidget(self.switchbutton)
        #self.textbox.addWidget(self.labelend)
        self.hbuttonbox.addWidget(self.labelend)
        self.hbuttonbox.addWidget(self.switchbutton)

        # CONNECT THE BUTTON WITH THEIR ACTION
        # Play pause
        self.connect(self.playbutton, QtCore.SIGNAL("clicked()"),
                     self.PlayPause)
        # Stop
        self.connect(self.stopbutton, QtCore.SIGNAL("clicked()"),
                     self.Stop)
        
        # Video 1
        self.connect(self.Scenario1button, QtCore.SIGNAL("clicked()"), self.Scenario1)
         

        # Video 2
        self.connect(self.Scenario2button, QtCore.SIGNAL("clicked()"),self.Scenario2)
        

        # Switch Version
        self.connect(self.switchbutton, QtCore.SIGNAL("clicked()"),
                     self.SwitchAudioTrack)

        
        
        # ORGANISE THE GUI WITH A VIDEOFRAME AND A BUTTON BOX
        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        #self.vboxlayout.addWidget(self.positionslider)
        #self.vboxlayout.addLayout(self.textbox)
        self.vboxlayout.addLayout(self.hbuttonbox)

        self.widget.setLayout(self.vboxlayout)

        # ACTIONS IN THE MENU AND DEFINED WITH SHORTCUTS
        open1 = QtGui.QAction("&Open", self)
        self.connect(open1, QtCore.SIGNAL("triggered()"), self.OpenFile)
        exit = QtGui.QAction("&Exit", self)
        self.connect(exit, QtCore.SIGNAL("triggered()"), sys.exit)

        actionPlay1 = QtGui.QAction("&Scenario 1",self)
        actionPlay1.setShortcut(QtGui.QKeySequence("1"))
        #self.actionExit.setStatusTip(_('Close application'))
        self.connect(actionPlay1, QtCore.SIGNAL("triggered()"),self.Scenario1)
       
        actionPlay2 = QtGui.QAction("&Scenario 2",self)
        actionPlay2.setShortcut(QtGui.QKeySequence("2"))
        #self.actionExit.setStatusTip(_('Close application'))
        self.connect(actionPlay2, QtCore.SIGNAL("triggered()"),self.Scenario2)
        
        actionSwitch = QtGui.QAction("&Switch Track",self)
        actionSwitch.setShortcut(QtGui.QKeySequence("b"))
        #self.actionExit.setStatusTip(_('Close application'))
        self.connect(actionSwitch, QtCore.SIGNAL("triggered()"),self.SwitchAudioTrack)

        actionPlayPause = QtGui.QAction("&Play Pause",self)
        actionPlayPause.setShortcut(QtGui.QKeySequence("SPACE"))
        #self.actionExit.setStatusTip(_('Close application'))
        self.connect(actionPlayPause, QtCore.SIGNAL("triggered()"),self.PlayPause)

        actionLoop = QtGui.QAction("&Loop",self)
        actionLoop.setShortcut(QtGui.QKeySequence("q"))
        #self.actionExit.setStatusTip(_('Close application'))
        self.connect(actionLoop, QtCore.SIGNAL("triggered()"),self.Loop)


        menubar = self.menuBar()
        filemenu = menubar.addMenu("&File")
        filemenu.addAction(open1)
        filemenu.addSeparator()
        filemenu.addAction(exit)
        filemenu.addAction(actionPlay1)
        filemenu.addAction(actionPlay2)
        filemenu.addAction(actionSwitch)
        filemenu.addAction(actionPlayPause)
        filemenu.addAction(actionLoop)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"),
                     self.updateUI)

    def PlayPause(self):
        """Toggle play/pause status
        """
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText("Play")
            self.isPaused = True
            #self.labelend.setText("bla")
        else:
            if self.mediaplayer.play() == -1:
                #self.labelend.setText("bli")
                self.OpenFile()
                return
            self.mediaplayer.play()
            if self.labelend.text()=="Version 2":
                while vlc.libvlc_audio_get_track(self.mediaplayer)!=2:
                    vlc.libvlc_audio_set_track(self.mediaplayer, 2)
                self.labelend.setText("Version 2")
                #self.labelend.setText("blo")
            else:
                while vlc.libvlc_audio_get_track(self.mediaplayer)!=1:
                    vlc.libvlc_audio_set_track(self.mediaplayer, 1)
                self.labelend.setText("Version 1")
                #self.labelend.setText("blu")
            self.playbutton.setText("Pause")
            self.timer.start()
            self.isPaused = False
            self.resize(1280, 720)

    def Stop(self):
        """Stop player
        """
        self.mediaplayer.stop()
        self.playbutton.setText("Play")

    def Scenario1(self):
        """ Read Scenario file
        """
        if self.labelend.text()=="Version 1":

            self.mediaplayer.stop()
            self.OpenFile('Dyn1_Spa_Test.mkv')
            while vlc.libvlc_audio_get_track(self.mediaplayer)!=2:
                vlc.libvlc_audio_set_track(self.mediaplayer, 2)
            #else :
            #    self.OpenFile('MVI_1124.AVI')
            self.setWindowTitle("Version 2")
            self.label.setText("Scenario 1")
            self.labelend.setText("Version 2")
            self.resize(1280, 720)
        elif self.labelend.text()=="Version 2":
            self.mediaplayer.stop()
            #self.OpenFile('MVI_1124.AVI')
            self.OpenFile('Dyn1_Spa_Test.mkv')
            while vlc.libvlc_audio_get_track(self.mediaplayer)!=1:
                vlc.libvlc_audio_set_track(self.mediaplayer, 1)
            self.setWindowTitle("Version 2")
            self.label.setText("Scenario 1")
            self.labelend.setText("Version 1")
            self.resize(1280, 720)
        else:
            self.mediaplayer.stop()
            self.OpenFile('Dyn1_Spa_Test.mkv')
            #else :
            #    self.OpenFile('MVI_1124.AVI')
            self.setWindowTitle("Version 1")
            self.label.setText("Scenario 1")
            self.labelend.setText("Version 1")
            self.resize(1280, 720)

    def Scenario2(self):
        """ Read Scenario file
        """
        self.mediaplayer.stop()
        #self.OpenFile('MVI_1124.AVI')
        self.OpenFile('test_multi.mkv')
        self.setWindowTitle("Version 2")
        self.label.setText("Scenario 2")
        self.labelend.setText("Version 1")
        self.resize(1280, 720)

    def OpenFile(self, filename=None):
        """Open a media file in a MediaPlayer
        """
        if filename is None:
            filename = QtGui.QFileDialog.getOpenFileName(self, "Open File", os.path.expanduser('~'))
        if not filename:
            return

        # create the media
        if sys.version < '3':
            filename = unicode(filename)
        self.media = self.instance.media_new(filename)
        # put the media in the media player
        self.mediaplayer.set_media(self.media)

        # parse the metadata of the file
        self.media.parse()
        # set the title of the track as window title
        #self.setWindowTitle(self.media.get_meta(0))

        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if sys.platform.startswith('linux'): # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32": # for Windows
            self.mediaplayer.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin": # for MacOS
            self.mediaplayer.set_nsobject(self.videoframe.winId())
        self.PlayPause()

    def SwitchAudioTrack(self):
        """Switch the Version
        """
        nb_tracks = vlc.libvlc_audio_get_track_count(self.mediaplayer)
        track_Id = vlc.libvlc_audio_get_track(self.mediaplayer)
        if nb_tracks<2:
            return
        #self.PlayPause()
        self.mediaplayer.pause()
        if track_Id==1:
            while vlc.libvlc_audio_get_track(self.mediaplayer)!=2:
                vlc.libvlc_audio_set_track(self.mediaplayer, 2)
            self.labelend.setText("Version 2")
        else:
            while vlc.libvlc_audio_get_track(self.mediaplayer)!=1:
                vlc.libvlc_audio_set_track(self.mediaplayer, 1)
            self.labelend.setText("Version 1")
        #self.PlayPause()
        self.mediaplayer.play()
        track_Id = vlc.libvlc_audio_get_track(self.mediaplayer)
        if track_Id==1:
            self.labelend.setText("Version 1")
        else:
            self.labelend.setText("Version 2")

    def Loop(self):
        """ Loop the video
        """
        self.label.setText("Scenario boucle")

    def setVolume(self, Volume): #NOT USED HERE
        """Set the volume
        """
        self.mediaplayer.audio_set_volume(Volume)

    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position
        #self.positionslider.setValue(self.mediaplayer.get_position() * 1000)

        if not self.mediaplayer.is_playing():
            # no need to call this function if nothing is played
            self.timer.stop()
            if not self.isPaused:
                # after the video finished, the play button stills shows
                # "Pause", not the desired behavior of a media player
                # this will fix it
                self.Stop()
                self.resize(640, 480)
                if self.label.text()=="Scenario boucle":
                    self.PlayPause()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    player = Player()
    player.show()
    player.resize(640, 480)
    #player.set_fullscreen(True)   
    #player.OpenFile('MVI_1321.AVI')
    sys.exit(app.exec_())
