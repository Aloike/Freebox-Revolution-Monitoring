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

def    fromJson(pApiPath, pApiSubpath, pTagsDict, pJsonObjectSystemSensor):

    if 'id' not in pJsonObjectSystemSensor:
        log.error("This sensor doesn't have any 'id'!")
        return


    lTags    =    pTagsDict.copy()

    # Add the station unique ID in the tags to identify the station
    lTags['sensor_id']    =    pJsonObjectSystemSensor['id']
    lTags['sensor_name']    =    pJsonObjectSystemSensor['name']


    #
    #    Iterate over attributes and export them
    #
    for lJsonKey in pJsonObjectSystemSensor:

        #
        #    Those keys are used in tags, skip them.
        #
        if    (    lJsonKey    ==    'id'
            or    lJsonKey    ==    'name'    ):
            continue

        #
        # Default export rule
        #
        else:
            _generic.measurement(
                pApiPath    =    pApiPath,
                pApiSubpath    =    pApiSubpath,
                pApiAttribute    =    lJsonKey,
                pAttrValue    =    pJsonObjectSystemSensor[lJsonKey],
                pTagsDict    =    lTags#,
                # pFieldsDict    =    lFields
            )

# ##############################################################################
# ##############################################################################