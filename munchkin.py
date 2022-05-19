#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'BlackBeans'
__copyright__ = 'BeansBoxⓡ ⓒ'

import xml.etree.ElementTree as ET
from PyGtk import MainLoop, MainWindow
import PyGtk
import random
import ccmc

cfgfile='munchkin.xml'

tree = ET.parse(cfgfile)
root = tree.getroot()

objects, races, kits = root.getchildren()[0], root.getchildren()[1], root.getchildren()[2]


class entity:
    def __init__(self,level):
        self.level = level
        self.strengh = self.level
    def getLevel(self):
        return self.level
    def setLevel(self,x):
        self.level = x
    def addLevel(self,x=1):
        self.level += x
    def removeLevel(self,x=1):
        if self.level > 1:
            self.level -= 1
            return True
        return False
    def getStrengh(self):
        return self.strengh
    def setStrengh(self,x):
        self.strengh = x
    def addStrengh(self,x=1):
        self.strengh += x
    def removeStrengh(self,x=1):
        if self.strengh > self.level:
            self.strengh -= x
        else:
            self.strengh = self.level

class player(entity):
    def __init__(self,name,index,level=1):
        entity.__init__(self,level)
        self.name = name
        self.hand = 2
        self.race, self.kit = 'Humain', None
        self.objects = {}
        self.index = index
    def getName(self):
        return self.name
    def getHand(self):
        return self.hand
    def checkHand(self,x):
        if self.getHand() >= x:
            return True
        return False
    def removeHand(self,x=1):
        if self.checkHand(x):
            self.hand -= x
    def addHand(self,x=1):
        if self.hand + x < 3:
            self.hand += x
    def setHand(self,x):
        self.hand = 2
    def setRace(self,race):
        self.race = race
    def setKit(self,kit):
        self.kit = kit
    def unsetRace(self,useless=None):
        self.race = 'Humain'
    def unsetKit(self,useless=None):
        self.kit = None
    def getRace(self):
        return self.race
    def getKit(self):
        return self.kit
    def addObject(self,_object):
        self.objects[_object] = False
    def setObject(self,_object):
        self.objects[_object] = True
    def unsetObject(self,_object):
        self.objects[_object] = False
    def getObjectStatus(self,_object):
        if _object in self.objects.keys():
            return self.objects[_object]
        else:
            return None
    def removeObject(self,_object):
        self.objects.pop(_object)
    def getObjects(self):
        return self.objects.keys()
    def getIndex(self):
        return self.index

class monster(entity):
    def __init__(self,level,effect,deatheffect):
        entity.__init__(self,level)
        self.effect = effect
        self.deatheffect = deatheffect
    def getEffect(self):
        return self.effect
    def getDeatheffect(self):
        return self.deatheffect

selected_player = None

def winner_popup(parent, message):
    dialogWindow = PyGtk.Gtk.MessageDialog(parent, 0, PyGtk.Gtk.MessageType.INFO, PyGtk.Gtk.ButtonsType.OK, message)
    dialogWindow.format_secondary_text("a gagné encore une fois à Munchkin")
    dialogWindow.run()
    dialogWindow.destroy()
    
def get_name(parent, message):
    dialogWindow = PyGtk.Gtk.MessageDialog(parent,
                          PyGtk.Gtk.DialogFlags.MODAL | PyGtk.Gtk.DialogFlags.DESTROY_WITH_PARENT,
                          PyGtk.Gtk.MessageType.QUESTION,
                          PyGtk.Gtk.ButtonsType.OK_CANCEL,
                          message)

    dialogBox = dialogWindow.get_content_area()
    userEntry = PyGtk.Gtk.Entry()

    dialogBox.pack_end(userEntry, False, False, 0)

    dialogWindow.show_all()
    response = dialogWindow.run()
    text = userEntry.get_text() 
    dialogWindow.destroy()
    if response == PyGtk.Gtk.ResponseType.OK:
        return text
    else:
        return None        

players = []
playerslist = PyGtk.Gtk.ListStore(str,str,str,int,int,int) #name race class level strengh free-hand    

