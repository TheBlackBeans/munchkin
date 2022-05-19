#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'BlackBeans'
__copyright__ = 'BeansBoxⓡ ⓒ'
import os

realname = 'load'

def run(params,parse_object):
    if len(params) != 1:
        return parse_object.getError(realname,message='%s takes excalty 1 argument' % realname)
    if params[0] == '--help':
        return 'Usage: %s <file>' % realname
    else:
        with open(params[0]) as f:
            l = f.readlines()
        parse_object.sendCmd('','\n'.join(l))
