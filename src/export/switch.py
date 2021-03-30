#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

##  @see    https://dev.freebox.fr/sdk/os/switch/

import freebox.api as freebox_api

import export._generic

from .objects	import SwitchPortStats

# ##############################################################################
# ##############################################################################
#
#	Logging configuration
#
import logging

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

def	ports_stats():

	#
	#	Fetch switch ports list to retrieve ports IDs
	#
	lJsonSwitchPortStatusList	=	freebox_api.get_switch_status()

	if 'result' not in lJsonSwitchPortStatusList:
		log.error("No result in lJsonSwitchPortStatusList: %s" %
			lJsonSwitchPortStatusList
		)
		return

	# log.debug("switch_json_raw['result'] = %s" % switch_json_raw['result'])

	lPortsIdList=[]
	for lJsonSwitchPortStatus in lJsonSwitchPortStatusList['result']:
		lPortsIdList.append( lJsonSwitchPortStatus['id'] )


	#
	#	Use the list of ports IDs to retrieve each port statistics
	#
	for lPortId in lPortsIdList :

		lTags	=	{
			'port_id'	:	lPortId
		}

		lJsonSwitchPortStatsAnswer	=	freebox_api.get_switch_port_stats( lPortId )
		# log.debug("    +-- lJsonSwitchPortStats = %s" % lJsonSwitchPortStats)

		if 'result' not in lJsonSwitchPortStatsAnswer:
			log.error("No result in lJsonSwitchPortStatsAnswer: %s" %
				lJsonSwitchPortStatsAnswer
			)
			continue

		SwitchPortStats.fromJson(
			pApiPath	=	"switch/port/stats",
			pApiSubpath	=	'',
			pTagsDict	=	lTags,
			pJsonObjectSwitchPortStats	=	lJsonSwitchPortStatsAnswer['result']
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