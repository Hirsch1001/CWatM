# -------------------------------------------------------------------------
# Name:        Configuration
# Purpose:
#
# Author:      burekpe
#
# Created:     16/05/2016
# Copyright:   (c) burekpe 2016
# -------------------------------------------------------------------------

from management_modules.globals import *

import ConfigParser
import re
import xml.dom.minidom
from management_modules.messages import *

import optparse
import os
import sys
import time
import datetime
import shutil
import glob



class ExtParser(ConfigParser.SafeConfigParser):
     #implementing extended interpolation
     def __init__(self, *args, **kwargs):
         self.cur_depth = 0
         ConfigParser.SafeConfigParser.__init__(self, *args, **kwargs)


     def get(self, section, option, raw=False, vars=None):
         r_opt = ConfigParser.SafeConfigParser.get(self, section, option, raw=True, vars=vars)
         if raw:
             return r_opt

         ret = r_opt
         re_newintp1 = r'\$\((\w*):(\w*)\)'  # other section
         re_newintp2 = r'\$\((\w*)\)'  # same section

         re_old1 = re.findall('\$\(\w*:\w*\)', r_opt)
         re_old2 = re.findall('\$\(\w*\)', r_opt)

         m_new1 = re.findall(re_newintp1, r_opt)
         m_new2 = re.findall(re_newintp2, r_opt)

         if m_new1:
             i = 0
             for f_section, f_option in m_new1:
                 self.cur_depth = self.cur_depth + 1
                 if self.cur_depth < ConfigParser.MAX_INTERPOLATION_DEPTH:
                     sub = self.get(f_section,f_option, vars=vars)
                     ret = ret.replace(re_old1[i], sub)
                     i += 1
                 else:
                     raise ConfigParser.InterpolationDepthError, (option, section, r_opt)

         if m_new2:
             i = 0
             for l_option in m_new2:
                 self.cur_depth = self.cur_depth + 1
                 if self.cur_depth < ConfigParser.MAX_INTERPOLATION_DEPTH:
                     sub = self.get(section, l_option, vars=vars)
                     ret = ret.replace(re_old2[i], sub)
                     i =+ 1
                 else:
                     raise ConfigParser.InterpolationDepthError, (option, section, r_opt)

         self.cur_depth = self.cur_depth - 1
         return ret



def parse_configuration(settingsFileName):

    def splitout(varin, check):
        out = map(str.strip, varin.split(','))
        if out[0] == "": out[0]="None"
        if out[0] != "None": check = True
        return out, check


    #config = ConfigParser.ConfigParser()
    config = ExtParser()
    config.optionxform = str
    config.sections()
    config.read(settingsFileName)
    for sec in config.sections():
        #print sec
        options = config.options(sec)
        check_section = False
        for opt in options:
            if sec=="OPTIONS":
                option[opt] = config.getboolean(sec, opt)
            else:
                # Check if config line = output line
                if opt.lower()[0:4] == "out_":
                    index = sec.lower()+"_"+opt.lower()

                    if opt.lower()[-4:] =="_dir":
                        outDir[sec] = config.get(sec, opt)
                    else:
                        # split into timeseries and maps
                        if opt.lower()[4:8] == "tss_":
                            outTss[index],check_section = splitout(config.get(sec, opt),check_section)
                        else:
                            outMap[index],check_section = splitout(config.get(sec, opt),check_section)

                else:
                    # binding: all the parameters which are not output or option are collected
                    binding[opt] = config.get(sec, opt)
        if check_section:
            k =1
            outsection.append(sec)

    outputDir.append(binding["PathOut"])
     # Output directory is stored in a separat global array


def read_metanetcdf(metaxml):
    """ read the metadata for netcdf output files
    unit, long name, standard name and additional information

    """

    try:
        f=open(metaxml)
        f.close()
    except:
        msg = "Cannot find option file: " + metaxml
        raise CWATMFileError(metaxml,msg)
    try:
        metaparse = xml.dom.minidom.parse(metaxml)
    except:
        msg = "Error using option file: " + metaxml
        raise CWATMError(msg)

    # running through all output variable
    # if an output variable is not defined here the standard metadata is used
    # unit = "undefined", standard name = long name = variable name
    meta = metaparse.getElementsByTagName("CWATM")[0]

    for metavar in meta.getElementsByTagName("metanetcdf"):
        d = {}
        for key in metavar.attributes.keys():
            if key != 'varname':
                d[key] = metavar.attributes[key].value
        key = metavar.attributes['varname'].value
        metaNetcdfVar[key] = d



