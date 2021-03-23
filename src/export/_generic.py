#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

# import os

# from datetime import datetime

import config

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

def	_export_influxdb(pMeasurement, pTagsDict, pFieldsDict):

	# Merge given tags with common tags
	# lTags	= __tags_commonDict() | pTagsDict
	lTags	=	{**__tags_commonDict(), **pTagsDict}

	# Encode the tags dictionnary to a string
	lTagsStr	=	__tags_dicToString(lTags)

	# Encode the fields dictionnary to a string
	lFieldsStr	=	__fields_dicToString(pFieldsDict)


	#
	#	Generate the output line
	#

	# Add measurement name
	lOutput	= pMeasurement

	# Add tags
	if lTagsStr != '':
		lOutput	+= ',' + lTagsStr

	# Add fields
	lOutput	+= ' '
	lOutput	+= lFieldsStr

	# Print the line
	print(lOutput)


# ##############################################################################
# ##############################################################################

def measurement(pApiPath, pApiAttribute, pAttrValue, pApiSubpath='', pTagsDict={}, pFieldsDict={}):

	#
	#	Tags content
	#
	lTagsDict	=	pTagsDict.copy()

	lTagsDict[C_KEY_TAG_API_PATH]	= pApiPath
	lTagsDict[C_KEY_TAG_API_ATTR]	= pApiAttribute

	if pApiSubpath != '':
		lTagsDict[C_KEY_TAG_API_SUBPATH]	= pApiSubpath


	#
	#	Fields content
	#
	lFieldsDict	=	pFieldsDict.copy()
	lFieldsDict[C_KEY_FIELD_VALUE]	=	pAttrValue


	#
	#	Export the measurement
	#
	_export_influxdb(
		config.INFLUXDB_MEASUREMENT,
		lTagsDict,
		lFieldsDict
	)

# ##############################################################################
# ##############################################################################

def	genericJson(pApiPath, pJsonRoot, pJsonObjectName, pTagsDict={}, pFieldsDict={}):

	if pJsonObjectName not in pJsonRoot:
		return

	lJsonData	=	pJsonRoot[pJsonObjectName]


	#
	#	Iterate over model_info attributes and export them
	#
	for lJsonKey in lJsonData:

		lJsonValue	=	lJsonData[lJsonKey]

		measurement(
			pApiPath	=	pApiPath,
			# pApiSubpath	=	pSubpath,
			pApiAttribute	=	lJsonKey,
			pAttrValue	=	lJsonValue,
			pTagsDict	=	pTagsDict,
			pFieldsDict	=	pFieldsDict
		)

# ##############################################################################
# ##############################################################################

def	genericSubpath(pApiPath, pJsonRoot, pSubpath, pTagsDict={}, pFieldsDict={}):

	if pSubpath not in pJsonRoot:
		return

	lJsonSubpath	=	pJsonRoot[pSubpath]


	#
	#	Iterate over model_info attributes and export them
	#
	for lJsonKey in lJsonSubpath:

		lJsonValue	=	lJsonSubpath[lJsonKey]

		measurement(
			pApiPath	=	pApiPath,
			pApiSubpath	=	pSubpath,
			pApiAttribute	=	lJsonKey,
			pAttrValue	=	lJsonValue,
			pTagsDict	=	pTagsDict,
			pFieldsDict	=	pFieldsDict
		)

# ##############################################################################
# ##############################################################################

def	__fields_dicToString(pFieldsDict):

	retval	=	''

	for lFieldName in pFieldsDict:
		lFieldValue = pFieldsDict[lFieldName]

		if retval != '':
			retval	+= ','

		retval	+= lFieldName
		retval	+= '='
		if type(lFieldValue) == str:
			retval	+= "\"" + lFieldValue + "\""
		else:
			retval	+= str(lFieldValue)

	return retval

# ##############################################################################
# ##############################################################################

def __tags_common():
	retval	=	''

	retval	+=	'endpoint'
	retval	+=	'='
	retval	+=	config.FREEBOX_HOST

	return retval

# ##############################################################################
# ##############################################################################

def __tags_commonDict():

	retval	=	{}

	retval['host']	=	config.FREEBOX_HOST

	return retval

# ##############################################################################
# ##############################################################################

def	__tags_dicToString(pTagsDict):

	retval	=	''

	for lTagName in pTagsDict:
		lTagValue = pTagsDict[lTagName]

		# See https://docs.influxdata.com/influxdb/v1.7/write_protocols/line_protocol_tutorial/#special-characters
		if type(lTagValue) == str:
			lTagValue	=	lTagValue.replace(",", "\\,")
			lTagValue	=	lTagValue.replace("=", "\\=")
			lTagValue	=	lTagValue.replace(" ", "\\ ")

		if retval != '':
			retval	+= ','

		retval	+= lTagName
		retval	+= '='
		retval	+= str(lTagValue) # Tags are always strings

	return retval

# ##############################################################################
# ##############################################################################