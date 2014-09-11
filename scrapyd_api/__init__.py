#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
                                    _               _
                                   | |             (_)
 ___  ___ _ __ __ _ _ __  _   _  __| |   __ _ _ __  _
/ __|/ __| '__/ _` | '_ \| | | |/ _` |  / _` | '_ \| |
\__ \ (__| | | (_| | |_) | |_| | (_| | | (_| | |_) | |
|___/\___|_|  \__,_| .__/ \__, |\__,_|  \__,_| .__/|_|
                   | |     __/ |             | |
                   |_|    |___/              |_|
"""

from __future__ import unicode_literals

from .exceptions import ScrapydError
from .wrapper import ScrapydAPI

__author__ = 'Darian Moody'
__email__ = 'mail@djm.org.uk'
__version__ = '0.1.0'
__license__ = 'BSD 2-Clause'
__copyright__ = 'Copyright 2014 Darian Moody'

VERSION = __version__

__all__ = ['ScrapydError', 'ScrapydAPI']
