#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

import freebox.api as fbx_api

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
	for lInterfaceName in lInterfaceNamesList :

		lApiPath	=	"lan/browser/interface"
		lJsonInterfaceHostsList = fbx_api.get_lan_interface_hostsList(lInterfaceName)

		# If the request didn't return any data, continue to next interface
		if 'result' not in lJsonInterfaceHostsList:
			continue

		lTags = {
			"interface_name"	:	lInterfaceName
		}

		lHostsCount	=	len(lJsonInterfaceHostsList['result'])
		lHostNbr	=	0
		while lHostNbr < lHostsCount :

			# lTags['iface_name']	=	lInterfaceName # Already accessible in hosts data

			lJsonHost	=	lJsonInterfaceHostsList['result'][lHostNbr]
			log.debug("lJsonHost = %s" % lJsonHost)

			lTags['host_id']	=	lJsonHost['id']

			# log.debug("Host: %s (%s)" % 
			# 	(	lJsonHost['id'],
			# 		lJsonHost['default_name']	)	)

			#
			#	Iterate over available keys
			#
			# ##  @brief  Setup hashtable for results
			# lFields	=	{}
			for lJsonKey in lJsonHost:
				# lJsonValue	=	lJsonHost[lJsonKey]

				if	(	lJsonKey	==	'id'
			# 		or	lJsonKey	==	'active'
			# 		or	lJsonKey	==	'default_name'
			# 		or	lJsonKey	==	'vendor_name'
			# 		or	lJsonKey	==	'host_type'
			# 		or	lJsonKey	==	'interface'
			# 		or	lJsonKey	==	'persistent'
			# 		or	lJsonKey	==	'primary_name'
			# 		or	lJsonKey	==	'primary_name_manual'
			# 		or	lJsonKey	==	'reachable'
					):
					# This data is considered as a tag
			# 		lTags[lJsonKey]	=	lJsonValue
					continue

				elif	lJsonKey	==	'names':
					_interfaces_host_names(lJsonHost, lTags)

				elif	lJsonKey	==	'l2ident':
					_interfaces_host_l2ident(lJsonHost, lTags)

				elif	lJsonKey	==	'l3connectivities':
					_interfaces_host_l3connectivities(lJsonHost, lTags)

				elif	lJsonKey	==	'access_point':
					_interfaces_host_accessPoint(lJsonHost, lTags)

				else:	# last_activity, last_time_reachable
					export._generic.measurement(
						pApiPath	=	lApiPath,
						# pApiSubpath	=	'fans',
						pApiAttribute	=	lJsonKey,
						pAttrValue	=	lJsonHost[lJsonKey],
						pTagsDict	=	lTags#,
						# pFieldsDict	=	lFields
					)

			lHostNbr	=	lHostNbr + 1

# ##############################################################################
# ##############################################################################

