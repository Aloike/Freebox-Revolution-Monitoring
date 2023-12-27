#!/usr/bin/env python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

import freebox.api as fbx_api

import export._generic

from .objects    import StorageDisk

# ##############################################################################
# ##############################################################################
#
#    Logging configuration
#
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# ##############################################################################
# ##############################################################################

def disk():

    lApiPath    =    "storage/disk"

    #
    #    Get the collection of all StorageDisk
    #

    # Fetch JSON data
    lJsonStorageDiskList = fbx_api.get_storage_disk()
    log.debug("lJsonStorageDiskList = %s" % lJsonStorageDiskList)

    if 'result' not in lJsonStorageDiskList:
        return

    lDisksCount    =    len(lJsonStorageDiskList['result'])
    lDiskNbr    =    0
    while lDiskNbr < lDisksCount:

        lJsonStorageDisk    =    lJsonStorageDiskList['result'][lDiskNbr]

        StorageDisk.fromJson(
            pApiPath    =    lApiPath,
            pApiSubpath    =    '',
            pTagsDict    =    {},
            pJsonObjectStorageDisk    =    lJsonStorageDisk
        )

        lDiskNbr = lDiskNbr + 1

# ##############################################################################
# ##############################################################################
