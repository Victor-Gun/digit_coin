#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ArgUtils(object):
    """
    参数解析
    """
    # 将参数解析到dict
    @staticmethod
    def parse_args(argv):
        (args, k, v) = ({}, '', '')
        for arg in argv:
            if arg.find('=') < 0:
                continue

            if arg.startswith('--'):
                (k, v) = arg[2:].split('=')
            elif arg.startswith('-'):
                (k, v) = arg[1:].split('=')
            else:
                (k, v) = arg.split('=')

            if k != '':
                args[k.replace('-', '_')] = v

        return args

