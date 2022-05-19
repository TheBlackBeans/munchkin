#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'BlackBeans'
__copyright__ = 'BeansBoxⓡ ⓒ'

realname = 'players'

def run(params,parse_object):
    if params[0] == '--help':
        return 'Usage: players <add|remove> <player>'
    elif params[0] == 'add':
        parse_object.addPlayer('',params[1])
        return 'Added %s' % params[1]
    elif params[0] == 'remove':
        parse_object.removePlayer(params[1])
        return 'Removed %s' % params[1]
    else:
        return parse_object.getError(realname,message='wrong parameter')
