#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

# import os

# from datetime import datetime

import config


import logging
FORMAT = "[%(filename)s +%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)



def measurement(pTagsDict, pFieldsDict):

	lTags	= __tags_common()

	for lTagName in pTagsDict:
		lTagValue = pTagsDict[lTagName]

		# See https://docs.influxdata.com/influxdb/v1.7/write_protocols/line_protocol_tutorial/#special-characters
		if type(lTagValue) == str:
			lTagValue	=	lTagValue.replace(",", "\\,")
			lTagValue	=	lTagValue.replace("=", "\\=")
			lTagValue	=	lTagValue.replace(" ", "\\ ")

		if lTags != '':
			lTags	+= ','
		
		lTags	+= lTagName
		lTags	+= '='
		lTags	+= str(lTagValue) # Tags are always strings


	lFields	= ''

	for lFieldName in pFieldsDict:
		lFieldValue = pFieldsDict[lFieldName]

		if lFields != '':
			lFields	+= ','
		
		lFields	+= lFieldName
		lFields	+= '='
		if type(lFieldValue) == str:
			lFields	+= "\"" + lFieldValue + "\""
		else:
			lFields	+= str(lFieldValue)


	lOutput	= config.INFLUXDB_MEASUREMENT

	if lTags != '':
		lOutput	+= ',' + lTags

	lOutput	+= ' '
	lOutput	+= lFields

	print(lOutput)



def __exportGenericJson(pMeasurementPath, pJson):

	if 'result' not in pJson:
		return

	# log.debug( "json_raw = %s" % json_raw )


	lTags = {
		"path"	:	pMeasurementPath
	}


	# Setup hashtable for results
	lFields	=	{}
	# Add the JSON answer's content as fields
	for lJsonTag in pJson['result']:
		lFields[lJsonTag]	=	pJson['result'][lJsonTag]


	__export(lTags, lFields)



def __tags_common():
	retval	=	''

	retval	+=	'endpoint'
	retval	+=	'='
	retval	+=	config.FREEBOX_HOST

	return retval
