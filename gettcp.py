#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
import buildtcp

if __name__ == "__main__":
    _packet = buildtcp.buildtcp()
    print(_packet)
    sys.exit(0)

