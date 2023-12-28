#!/usr/bin/env python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

# import export._generic
from ..    import    _generic

# ##############################################################################
# ##############################################################################

def    fromJson(pApiPath, pApiSubpath, pTagsDict, pJsonObjectLanHostL2Ident):

    #
    #    Iterate over available keys
    #
    for lJsonKey in pJsonObjectLanHostL2Ident:

        # export._generic.measurement(
        _generic.measurement(
            pApiPath    =    pApiPath,
            pApiSubpath    =    pApiSubpath,
            pApiAttribute    =    lJsonKey,
            pAttrValue    =    pJsonObjectLanHostL2Ident[lJsonKey],
            pTagsDict    =    pTagsDict#,
            # pFieldsDict    =    lFields
        )

# ##############################################################################
# ##############################################################################