def addPlayer(widget,name=''):
    if not name:
        name = get_name(window,'Choisissez le nom')
    for i in players:
        if name == i.getName():
            return
    if name:
        players.append(player(name,len(players)))
        playerslist.append([players[-1].getName(),players[-1].getRace(),players[-1].getKit(),players[-1].getLevel(),players[-1].getStrengh(),players[-1].getHand()])
        treeview.set_model(playerslist)
        window.show_all()

def reset_playerslist():
    playerslist.clear()
    for player in players:
        playerslist.append([player.getName(),player.getRace(),player.getKit(),player.getLevel(),player.getStrengh(),player.getHand()])

def refresh():
    if selected_player:
        a = selected_player.getIndex()
    reset_playerslist()
    if selected_player:
        treeview.set_cursor(PyGtk.Gtk.TreePath(a))
    
def removePlayer(widget):
    if selected_player:
        players.remove(selected_player)
        reset_playerslist()
        treeview.set_model(playerslist)
        window.show_all()
        
def addLevel(widget):
    if not selected_player:
        return
    selected_player.addLevel()
    selected_player.addStrengh()
    refresh()
    if selected_player.getLevel() >= 10:
        winner_popup(window,selected_player.getName())
    
def removeLevel(widget):
    if not selected_player:
        return
    if selected_player.removeLevel():
        selected_player.removeStrengh()
    refresh()

def addStrengh(widget):
    if not selected_player:
        return
    selected_player.addStrengh()
    refresh()
    
def removeStrengh(widget):
    if not selected_player:
        return
    selected_player.removeStrengh()
    refresh()

def addHand(widget):
    if not selected_player:
        return
    selected_player.addHand()
    refresh()
    
def removeHand(widget):
    if not selected_player:
        return
    selected_player.removeHand()
    refresh()

def resetGame(widget):
    for player in players:
        player.setLevel(1)
        player.setStrengh(1)
        player.setHand(2)
        player.setRace('Human')
        player.setKit('')
        for _object in player.getObjects():
            player.removeObject(_object)
    refresh()

def throwDice(widget):
    dialogWindow = PyGtk.Gtk.MessageDialog(window, 0, PyGtk.Gtk.MessageType.INFO, PyGtk.Gtk.ButtonsType.OK, "Et le dé donne...")
    dialogWindow.format_secondary_text(str(random.randint(1,6)))
    dialogWindow.run()
    dialogWindow.destroy()

def sendCmd(widget,cmd=''):
    if not cmd:
        cmd = TerminalBuffer.get_text(TerminalBuffer.get_start_iter(),TerminalBuffer.get_end_iter(),'')
    output = TerminalHandler.getCommands(_input=cmd.split('\n'))
    TerminalCommands.set_text('\n'.join(output))
    TerminalBuffer.set_text('')
window = PyGtk.MainWindow(title='Munchkin Level Counter')
global_box = window.create('Box',orientation=PyGtk.Gtk.Orientation.VERTICAL,spacing=20)

PlayerBox = window.create('Box',orientation=PyGtk.Gtk.Orientation.HORIZONTAL,spacing=10)
ButtonsBox = window.create('Box',orientation=PyGtk.Gtk.Orientation.HORIZONTAL,spacing=2)
TerminalBox = window.create('Box',orientation=PyGtk.Gtk.Orientation.HORIZONTAL)
TerminalOutput = window.create('Box',orientation=PyGtk.Gtk.Orientation.VERTICAL,spacing=2)

window.add(global_box)
global_box.pack_start(PlayerBox,True,True,0)
global_box.pack_start(ButtonsBox,True,True,0)
global_box.pack_start(TerminalOutput,True,True,0)

TerminalOutput.pack_end(TerminalBox, True, True, 0)

