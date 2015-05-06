#!/usr/bin/env python

import sys
import os

basedir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(basedir)

from sclab_sites import app

if __name__ == '__main__':
    app.run(port=9000, debug=True)
