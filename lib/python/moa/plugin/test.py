# 
# Copyright 2009 Mark Fiers, Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Moa is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
# 
# Moa is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Moa.  If not, see <http://www.gnu.org/licenses/>.
# 

"""
**test** - Run unittests
------------------------
"""

import os
import sys
import optparse

import moa.unittests
import moa.logger as l

def defineCommands(data):
    data['commands']['unittest'] = {
        'desc' : 'Run Moa unittests',
        'call' : runTests,
        'needsJob' : False
        }

def runTests(data):
    moa.unittests.run(data['options'], data['args'])
