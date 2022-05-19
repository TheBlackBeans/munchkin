#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'BlackBeans'
__copyright__ = 'BeansBoxⓡ ⓒ'

realname = 'var'


def run(params,parse_object): #params: 0 -> modifier; 1 -> what; 2 -> value; 3 -> target
    if params[0] == '--help':
        return 'Usage: var <modifier> <attribute> <value> <target>'
    if not params[0] == 'unset' and not params[3]:
        parse_object.getError('var', message='no target defined')        
#    if not type(int(params[2])) == type(0) and (params[1] == 'strengh' or params[1] == 'hand' or params[1] == 'level'):
#        return parse_object.getError('var', message='the fird modifier is not an integer: %s' % params[2])
    player = None
    for i in parse_object.players:
        if params[0] == 'unset':
            if i.getName() == params[2]:
                player = i
            continue
        elif i.getName() == params[3]:
            player = i
    if not player:
        return parse_object.getError(realname,message='the defined target doesn\'t exist')
    if params[0] == 'add' or params[0] == 'remove':
        exec('player.%s%s(int(params[2]))' % (params[0],params[1].title()))
        parse_object.refresh()
        return '%s was %s to %s\'s %s' % (params[2], params[0], params[3], params[1])
    elif params[0] == 'set':
        exec('player.%s%s(params[2].title())' % (params[0],params[1].title()))
        parse_object.refresh()
        return '%s\'s %s was %s (to %s)' % (params[3], params[1], params[0], params[2].title())
    elif params[0] == 'unset':
        exec('player.%s%s()' % (params[0],params[1].title()))
        parse_object.refresh()
        return '%s\'s %s was %s' % (params[2], params[1], params[0])
    else:
        return parse_object.getError('var', message='wrong modifier')
    
