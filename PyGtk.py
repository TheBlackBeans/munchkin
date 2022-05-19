#!/usr/bin/python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from threading import Thread

class MainLoop(Thread):
    def __init__(self):
        Thread.__init__(self)
    def StopMain(self):
        Gtk.main_quit()
    def run(self):
        Gtk.main()

class MainWindow(Gtk.Window):
    def __init__(self,title='Window',border=1):
        Gtk.Window.__init__(self,title=title)
        self.set_border_width(border)
        self.elements = {}
        self.connect("delete-event",Gtk.main_quit)
        self.IsStarted = False
    def create(self,what,**kwargs):
        exec('self.elements[len(self.elements) + 1] = Gtk.%s(**kwargs)' % what)
        uuid = len(self.elements)
        return self.elements[uuid]
