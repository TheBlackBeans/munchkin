
#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'BlackBeans'
__copyright__ = 'BeansBoxⓡ ⓒ'

realname = 'help'

def run(params,parse_object):
    cmds = parse_object.getCommands(_input=['getcmds'])[0].split('\n')
    output = 'Commands:\n'
    for cmd in cmds:
        output += '\t%s\n' % cmd
    output += 'Try <command> --help to get more help'
    return output
