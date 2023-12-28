#!/usr/bin/env python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

from ..    import    _generic

from .    import    SystemFan
from .    import    SystemModelInfo
from .    import    SystemSensor

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

def    fromJson(pApiPath, pApiSubpath, pTagsDict, pJsonObjectSystemConfig):

    #
    #    Iterate over attributes and export them
    #
    for lJsonKey in pJsonObjectSystemConfig:

        #
        # Those keys identify subpath; they are managed separately.
        #
        if    (    lJsonKey    ==    'fans'    ):

            # Iterate over connectivities and export them
            lFansCount    =    len(pJsonObjectSystemConfig[lJsonKey])
            lFanIdx    =    0
            while lFanIdx < lFansCount :

                lJsonObjSystemFan    =    pJsonObjectSystemConfig[lJsonKey][lFanIdx]

                SystemFan.fromJson(
                    pApiPath,
                    pApiSubpath + '/' + lJsonKey,
                    pTagsDict,
                    lJsonObjSystemFan
                )
                lFanIdx    =    lFanIdx + 1


        elif    (    lJsonKey    ==    'model_info'    ):
            SystemModelInfo.fromJson(
                pApiPath    =    pApiPath,
                pApiSubpath    =    pApiSubpath + '/' + lJsonKey,
                pTagsDict    =    pTagsDict,
                pJsonObjectSystemModelInfo    =    pJsonObjectSystemConfig[lJsonKey]
            )


        elif    (    lJsonKey    ==    'sensors'    ):

            # Iterate over connectivities and export them
            lSensorsCount    =    len(pJsonObjectSystemConfig[lJsonKey])
            lSensorIdx    =    0
            while lSensorIdx < lSensorsCount :

                lJsonObjSystemSensor    =    pJsonObjectSystemConfig[lJsonKey][lSensorIdx]

                SystemSensor.fromJson(
                    pApiPath,
                    pApiSubpath + '/' + lJsonKey,
                    pTagsDict,
                    lJsonObjSystemSensor
                )
                lSensorIdx    =    lSensorIdx + 1


        #
        # Default export rule
        #
        else:
            _generic.measurement(
                pApiPath    =    pApiPath,
                # pApiSubpath    =    'fans',
                pApiAttribute    =    lJsonKey,
                pAttrValue    =    pJsonObjectSystemConfig[lJsonKey],
                pTagsDict    =    pTagsDict#,
                # pFieldsDict    =    lFields
            )

# ##############################################################################
# ##############################################################################