def	_interfaces_host_accessPoint(pJsonInterfaceHost, pTagsDict):

	lApiPath	=	"lan/browser/interface"
	lApiSubpath	=	"hosts/access_point"


	# If the request didn't return any data, continue to next interface
	# log.debug("pJsonInterfaceHost = %s" % pJsonInterfaceHost)
	if 'access_point' not in pJsonInterfaceHost:
		return

	lTagsDict	=	pTagsDict.copy()

	lJsonAccessPoint	=	pJsonInterfaceHost['access_point']

	# lTagsDict['type']	=	lJsonL2IdentData['type']

	# Export each value as a measurement
	for lJsonKey in lJsonAccessPoint:
		# lJsonValue	=	lJsonL2IdentData[lJsonKey]

	# 	if	(	lJsonKey	==	'type'	):
	# 		# This data is considered as a tag
	# 		continue

		if lJsonKey == 'ethernet_information':
			_interfaces_host_accessPoint_ethernet_information(
				lJsonAccessPoint,
				lTagsDict
			)
		elif lJsonKey == 'wifi_information':
			_interfaces_host_accessPoint_wifi_information(
				lJsonAccessPoint,
				lTagsDict
			)
		else:
			# lFields[lJsonKey]	=	lJsonValue
			export._generic.measurement(
				pApiPath	=	lApiPath,
				pApiSubpath	=	lApiSubpath,
				pApiAttribute	=	lJsonKey,
				pAttrValue	=	lJsonAccessPoint[lJsonKey],
				pTagsDict	=	lTagsDict#,
				# pFieldsDict	=	lFields
			)

	# TODO:

	# # lTags = {
	# # 	"path"	:	lMeasurementPath,
	# # 	"interface"	:	pJsonInterfaceHost['interface'],
	# # 	"id"	:	pJsonInterfaceHost['id'],
	# # 	"default_name"	:	pJsonInterfaceHost['default_name'],
	# # 	"primary_name"	:	pJsonInterfaceHost['primary_name']
	# # }

	# lNodeAPData	=	pJsonInterfaceHost['access_point']

	# # Setup hashtable for results
	# lFields	=	{}
	# # Add the JSON answer's content as fields
	# # lConnectivitiesCount	=	len(lJsonL3ConnList)
	# # lConnectivityNbr	=	0
	# # while lConnectivityNbr < lConnectivitiesCount :
	# for lJsonKey in lNodeAPData:
	# 	lJsonValue	=	lNodeAPData[lJsonKey]

	# 	if	(	lJsonKey	==	'connectivity_type'
	# 		or	lJsonKey	==	'mac'
	# 		or	lJsonKey	==	'type'
	# 		or	lJsonKey	==	'uid'	):

	# 		# This data is considered as a tag
	# 		lTags[lJsonKey]	=	lJsonValue

	# 	elif	(	lJsonKey	==	'ethernet_information'	):
	# 		lTags['ethernet_information_duplex']	=	lJsonValue['duplex']
	# 		lTags['ethernet_information_speed']	=	lJsonValue['speed']

	# 		lFields['ethernet_information_link']	=	lJsonValue['link']

	# 	elif	(	lJsonKey	==	'wifi_information'	):
	# 		lTags['wifi_information_band']	=	lJsonValue['band']
	# 		lTags['wifi_information_ssid']	=	lJsonValue['ssid']

	# 		lFields['wifi_information_signal']	=	lJsonValue['signal']

	# 	else:
	# 		lFields[lJsonKey]	=	lJsonValue

	# log.error("Unimplemented export!")
	# # __export(lTags, lFields)

# ##############################################################################
# ##############################################################################

def	_interfaces_host_accessPoint_ethernet_information(pJsonAccessPoint, pTagsDict):

	lApiPath	=	"lan/browser/interface"
	lApiSubpath	=	"hosts/access_point/ethernet_information"


	# If the request didn't return any data, continue to next interface
	if 'ethernet_information' not in pJsonAccessPoint:
		return

	lTagsDict	=	pTagsDict.copy()

	lJsonEthInfo	=	pJsonAccessPoint['ethernet_information']

	# Export each value as a measurement
	for lJsonKey in lJsonEthInfo:

		export._generic.measurement(
			pApiPath	=	lApiPath,
			pApiSubpath	=	lApiSubpath,
			pApiAttribute	=	lJsonKey,
			pAttrValue	=	lJsonEthInfo[lJsonKey],
			pTagsDict	=	lTagsDict#,
			# pFieldsDict	=	lFields
		)

# ##############################################################################
# ##############################################################################

def	_interfaces_host_accessPoint_wifi_information(pJsonAccessPoint, pTagsDict):

	lApiPath	=	"lan/browser/interface"
	lApiSubpath	=	"hosts/access_point/wifi_information"


	# If the request didn't return any data, continue to next interface
	if 'wifi_information' not in pJsonAccessPoint:
		return

	lTagsDict	=	pTagsDict.copy()

	lJsonWifiInfo	=	pJsonAccessPoint['wifi_information']

	# Export each value as a measurement
	for lJsonKey in lJsonWifiInfo:

		export._generic.measurement(
			pApiPath	=	lApiPath,
			pApiSubpath	=	lApiSubpath,
			pApiAttribute	=	lJsonKey,
			pAttrValue	=	lJsonWifiInfo[lJsonKey],
			pTagsDict	=	lTagsDict#,
			# pFieldsDict	=	lFields
		)

# ##############################################################################
# ##############################################################################

