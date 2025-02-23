"""
    :copyright: Copyright 2022 by the FreePDM team
    :license:   MIT License.
"""

import os
import configparser
import appdirs
from typing import NewType
import logging

# Reading and writing the configuration file.
# The location of the file is: [prefix location]/FreePDM/FreePDM.conf
#   [prefix location] depends on which OS you use...
#
#  The items are:
#    * The start of the project directory (or directories).
#      These directories are shown at the start of the main window.
#        "startupdir"
#

appname = 'FreePDM'
config_dir = appdirs.user_config_dir(appname)
config_name = os.path.join(config_dir, 'FreePDM.conf')

# filter type
Filter = NewType('Filter', int)

#
# filter flags
#
show_fc_files_only = 1
hide_versioned_fc_files = 2

# basic log level
# logging.basicConfig(level=logging.DEBUG)


class conf():
    def __init__(self):
        self.startup_directory = ''
        self.filter: Filter = 0
        self.log_file = ""
        self.logging_is_on = "False"
        self.fast_loading_dir =  ''
        self.server_pdm_name: str = None     # The URL to the server
        self.server_pdm_username: str = None # User login name
        self.server_pdm_path: str = None     # Path to the PDM

    def get_filter(self, filter_flag) -> Filter:
        return self.filter & filter_flag == filter_flag

    def set_filter(self, filter_flag):
        self.filter = self.filter | filter_flag

    def read(self):
        config = configparser.ConfigParser()
        config.read(config_name)

        # reading variables from section: 'DEFAULT'
        self.startup_directory = config['DEFAULT']['startup_directory']
        self.filter = int(config['DEFAULT']['filter'])
        self.log_file = config['DEFAULT']['log_file']
        self.logging_is_on = config['DEFAULT']['logging_is_on']
        self.fast_loading_dir = config['DEFAULT']['fast_loading_dir']
        self.server_pdm_name = config['DEFAULT']['server_name']
        self.server_pdm_username = config['DEFAULT']['server_pdm_name']
        self.server_pmd_path = config['DEFAULT']['server_pdm_path']


    def write(self):
        config = configparser.ConfigParser()
        config['DEFAULT']['startup_directory'] = self.startup_directory
        config['DEFAULT']['filter'] = str(self.filter)
        config['DEFAULT']['log_file'] = self.log_file
        config['DEFAULT']['logging_is_on'] = self.logging_is_on
        config['DEFAULT']['fast_loading_dir'] = self.fast_loading_dir
        config['DEFAULT']['server_name'] = self.server_pdm_name
        config['DEFAULT']['server_pdm_name'] = self.server_pdm_username
        config['DEFAULT']['server_pdm_path'] = self.server_pdm_path

        with open(config_name, 'w') as configfile:
            config.write(configfile)


# create the new directory if it doesn't exist
if not os.path.exists(config_dir):
    os.makedirs(config_dir)

# create a new config file when it doesn't exist
if not os.path.isfile(config_name):
    c = conf()
    c.write()