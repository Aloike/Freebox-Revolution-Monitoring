#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

import freebox.api as fbx_api

import export._generic

from .objects	import LanHost

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

def	config():

	# Fetch connection stats
	lJsonAnswer	=	fbx_api.get_lan_config()
	log.debug( "lJsonAnswer == %s" % lJsonAnswer )
	if 'result' not in lJsonAnswer:
		return


	export._generic.genericJson(
		pApiPath		=	'lan/config',
		pJsonRoot		=	lJsonAnswer,
		pJsonObjectName	=	'result'
	)

# ##############################################################################
# ##############################################################################

def interfaces():

	lApiPath	=	"lan/browser/interfaces"

	#
	#	Get the list of LAN interfaces
	#

	# Fetch JSON data
	lJsonLanInterfacesList = fbx_api.get_lan_interfaces()
	log.debug("lJsonLanInterfacesList = %s" % lJsonLanInterfacesList)

	if 'result' not in lJsonLanInterfacesList:
		return

	lIfacesCount	=	len(lJsonLanInterfacesList['result'])
	lIfaceNbr	=	0
	while lIfaceNbr < lIfacesCount:

		lJsonLanInterface	=	lJsonLanInterfacesList['result'][lIfaceNbr]

		lTags	=	{
			'interface_name'	:	lJsonLanInterface['name']
		}


		# # Setup hashtable for results
		# lFields	=	{}

		# Add the JSON answer's content as fields
		for lJsonKey in lJsonLanInterface:

			if lJsonKey != 'name':	# 'name' is considered as a tag
				export._generic.measurement(
					pApiPath	=	lApiPath,
					# pApiSubpath	=	'fans',
					pApiAttribute	=	lJsonKey,
					pAttrValue	=	lJsonLanInterface[lJsonKey],
					pTagsDict	=	lTags#,
					# pFieldsDict	=	lFields
				)

		lIfaceNbr	=	lIfaceNbr + 1

# ##############################################################################
# ##############################################################################

def interfaces_hosts():

	# liste des stations -X
	# API V8

	# API V8
	# chercher la liste des interfaces
	lJsonLanInterfacesList	=	fbx_api.get_lan_interfaces()
	if 'result' not in lJsonLanInterfacesList:
		return


	#
	# Set a list of known interfaces names
	#
	lInterfaceNamesList=[]
	for lInterfaceObj in lJsonLanInterfacesList['result'] :
		lInterfaceNamesList.append(lInterfaceObj['name'])


	#
	# Iterate over interfaces and retrieve their data
	#
	lApiPath	=	"lan/browser/interface"
	for lInterfaceName in lInterfaceNamesList :

		lJsonAnswerInterfaceHostsList = fbx_api.get_lan_interface_hostsList(lInterfaceName)

		# If the request didn't return any data, continue to next interface
		if 'result' not in lJsonAnswerInterfaceHostsList:
			continue
		lJsonObjectLanHostsList	=	lJsonAnswerInterfaceHostsList['result']


		lTags = {
			"interface_name"	:	lInterfaceName
		}


		lHostsCount	=	len(lJsonObjectLanHostsList)
		lHostNbr	=	0
		while lHostNbr < lHostsCount :

			lJsonObjectLanHost	=	lJsonObjectLanHostsList[lHostNbr]
			log.debug("lJsonObjectLanHost = %s" % lJsonObjectLanHost)

			LanHost.fromJson(
				lApiPath,
				'',
				lTags,
				lJsonObjectLanHost
			)

			lHostNbr	=	lHostNbr + 1