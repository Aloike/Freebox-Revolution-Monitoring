#!/usr/bin/env python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

from ..    import    _generic

# ##############################################################################
# ##############################################################################

def    fromJson(pApiPath, pApiSubpath, pTagsDict, pJsonObjectSwitchPortStats):

    #
    #    Iterate over available keys
    #
    for lJsonKey in pJsonObjectSwitchPortStats:

        _generic.measurement(
            pApiPath    =    pApiPath,
            pApiSubpath    =    pApiSubpath,
            pApiAttribute    =    lJsonKey,
            pAttrValue    =    pJsonObjectSwitchPortStats[lJsonKey],
            pTagsDict    =    pTagsDict#,
            # pFieldsDict    =    lFields
        )

# ##############################################################################
# ##############################################################################