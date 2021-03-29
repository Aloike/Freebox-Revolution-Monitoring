#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

import os

from datetime import datetime

import freebox.api as fbx_api

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

def	all():

	sys_json_raw = fbx_api.get_connection_stats()
	if 'result' not in sys_json_raw:
		return
	# log.debug( "sys_json_raw['result'] == %s" % sys_json_raw['result'])


	lJsonRoot	=	sys_json_raw['result']


	#
	#	Prepare tags and fields of default item
	#	
	
	for lJsonKey in lJsonRoot:

		if	(	lJsonKey	==	'ipv4_port_range'	):
			# Those values identify subpath; they will be managed separately.
			continue

		lJsonValue	=	lJsonRoot[lJsonKey]

		export._generic.measurement(
			pApiPath	=	'connection',
			pApiAttribute	=	lJsonKey,
			pAttrValue	=	lJsonValue
		)


	if	(	'ipv4_port_range'	in lJsonRoot	):
		_ipv4_port_range(lJsonRoot)


	# ffth for FFTH (default)
	# xdsl for xDSL
	lConnectionMedia	= lJsonRoot['media']

	# FTTH specific
	if lConnectionMedia == "ftth":
		ftth()

	# xDSL specific
	elif lConnectionMedia == "xdsl":
		xdsl()

# ##############################################################################
# ##############################################################################

def	_ipv4_port_range(pJsonRoot):

	if 'ipv4_port_range' not in pJsonRoot:
		return

	lJsonData	=	pJsonRoot['ipv4_port_range']


	export._generic.measurement(
		pApiPath	=	'connection',
		pApiSubpath	=	'ipv4_port_range',
		pApiAttribute	=	'begin',
		pAttrValue	=	lJsonData[0]#,
		# pTagsDict	=	lTags,
		# pFieldsDict	=	lFields
	)

	export._generic.measurement(
		pApiPath	=	'connection',
		pApiSubpath	=	'ipv4_port_range',
		pApiAttribute	=	'end',
		pAttrValue	=	lJsonData[1]#,
		# pTagsDict	=	lTags,
		# pFieldsDict	=	lFields
	)


# ##############################################################################
# ##############################################################################

def	ftth():

	# Fetch connection stats
	lJsonAnswer	=	fbx_api.get_connection_ftth()
	if 'result' not in lJsonAnswer:
		return
	# log.debug( "lJsonAnswer == %s" % lJsonAnswer )


	export._generic.genericJson(
		pApiPath		=	'connection/ftth',
		pJsonRoot		=	lJsonAnswer,
		pJsonObjectName	=	'result'
	)

# ##############################################################################
# ##############################################################################

def xdsl():

	lJsonAnswer	=	fbx_api.get_connection_xdsl()
	if 'result' not in lJsonAnswer:
		return
	# log.debug( "lJsonAnswer == %s" % lJsonAnswer )


	export._generic.genericJson(
		pApiPath		=	'connection/xdsl',
		pJsonRoot		=	lJsonAnswer,
		pJsonObjectName	=	'result'
	)
