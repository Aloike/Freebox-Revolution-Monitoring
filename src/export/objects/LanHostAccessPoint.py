#!/usr/bin/env python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

from ..    import    _generic

from .    import    LanHostAccessPointEthInformation
from .    import    LanHostAccessPointWifiInformation

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

def    fromJson(pApiPath, pApiSubpath, pTagsDict, pJsonObjectLanHostAccessPoint):

    lTags    =    pTagsDict.copy()
    lTags['access_point_uid']    =    pJsonObjectLanHostAccessPoint['uid']


    #
    #    Iterate over available keys
    #
    for lJsonKey in pJsonObjectLanHostAccessPoint:

        #
        #    Those keys are used in tags, skip them.
        #
        if lJsonKey == 'uid':
            continue

        #
        # Those keys identify subpath; they are managed separately.
        #
        elif lJsonKey == 'ethernet_information':
            LanHostAccessPointEthInformation.fromJson(
                pApiPath,
                pApiSubpath + '/ethernet_information',
                lTags,
                pJsonObjectLanHostAccessPoint[lJsonKey]
            )

        elif lJsonKey == 'wifi_information':
            LanHostAccessPointWifiInformation.fromJson(
                pApiPath,
                pApiSubpath + '/wifi_information',
                lTags,
                pJsonObjectLanHostAccessPoint[lJsonKey]
            )

        #
        # Default export rule
        #
        else:
            # log.error("Unmanaged key '%s'." % lJsonKey)
            _generic.measurement(
                pApiPath    =    pApiPath,
                pApiSubpath    =    pApiSubpath,
                pApiAttribute    =    lJsonKey,
                pAttrValue    =    pJsonObjectLanHostAccessPoint[lJsonKey],
                pTagsDict    =    lTags#,
                # pFieldsDict    =    lFields
            )

# ##############################################################################
# ##############################################################################
