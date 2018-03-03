#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from utils.ArgUtils import ArgUtils


if __name__ == '__main__':
    args = ArgUtils.parse_args(sys.argv)
    s_package = args.pop('package')
    s_controller = args.pop('controller')
    s_action = args.pop('action')

    controller_package = __import__(s_package + '.' + s_controller, fromlist=s_package)
    controller = getattr(controller_package, s_controller)
    action = getattr(controller, s_action)
    #
    action(args)
