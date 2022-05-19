#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'BlackBeans'
__copyright__ = 'BeansBoxⓡ ⓒ'

realname = 'getcmds'

def run(params,parse_object):
    if params[0] == '--help':
        return 'Usage: getcmds\nreturns all the enables commands'
    return '\n'.join(parse_object.true_cmds.keys())
