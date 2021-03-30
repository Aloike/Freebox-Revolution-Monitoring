#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

from ..	import	_generic

from .	import	LanHost
from .	import	WifiStationFlags
from .	import	WifiStationStats

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

def	fromJson(pApiPath, pApiSubpath, pTagsDict, pJsonObjectWifiStation):

	if 'id' not in pJsonObjectWifiStation:
		log.error("Found an AP station without id!")
		return


	lTags	=	pTagsDict.copy()

	# Add the station unique ID in the tags to identify the station
	lTags['station_id']	=	pJsonObjectWifiStation['id']


	#
	#	Iterate over station attributes and export them
	#
	for lJsonKey in pJsonObjectWifiStation:

		#
		#	Those keys are used in tags, skip them.
		#
		if	(	lJsonKey	==	'id'
			# or	lJsonKey	==	'hostname'
				):
			continue

		#
		# Those keys identify subpath; they are managed separately.
		#
		elif	(	lJsonKey	==	'flags'	):
			WifiStationFlags.fromJson(
				pApiPath	=	pApiPath,
				pApiSubpath	=	pApiSubpath + '/' + lJsonKey,
				pTagsDict	=	lTags,
				pJsonObjectWifiStationFlags	=	pJsonObjectWifiStation[lJsonKey]
			)

		elif	(	lJsonKey	==	'host'	):
			LanHost.fromJson(
				pApiPath	=	pApiPath,
				pApiSubpath	=	pApiSubpath + '/' + lJsonKey,
				pTagsDict	=	lTags,
				pJsonObjectLanHost	=	pJsonObjectWifiStation[lJsonKey]
			)

		elif	(	lJsonKey	==	'last_rx'
				or	lJsonKey	==	'last_tx'	):
			WifiStationStats.fromJson(
				pApiPath	=	pApiPath,
				pApiSubpath	=	pApiSubpath + '/' + lJsonKey,
				pTagsDict	=	lTags,
				pJsonObjectWifiStationStats	=	pJsonObjectWifiStation[lJsonKey]
			)

		#
		# Default export rule
		#
		else:
			_generic.measurement(
				pApiPath	=	pApiPath,
				# pApiSubpath	=	'fans',
				pApiAttribute	=	lJsonKey,
				pAttrValue	=	pJsonObjectWifiStation[lJsonKey],
				pTagsDict	=	lTags#,
				# pFieldsDict	=	lFields
			)

	# lTags['station_rx_bytes']	=	pJsonObjectWifiStation['rx_bytes']
	# lTags['station_rx_rate']	=	pJsonObjectWifiStation['rx_rate']
	# lTags['station_tx_bytes']	=	pJsonObjectWifiStation['tx_bytes']
	# lTags['station_tx_rate']	=	pJsonObjectWifiStation['tx_rate']


	# if 'host' not in pJsonObjectWifiStation:
	# 	log.warn("No host in AP %s station %s (%s)" % 
	# 	lTags['ap_id'],
	# 	lTags['station_mac'],
	# 	pJsonObjectWifiStation['hostname']	)
	# 	continue

	# _ap_station_host(pJsonObjectWifiStation)

# ##############################################################################
# ##############################################################################