def	_interfaces_host_l2ident(pJsonInterfaceHost, pTagsDict):

	lApiPath	=	"lan/browser/interface"
	lApiSubpath	=	"hosts/l2ident"


	# If the request didn't return any data, continue to next interface
	if 'l2ident' not in pJsonInterfaceHost:
		return

	lTagsDict	=	pTagsDict.copy()

	lJsonL2IdentData	=	pJsonInterfaceHost['l2ident']

	lTagsDict['type']	=	lJsonL2IdentData['type']

	# Add the JSON answer's content as fields
	for lJsonKey in lJsonL2IdentData:
		# lJsonValue	=	lJsonL2IdentData[lJsonKey]

		if	(	lJsonKey	==	'type'	):
			# This data is considered as a tag
			continue

		else:
			# lFields[lJsonKey]	=	lJsonValue
			export._generic.measurement(
				pApiPath	=	lApiPath,
				pApiSubpath	=	lApiSubpath,
				pApiAttribute	=	lJsonKey,
				pAttrValue	=	lJsonL2IdentData[lJsonKey],
				pTagsDict	=	lTagsDict#,
				# pFieldsDict	=	lFields
			)

# ##############################################################################
# ##############################################################################

def	_interfaces_host_l3connectivities(pJsonInterfaceHost, pTagsDict):

	lApiPath	=	"lan/browser/interface"
	lApiSubpath	=	"host/l3connectivities"

	# If the request didn't return any data, continue to next interface
	if 'l3connectivities' not in pJsonInterfaceHost:
		return

	lTagsDict	=	pTagsDict.copy()

	lJsonL3ConnList	=	pJsonInterfaceHost['l3connectivities']

	lConnectivitiesCount	=	len(lJsonL3ConnList)
	lConnectivityNbr	=	0
	while lConnectivityNbr < lConnectivitiesCount :
		lJsonL3Connectivity	=	lJsonL3ConnList[lConnectivityNbr]

		lTagsDict['l3connectivities_af']	=	lJsonL3Connectivity['af']
		lTagsDict['l3connectivities_addr']	=	lJsonL3Connectivity['addr']
		lTagsDict['l3connectivities_active']	=	lJsonL3Connectivity['active']
		lTagsDict['l3connectivities_reachable']	=	lJsonL3Connectivity['reachable']

		for lJsonKey in lJsonL3Connectivity:
			# lJsonValue	=	lJsonL3ConnList[lConnectivityNbr][lJsonKey]

			if	(	lJsonKey	==	'active'
				or	lJsonKey	==	'addr'
				or	lJsonKey	==	'af'
				or	lJsonKey	==	'reachable'	):

				# This data is considered as a tag
				# lTags[lJsonKey]	=	lJsonValue
				continue

			else:
				# lFields[lJsonKey]	=	lJsonValue
				export._generic.measurement(
					pApiPath	=	lApiPath,
					pApiSubpath	=	lApiSubpath,
					pApiAttribute	=	lJsonKey,
					pAttrValue	=	lJsonL3Connectivity[lJsonKey],
					pTagsDict	=	lTagsDict#,
					# pFieldsDict	=	lFields
				)

		lConnectivityNbr	=	lConnectivityNbr + 1

# ##############################################################################
# ##############################################################################

def	_interfaces_host_names(pJsonInterfaceHost, pTagsDict):

	lApiPath	=	"lan/browser/interface"
	lApiSubpath	=	"host/names"

	# If the request didn't return any data, continue to next interface
	if 'names' not in pJsonInterfaceHost:
		return

	lTagsDict	=	pTagsDict.copy()

	lJsonNamesList	=	pJsonInterfaceHost['names']

	lNamesCount	=	len(lJsonNamesList)
	lNameNbr	=	0
	while lNameNbr < lNamesCount :
		lJsonName	=	lJsonNamesList[lNameNbr]

		lTagsDict['nameIdx']	=	lNameNbr

		for lJsonKey in lJsonName:
				export._generic.measurement(
					pApiPath	=	lApiPath,
					pApiSubpath	=	lApiSubpath,
					pApiAttribute	=	lJsonKey,
					pAttrValue	=	lJsonName[lJsonKey],
					pTagsDict	=	lTagsDict#,
					# pFieldsDict	=	lFields
				)

		lNameNbr	=	lNameNbr + 1

# ##############################################################################
# ##############################################################################
