# Copyright 2009-2011 Mark Fiers
# The New Zealand Institute for Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Licensed under the GPL license (see 'COPYING')
# 
"""
moa.jobConf
-----------

moa job configuration
"""

import re
import os
import sys

import Yaco
 
import moa.logger as l
import moa.utils

MOABASE = moa.utils.getMoaBase()

class JobConf(object):
    """
    This is a wrapper around a Yaco object - with a few extras, such as
    checking if a parameter is of the promised type

    to distinguish between attributes of this object & proper job
    configuration parameters
    """
    
    def __init__(self, job):
        """
        Initialize the conf from the parent job
        """
        
        self.job = job
        self.jobConf = Yaco.Yaco()
        self.jobConfFile = os.path.join(self.job.confDir, 'config')
        
        #: these fields are not to be saved
        self.doNotSave = []
        
        #: these fields are not be type-checked
        self.doNotCheck = []
        
        #: these fields are private (i.e. not to be
        #: displayed by default)
        self.private = []
        
        if os.path.exists(self.jobConfFile):
            self.jobConf.load(self.jobConfFile)

        #this is a temp addition - private was accidentaly
        #added to the jobconf in a number of jobs - can't
        #be theremoa
        if self.jobConf.has_key('private'):
            del self.jobConf['private']

            
    def save(self):
        self.job.checkConfDir()
        self.jobConf.save(self.jobConfFile, self.doNotSave)

    def setInJobConf(self, key):
        if self.jobConf.has_key(key):
            return True
        else:
            return False

    def keys(self):
        """
        return a dict with all known parameters and values, either
        defined in the job configuration of the template
        """
        rvt = set(self.job.template.parameters.keys())
        rvj = set(self.jobConf.keys())
        return list(rvt.union(rvj))

    def has_key(self, key):
        if self.jobConf.has_key(key):
            return True
        if self.job.template.parameters.has_key(key):
            return True
        return False

    def update(self, data):
        self.jobConf.update(data)
        
    def get(self, key, default):
        v = self.__getitem__(key)
        if v: 
            return v
        else:
            return default
        
    def __getitem__(self, key):
        v = ''
        if self.jobConf.has_key(key):
            v = self.jobConf[key]
        elif key in self.job.template.parameters.keys() and \
                 self.job.template.parameters[key].has_key('default'):
            v = self.job.template.parameters[key].default

#        if isinstance(v, str) and '{{' in v:
#            rere = re.compile('\{\{ *([^ \}]*) *\}\}')
#            v = rere.sub(lambda x: self.__getitem__(x.groups()[0]), v)

        if key in self.job.template.parameters.keys() and \
               self.job.template.parameters[key].has_key('callback'):
            v = self.job.template.parameters[key].callback(key, v)
        return v
    
    def __delitem__(self, key):
        del(self.jobConf[key])


    def __setitem__(self, key, value):
        if key in self.job.template.parameters.keys():
            pd = self.job.template.parameters[key]
            if pd.type == 'boolean':
                if value.lower() in ["yes", "true", "1", 'y', 't']:
                    value = True
                else: value = False
            elif pd.type == 'integer':
                try:
                    value = int(value)
                except ValueError:
                    pass
            elif pd.type == 'float':
                try:
                    value = float(value)
                except ValueError:
                    pass
                
        self.jobConf[key] = value

    def __setattr__(self, key, value):
        if key in ['job', 'jobConf', 'jobConfFile',
                   'doNotCheck', 'doNotSave', 'private']:
            object.__setattr__(self, key, value)
        elif key[:4] == '_JC_':
            object.__setattr__(self, key, value)
        else:
            return self.__setitem__(key, value)
        
    def __getattr__(self, key):
        if key in ['job', 'jobConf', 'jobConfFile',
                   'doNotCheck', 'doNotSave', 'private']:
            object.__getattr__(self, key)
        elif key[:4] == '_JC_':
            object.__getattr__(self, key)
        else:
            return self.__getitem__(key)
