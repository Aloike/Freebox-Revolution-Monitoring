#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

#
# Freebox API SDK / Docs: http://dev.freebox.fr/sdk/os/login/
# version 8
#

from __future__ import print_function
from __future__ import unicode_literals

import requests
import os
# import json
# import hmac
import time
import argparse
import sys
import time
from time import strftime, gmtime
from datetime import datetime
# from hashlib import sha1


# To install the latest version of Unidecode from the Python package index, use these commands:
# $ pip install unidecode
from unidecode import unidecode
#
# if sys.version_info >= (3, 0):
#     import configparser as configp
# else:
#     import ConfigParser as configp


import application_config as app_cfg
import freebox_export
import export.connection
import export.lan
import export.system
import export.switch
import freebox.api as freebox_api

# ##############################################################################
# ##############################################################################

import logging

FORMAT = "[%(levelname)6s][%(filename)s +%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# ##############################################################################
# ##############################################################################

VERSION = "1.0.0 2021/03/22"

# ##############################################################################
# ##############################################################################

def get_creation_date(file):
    stat = os.stat(file)
    return stat.st_mtime

# ##############################################################################
# ##############################################################################

def register_status():
    
    if freebox_api.isRegistered() != True:
        print("Status: invalid config, auth not done.")
        print("Please run `%s --register` to register app." % sys.argv[0])
        return False
    else:
        print("Status: auth already done")
        return True

# ##############################################################################
# ##############################################################################

def do_export():

    # Set the measurement name's prefix
    export._generic.setMeasurementName(app_cfg.measurement_namePrefix())

    # Set tags common to all metrics
    lCommonTagsDict =   {
        'host'  :   app_cfg.freebox_hostname()
    }
    export._generic.setTagsCommon_dict(lCommonTagsDict)


    # Export application infos.
    freebox_export.application_infos(__file__, VERSION)


    # Fetch session_token
    freebox_api.session_open(
        app_cfg.app_id()
    )


    # --------------------------------------------------------------------------
    #   Export
    # --------------------------------------------------------------------------

    if  app_cfg.export_connection():
        export.connection.all()

    if  app_cfg.export_lan_config():
        export.lan.config()

    if app_cfg.export_lan_interfaces():
        freebox_export.lan_interfaces()

    if app_cfg.export_lan_interfaces_hosts():
        freebox_export.lan_interfaces_hosts()

    if app_cfg.export_switch_ports_status():
        freebox_export.switch_ports()

    if app_cfg.export_switch_status():
        export.switch.status()

    if app_cfg.export_system():
        export.system.all()

    if app_cfg.export_storage_disk():
        freebox_export.storage_disk()

    if app_cfg.export_wifi_usage():
        export.wifi.accessPoints_stations()

# ##############################################################################
# ##############################################################################

# Main
def main():

    #
    #   Initialize the application
    #

    # Read the configuration from env and command line.
    app_cfg.init()
    app_cfg.parse_args()

    # Initialize the module used to interact with the Freebox API.
    freebox_api.init(
        pFreeboxHostname    =   app_cfg.freebox_hostname(),
        pAppId  =   app_cfg.app_id(),
        pAppName    = app_cfg.app_name(),
        pDeviceName = app_cfg.device_name()
    )


    #
    #   Execute actions depending on command-line flags
    #
    if app_cfg.application_register():
        # Register the application with the Freebox
        freebox_api.login_registerApplication(
            app_cfg.app_id(),
            app_cfg.app_name(),
            VERSION,
            app_cfg.device_name()
        )

    elif app_cfg.application_registerStatus():
        # Check the application registration status with the Freebox
        if not register_status():
            return 1
        else:
            return 0

    else:
        # Export metrics
        do_export()


    return 0


if __name__ == '__main__':
    exit( main() )
    # log.info ("Application name: %s" % app_cfg.app_name() )
