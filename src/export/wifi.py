#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

import freebox.api as fbx_api

import export._generic

from .objects	import	WifiStation

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

def	accessPoints_stations():

	#
	#	Fetch Wifi Access Points list to retrieve AP IDs
	#
	lJsonObjectWifiApListQuery = fbx_api.get_wifi_accessPointsList()
	# log.debug("lJsonObjectWifiApListQuery = %s" % lJsonObjectWifiApListQuery )
	
	if 'result' not in lJsonObjectWifiApListQuery:
		return

	if lJsonObjectWifiApListQuery['success'] != True:
		log.error("Get access points list failed!")
		return


	#
	#	Use access points IDs to get stations list
	#
	lApiPath	=	"wifi/ap/stations"
	lTags	=	{}
	lJsonObjectWifiApList = lJsonObjectWifiApListQuery['result']
	for lJsonObjectWifiAp in lJsonObjectWifiApList :
		log.debug("+-- lJsonObjectWifiAp ID = %s" % lJsonObjectWifiAp['id'] )

		lTags['ap_id']	=	lJsonObjectWifiAp['id']

		# Get stations list
		lJsonApStationsQuery = fbx_api.get_wifi_accessPoint_stations(lJsonObjectWifiAp['id'])
		
		if 'result' not in lJsonApStationsQuery:
			continue


		#
		# Iterate over stations list
		#
		lApStationsCount=len(lJsonApStationsQuery['result'])
		lApStationNbr=0
		while lApStationNbr < lApStationsCount :
			lJsonApStation	=	lJsonApStationsQuery['result'][lApStationNbr]

			WifiStation.fromJson(
				pApiPath	=	lApiPath,
				pApiSubpath	=	'',
				pTagsDict	=	lTags,
				pJsonObjectWifiStation	=	lJsonApStation
			)

			lApStationNbr	=	lApStationNbr + 1

# ##############################################################################
# ##############################################################################