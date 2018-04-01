#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .constants import (
    FINISHED,
    PENDING,
    RUNNING
)
from .exceptions import ScrapydError
from .wrapper import ScrapydAPI

__author__ = 'Darian Moody'
__email__ = 'mail@djm.org.uk'
__version__ = '2.1.2'
__license__ = 'BSD 2-Clause'
__copyright__ = 'Copyright 2014 Darian Moody'

VERSION = __version__

__all__ = ['ScrapydError', 'ScrapydAPI', 'FINISHED', 'PENDING', 'RUNNING']
