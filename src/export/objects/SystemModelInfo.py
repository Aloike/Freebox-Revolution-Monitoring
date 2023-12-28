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

def    fromJson(pApiPath, pApiSubpath, pTagsDict, pJsonObjectSystemModelInfo):

    #
    #    Iterate over attributes and export them
    #
    for lJsonKey in pJsonObjectSystemModelInfo:

        _generic.measurement(
            pApiPath    =    pApiPath,
            pApiSubpath    =    pApiSubpath,
            pApiAttribute    =    lJsonKey,
            pAttrValue    =    pJsonObjectSystemModelInfo[lJsonKey],
            pTagsDict    =    pTagsDict#,
            # pFieldsDict    =    lFields
        )

# ##############################################################################
# ##############################################################################