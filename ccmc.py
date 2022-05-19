#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re, sys
from smartstrings import SplitIgnoreStrings as SIS
from smartstrings import CheckNonNull as CNN
from smartstrings import CheckNonComment as CNC

class ArgumentsError(Exception):
	pass

class MainError(Exception):
        pass

def run(*,_file=None,_input=None,aliases={},bugs=None):
        pass

class debugger():
        def __init__(self,*s):
                pass
        """
        This class is ONLY
        in case the user of
        this module doesn't
        think to add my debugging
        library in params
        """
        def debug(self,*s):
                pass

class parse():
        def __init__(self,*,bugs=debugger):
                self.bugs = bugs
                try:
                        import cmds
                except:
                        raise ImportError("Can't get the commands")
                
                self.cmds, self.commands = cmds, cmds
        def getError(self,command,message='unknown command'):
                return 'Error: %s: %s' % (command,message)
        def getCommands(self,*,_file=None,_input=None):
                global commands
                if _file:
                        self.File = _file
                        self.typeof = 'file'
                elif _input and type(_input) == type([]):
                        self.File = _input
                        self.typeof = 'str'
                else:
                        raise ArgumentsError('File pointer or a list must be set: %s, %s' % (_file, _input))
                cmds, commands = self.cmds, self.commands
                cmds = self.cmds
                bugs = self.bugs
                Input = []
                Output = []
                if self.typeof == 'file':
                        u = open(self.File,'r')
                        f = u.readlines()
                else:
                        f = self.File
                for line in f:
                        if CNC(line,comment=['#']) and CNN(line):
                                if line.endswith('\n'):
                                        line = line[:-1]
                                Input.append(line)
                if self.typeof == 'file':
                        u.close()
                        del u
                bugs.debug('File f: %s' % f,['--file-show'])
                del f

                true_cmds = {}
                for cmd in dir(cmds):
                        try:
                                if not cmd.startswith('__') and cmd != 'cmds':
                                        exec('true_cmds[cmds.%s.realname] = cmds.%s' % (cmd, cmd))
                                        self.true_cmds = true_cmds
                        except:
                                pass
                                        
                for line in Input:
                        line = SIS(line,sep=';',ConserveStrings=True)
                        bugs.debug('line: %s ' % line,['--line'])
                        for a in line:
                                bugs.debug('a (before): %s' % a,['--a'])
                                a = a.split(' ')
                                bugs.debug('a (after): %s' % a,['--a'])
                                bugs.debug('a[0] = %s, is in dir(cmds) = %s' % (a[0],dir(cmds)),['--cmds'])
                                if a[0] in true_cmds.keys():
                                        bugs.debug('a[0] = %s, is in dir(cmds) = %s' % (a[0],dir(cmds)),['--cmds'])
                                        true_cmds[a[0]].command_line = a[:]
                                        command_result = []
                                        command_result.append(true_cmds[a[0]].run(a[1:],self))
                                        if command_result[0]:
                                                Output.append(command_result[0])
                                        
                                else:
                                        Output.append(self.getError(a[0]))
                return Output


if __name__ == "__main__":
        raise MainError('The %s module can\'t be called as the main program' % sys.argv[0])