scrolledwindow = PyGtk.Gtk.ScrolledWindow()
scrolledwindow.set_hexpand(True)
scrolledwindow.set_vexpand(True)
TerminalBox.add(scrolledwindow)
TerminalText = window.create('TextView')
TerminalBuffer = TerminalText.get_buffer()
scrolledwindow.add(TerminalText)
TerminalButton = window.create('Button', label='Envoyer la commande')
TerminalBox.add(TerminalButton)
TerminalButton.connect('clicked', sendCmd)
TerminalCommands = window.create('Label')
TerminalHandler = ccmc.parse()
TerminalHandler.players = players
TerminalHandler.refresh = refresh
TerminalHandler.addPlayer = addPlayer
TerminalHandler.removePlayer = removePlayer
TerminalHandler.sendCmd = sendCmd

TerminalOutput.pack_start(TerminalCommands, True, True, 0)


PlayerButtonBox = window.create('Box',orientation=PyGtk.Gtk.Orientation.VERTICAL,spacing=2)
ButtonsBox.add(PlayerButtonBox)

RemovePlayerButton = window.create('Button',label='Enlever un joueur')
PlayerButtonBox.add(RemovePlayerButton)
RemovePlayerButton.connect('clicked',removePlayer)

AddPlayerButton = window.create('Button',label='Ajouter un joueur')
PlayerButtonBox.add(AddPlayerButton)
AddPlayerButton.connect("clicked",addPlayer)

LevelBox = window.create('Box',orientation=PyGtk.Gtk.Orientation.VERTICAL,spacing=2)
ButtonsBox.add(LevelBox)

RemovePlayerButton = window.create('Button',label='Enlever un niveau')
LevelBox.add(RemovePlayerButton)
RemovePlayerButton.connect('clicked',removeLevel)

AddLevelButton = window.create('Button',label='Ajouter un niveau')
LevelBox.add(AddLevelButton)
AddLevelButton.connect('clicked',addLevel)

StrenghBox = window.create('Box',orientation=PyGtk.Gtk.Orientation.VERTICAL,spacing=2)
ButtonsBox.add(StrenghBox)

RemoveStrenghButton = window.create('Button',label='Enlever un de force')
StrenghBox.add(RemoveStrenghButton)
RemoveStrenghButton.connect('clicked',removeStrengh)

AddStrenghButton = window.create('Button',label='Ajouter un de force')
StrenghBox.add(AddStrenghButton)
AddStrenghButton.connect('clicked',addStrengh)

HandBox = window.create('Box',orientation=PyGtk.Gtk.Orientation.VERTICAL,spacing=2)
ButtonsBox.add(HandBox)

RemoveHandButton = window.create('Button',label='Enlever une main')
HandBox.add(RemoveHandButton)
RemoveHandButton.connect('clicked',removeHand)

AddHandButton = window.create('Button',label='Ajouter une main')
HandBox.add(AddHandButton)
AddHandButton.connect('clicked',addHand)

OtherBox = window.create('Box',orientation=PyGtk.Gtk.Orientation.VERTICAL,spacing=2)
ButtonsBox.add(OtherBox)

DiceButton = window.create('Button',label='Lancer un dé')
OtherBox.add(DiceButton)
DiceButton.connect('clicked',throwDice)

ResetButton = window.create('Button',label='Recommencer')
OtherBox.add(ResetButton)
ResetButton.connect('clicked',resetGame)

window.set_default_size(600,350)

def selection(selec):
    global selected_player
    model, treeiter = selec.get_selected()
    if treeiter != None:
        for i in players:
            if i.getName() == model[treeiter][0]:
                selected_player = i

treeview = PyGtk.Gtk.TreeView.new()
select = treeview.get_selection()
select.connect("changed",selection)

for i, column_title in enumerate(["Nom", "Race", "Classe", "Niveau", "Force", "Nombre de mains libres"]):
    renderer = PyGtk.Gtk.CellRendererText()
    column = PyGtk.Gtk.TreeViewColumn(column_title, renderer, text=i)
    treeview.append_column(column)

PlayerBox.pack_start(treeview, True, True, 0)

sendCmd('',cmd='load players.mlc')

loop = MainLoop()
window.show_all()
loop.start()
