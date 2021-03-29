#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

import os

from datetime import datetime

import freebox.api as freebox_api

import export._generic

# ##############################################################################
# ##############################################################################
#
#	Logging configuration
#
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# ##############################################################################
# ##############################################################################

def	all():

	sys_json_raw = freebox_api.get_system()
	log.debug( "sys_json_raw == %s" % sys_json_raw)

	if 'result' not in sys_json_raw:
		return


	lNodeData	=	sys_json_raw['result']

	#
	#	Prepare tags and fields of default item
	#	
	
	for lJsonKey in lNodeData:

		if	(	lJsonKey	==	'fans'
			or	lJsonKey	==	'model_info'
			or	lJsonKey	==	'sensors'	):
			# Those values identify subpath; they will be managed separately.
			continue

		lJsonValue	=	lNodeData[lJsonKey]

		export._generic.measurement(
			pApiPath	=	'system',
			pApiAttribute	=	lJsonKey,
			pAttrValue	=	lJsonValue
		)


	if	(	'fans'	in lNodeData	):
		_fans(lNodeData)

	if	(	'model_info'	in lNodeData	):
		_modelInfo(lNodeData)

	if	(	'sensors'	in lNodeData	):
		_sensors(lNodeData)

# ##############################################################################
# ##############################################################################

def	_fans(pNodeSystem):

	if 'fans' not in pNodeSystem:
		return

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
		lTags	=	{
			'fan_id'	:	lJsonFanData['id'],
			'fan_name'	:	lJsonFanData['name']
		}


		#
		#	Iterate over fan attributes and export them
		#
		for lJsonKey in lJsonFanData:

			if	(	lJsonKey	==	'id'
				or	lJsonKey	==	'name'	):
				#Those keys are used in tags, skip them.
				continue

			lJsonValue	=	lJsonFanData[lJsonKey]

			export._generic.measurement(
				pApiPath	=	'system',
				pApiSubpath	=	'fans',
				pApiAttribute	=	lJsonKey,
				pAttrValue	=	lJsonValue,
				pTagsDict	=	lTags#,
				# pFieldsDict	=	lFields
			)

		lFanNbr	=	lFanNbr + 1

# ##############################################################################
# ##############################################################################

def	_modelInfo(pNodeSystem):

	export._generic.genericSubpath(
		pApiPath='system',
		pJsonRoot=pNodeSystem,
		pSubpath	=	'model_info'
		# pTagsDict=
		# pFieldsDict=
	)

# ##############################################################################
# ##############################################################################

def	_sensors(pNodeSystem):

	if 'sensors' not in pNodeSystem:
		return

	lJsonSensorsList	=	pNodeSystem['sensors']


	#
	#	Iterate over available sensors
	#
	lSensorsCount	=	len(lJsonSensorsList)
	lSensorNbr	=	0
	while lSensorNbr < lSensorsCount :
		# log.debug("lJsonSensorsList[%d] = %s" % (lSensorNbr, lJsonSensorsList[lSensorNbr]))

		lJsonSensorData	=	lJsonSensorsList[lSensorNbr]

		# Use some sensor attributes as tags
		lTags	=	{
			'sensor_id'	:	lJsonSensorData['id'],
			'sensor_name'	:	lJsonSensorData['name']
		}


		#
		#	Iterate over sensor attributes and export them
		#
		for lJsonKey in lJsonSensorData:

			if	(	lJsonKey	==	'id'
				or	lJsonKey	==	'name'	):
				#Those keys are used in tags, skip them.
				continue

			lJsonValue	=	lJsonSensorData[lJsonKey]


			export._generic.measurement(
				pApiPath	=	'system',
				pApiSubpath	=	'sensors',
				pApiAttribute	=	lJsonKey,
				pAttrValue	=	lJsonValue,
				pTagsDict	=	lTags#,
				# pFieldsDict	=	lFields
			)

		lSensorNbr	=	lSensorNbr + 1

# ##############################################################################
# ##############################################################################
