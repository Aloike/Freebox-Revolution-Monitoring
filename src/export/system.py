#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

import os

from datetime import datetime

# import ../config
# import ../freebox_api
import config
import freebox_api

import export._generic

# ##############################################################################
# ##############################################################################
#
#	Logging configuration
#
import logging
FORMAT = "[%(filename)s +%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# ##############################################################################
# ##############################################################################

C_KEY_TAG_API_PATH	=	'api_path'
C_KEY_TAG_API_SUBPATH	=	'api_subpath'
C_KEY_TAG_API_ATTR	=	'api_attribute'

C_KEY_FIELD_VALUE	=	'value'

# ##############################################################################
# ##############################################################################

def	all():

	sys_json_raw = freebox_api.get_system()
	if 'result' not in sys_json_raw:
		return
	# log.debug( "sys_json_raw['result'] == %s" % sys_json_raw['result'])


	lTags = {
		C_KEY_TAG_API_PATH	:	'system',
	}

	lNodeData	=	sys_json_raw['result']

	#
	#	Prepare tags and fields of default item
	#	
	
	for lJsonKey in lNodeData:

		# if	(	lJsonKey	==	'board_name'
		# 	# or	lJsonKey	==	'firmware_version'
		# 	or	lJsonKey	==	'mac'
		# 	or	lJsonKey	==	'serial'	):

		# 	# This data is considered as a tag
		# 	lTags[lJsonKey]	=	lJsonValue
		# else
		if	(	lJsonKey	==	'fans'
			or	lJsonKey	==	'model_info'
			or	lJsonKey	==	'sensors'	):
			# Those values identify subpath; they will be managed separately.
			continue

		lJsonValue	=	lNodeData[lJsonKey]

		lTags[C_KEY_TAG_API_ATTR]	= lJsonKey

		lFields	=	{
			C_KEY_FIELD_VALUE	:	lJsonValue
		}

		export._generic.measurement(lTags, lFields)


	if	(	'fans'	in lNodeData	):
		system_fans(lTags, lNodeData)

	if	(	'model_info'	in lNodeData	):
		system_modelInfo(lTags, lNodeData)

	if	(	'sensors'	in lNodeData	):
		system_sensors(lTags, lNodeData)

# ##############################################################################
# ##############################################################################

def	system_fans(pTags, pNodeSystem):

	if 'fans' not in pNodeSystem:
		return

	lTags	=	pTags.copy()
	lTags[C_KEY_TAG_API_PATH]	=	'system'
	lTags[C_KEY_TAG_API_SUBPATH]	=	'fans'


	lNodeData	=	pNodeSystem['fans']

	#
	#	Iterate over available fans
	#

	lFansCount	=	len(lNodeData)
	lFanNbr	=	0
	while lFanNbr < lFansCount :
		# log.debug("lNodeData[%d] = %s" % (lFanNbr, lNodeData[lFanNbr]))

		lJsonFanData	=	lNodeData[lFanNbr]

		# Use some fan attributes as tags
		lTags['fan_id']	=	lJsonFanData['id']
		lTags['fan_name']	=	lJsonFanData['name']


		#
		#	Iterate over fan attributes and export them
		#
		for lJsonKey in lJsonFanData:

			if	(	lJsonKey	==	'id'
				or	lJsonKey	==	'name'	):
				#Those keys are used in tags, skip them.
				continue

			lJsonValue	=	lJsonFanData[lJsonKey]

			lTags[C_KEY_TAG_API_ATTR]	=	lJsonKey

			# Setup hashtable for results
			lFields	=	{
				C_KEY_FIELD_VALUE	:	lJsonValue
			}

			export._generic.measurement(lTags, lFields)

		lFanNbr	=	lFanNbr + 1

# ##############################################################################
# ##############################################################################

def	system_modelInfo(pTags, pNodeSystem):

	if 'model_info' not in pNodeSystem:
		return

	lJsonModelInfo	=	pNodeSystem['model_info']

	lTags	=	pTags.copy()
	lTags[C_KEY_TAG_API_PATH]	=	'system'
	lTags[C_KEY_TAG_API_SUBPATH]	=	'model_info'

	#
	#	Iterate over model_info attributes and export them
	#
	for lJsonKey in lJsonModelInfo:

	# 	if	(	lJsonKey	==	'id'
	# 		or	lJsonKey	==	'name'	):
	# 		#Those keys are used in tags, skip them.
	# 		continue

		lJsonValue	=	lJsonModelInfo[lJsonKey]

		lTags[C_KEY_TAG_API_ATTR]	=	lJsonKey

		# Setup hashtable for results
		lFields	=	{
			C_KEY_FIELD_VALUE	:	lJsonValue
		}

		export._generic.measurement(lTags, lFields)

# ##############################################################################
# ##############################################################################

def	system_sensors(pTags, pNodeSystem):

	if 'sensors' not in pNodeSystem:
		return

	lNodeData	=	pNodeSystem['sensors']

	lTags	=	pTags.copy()
	lTags[C_KEY_TAG_API_PATH]	=	'system'
	lTags[C_KEY_TAG_API_SUBPATH]	=	'sensors'


	#
	#	Iterate over available sensors
	#

	lSensorsCount	=	len(lNodeData)
	lSensorNbr	=	0
	while lSensorNbr < lSensorsCount :
		# log.debug("lNodeData[%d] = %s" % (lSensorNbr, lNodeData[lSensorNbr]))

		lJsonSensorData	=	lNodeData[lSensorNbr]

		# Use some sensor attributes as tags
		lTags['sensor_id']	=	lJsonSensorData['id']
		lTags['sensor_name']	=	lJsonSensorData['name']


		#
		#	Iterate over sensor attributes and export them
		#
		for lJsonKey in lJsonSensorData:

			if	(	lJsonKey	==	'id'
				or	lJsonKey	==	'name'	):
				#Those keys are used in tags, skip them.
				continue

			lJsonValue	=	lJsonSensorData[lJsonKey]

			lTags[C_KEY_TAG_API_ATTR]	=	lJsonKey

			# Setup hashtable for results
			lFields	=	{
				C_KEY_FIELD_VALUE	:	lJsonValue
			}

			export._generic.measurement(lTags, lFields)

		lSensorNbr	=	lSensorNbr + 1

# ##############################################################################
# ##############################################################################
