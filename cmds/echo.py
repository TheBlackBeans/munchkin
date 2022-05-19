#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'BlackBeans'
__copyright__ = 'BeansBoxⓡ ⓒ'

realname = 'echo'

def run(params,parse_object):
    if params[0] == '--help':
        return 'Usage: echo [message]\nreturn to stdout message'
    return ' '.join(params)
