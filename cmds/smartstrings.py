#!/usr/bin/python3
# -*- coding: utf-8 -*-

class ParsingError(Exception):
        pass

def SplitIgnoreStrings(line,*,sep=';',ConserveStrings=False):
        if not line.replace('\t','').replace(' ','').replace('\n','').endswith(sep):
                line += sep
        IsStr = False
        BuffLine = ''
        output = []
        Next = True
        if line.endswith('\n'):
                line = line[:-1]
        for i in line:
                if not Next:
                        Next = True
                        BuffLine += i
                elif i == '\\':
                        Next = False
                elif i == '"' or i == '\'':
                        if IsStr:
                                IsStr = False
                        else:
                                IsStr = True
                        if ConserveStrings:
                                BuffLine += i
                elif i == sep and not IsStr:
                     output.append(BuffLine)
                     BuffLine = ''
                else:
                        BuffLine += i
        return output

def CheckNonNull(line):
        if line.replace('\t','').replace(' ','') != '\n':
                return True
        return False

def CheckNonComment(line,comment=['#','//']):
        for c in comment:
                if line.startswith(c):
                        return False
        return True

def FromListToString(line):
        if not line.startswith('[') and not line.startswith(']'):
                raise ParsingError('The list doesn\'t start with [ or/and doesn\'t end with ]: %s' % line)
        line = line[1:-1] + ','
        return SplitIgnoreStrings(line,sep=',')

