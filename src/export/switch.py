#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

##  @see    https://dev.freebox.fr/sdk/os/switch/

import freebox.api as freebox_api

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

def	_mac_list(pJsonSwitchPortStatus, pTags):

	if 'mac_list' not in pJsonSwitchPortStatus:
		return

	lTags	=	pTags.copy()

	lJsonHostsMacList	=	pJsonSwitchPortStatus['mac_list']
	for lJsonHostMac in lJsonHostsMacList:

		lTags['switch_port_mac_host']	=	lJsonHostMac['mac']

		export._generic.measurement(
			pApiPath	=	'switch/status',
			pApiSubpath	=	'mac_list',
			pApiAttribute	=	'hostname',
			pAttrValue	=	lJsonHostMac['hostname'],
			pTagsDict	=	lTags
			# pFieldsDict	=	lFields
		)

# ##############################################################################
# ##############################################################################

def	status():

	switch_json_raw = freebox_api.get_switch_status()
	if 'result' not in switch_json_raw:
		return
	# log.debug( "switch_json_raw['result'] == %s" % switch_json_raw['result'])

	lApiPath	=	"switch/status"
	lJsonRootSS	=	switch_json_raw['result']


	# Add the JSON answer's content as fields
	lPortsCount	=	len(lJsonRootSS)
	lPortNbr	=	0
	while lPortNbr < lPortsCount :

		lJsonPort	=	lJsonRootSS[lPortNbr]

		lTags	=	{
			'port_id'	:	lJsonPort['id']
		}

		for lJsonKey in lJsonPort:
			lJsonValue	=	lJsonPort[lJsonKey]

			if	(	lJsonKey	==	'id'	):
				# This data is used as a tag, skip it.
				continue

			elif	(	lJsonKey	==	'mac_list'	):
				_mac_list(lJsonPort, lTags)

			else:
				export._generic.measurement(
					pApiPath	=	lApiPath,
					pApiAttribute	=	lJsonKey,
					pAttrValue	=	lJsonValue,
					pTagsDict	=	lTags
				)

		lPortNbr	=	lPortNbr + 1


# ##############################################################################
# ##############################################################################