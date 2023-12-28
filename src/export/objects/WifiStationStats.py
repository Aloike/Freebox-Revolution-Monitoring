#!/usr/bin/env python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

from ..    import    _generic

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

def    fromJson(pApiPath, pApiSubpath, pTagsDict, pJsonObjectWifiStationStats):

    #
    #    Iterate over available keys
    #
    for lJsonKey in pJsonObjectWifiStationStats:

        _generic.measurement(
            pApiPath    =    pApiPath,
            pApiSubpath    =    pApiSubpath,
            pApiAttribute    =    lJsonKey,
            pAttrValue    =    pJsonObjectWifiStationStats[lJsonKey],
            pTagsDict    =    pTagsDict#,
            # pFieldsDict    =    lFields
        )

# ##############################################################################
# ##############################################################################