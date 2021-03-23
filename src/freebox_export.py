#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

import os

from datetime import datetime

import config
import freebox_api


import logging
FORMAT = "[%(filename)s +%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)



def __export(pTagsDict, pFieldsDict):

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



def __get_creation_date(file):
	stat = os.stat(file)
	return stat.st_mtime 


# fbx telegraf docker info
def application_infos(pFile, pVersion):

	# Convertir Timestamp en datetime
	update_date = datetime.fromtimestamp(__get_creation_date(__file__))
	update_str = datetime.ctime(update_date)

	lTags = {
		'name' : 'application_infos',
		'script_version' : pVersion,
		'file' : pFile,
	}

	lFields = {
		'last_updated' : update_str
	}

	__export(lTags, lFields)


def	connection():

	# Fetch connection stats
	json_raw = freebox_api.get_connection_stats()

	if 'result' not in json_raw:
		return


	# Setup hashtable for results
	lFields	=	{}

	# log.debug( "json_raw = %s" % json_raw )


	lTags = {
		"name"	:	'connection/common'
	}


	lFields.clear()
	# Add the JSON answer's content as fields
	for lJsonTag in json_raw['result']:
		if lJsonTag == 'ipv4_port_range':
			lFields['ipv4_port_range_begin']    =	json_raw['result'][lJsonTag][0]
			lFields['ipv4_port_range_end']      =	json_raw['result'][lJsonTag][1]
		else:
			lFields[lJsonTag]	=	json_raw['result'][lJsonTag]

	__export(lTags, lFields)


	# ffth for FFTH (default)
	# xdsl for xDSL
	lConnectionMedia	= json_raw['result']['media']


	# FTTH specific
	if lConnectionMedia == "ftth":
		connection_ftth()

	# xDSL specific
	elif lConnectionMedia == "xdsl":
		connection_xdsl()



def	connection_ftth():
	# Fetch connection stats
	json_raw = freebox_api.get_connection_ftth()

	__exportGenericJson('connection/ftth', json_raw)



def connection_xdsl():
	# Fetch connection stats
	json_raw = freebox_api.get_connection_xdsl()

	__exportGenericJson('connection/xdsl', json_raw)

	# 	if 'result' in json_raw:
	# 		my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_modulation'] = json_raw['result']['status']['modulation'] + " ("+json_raw['result']['status']['protocol']+")"  # in seconds

	# 		my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_uptime'] = json_raw['result']['status']['uptime']  # in seconds

	# 		my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_status_string'] = json_raw['result']['status']['status']
	# 		if json_raw['result']['status']['status'] == "down":  # unsynchronized
	# 			my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_status'] = 0
	# 		elif json_raw['result']['status']['status'] == "training":  # synchronizing step 1/4
	# 			my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_status'] = 1
	# 		elif json_raw['result']['status']['status'] == "started":  # synchronizing step 2/4
	# 			my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_status'] = 2
	# 		elif json_raw['result']['status']['status'] == "chan_analysis":  # synchronizing step 3/4
	# 			my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_status'] = 3
	# 		elif json_raw['result']['status']['status'] == "msg_exchange":  # synchronizing step 4/4
	# 			my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_status'] = 4
	# 		elif json_raw['result']['status']['status'] == "showtime":  # ready
	# 			my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_status'] = 5
	# 		elif json_raw['result']['status']['status'] == "disabled":  # disabled
	# 			my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_status'] = 6
	# 		else:  # unknown
	# 			my_data['xdsl_status'] = 999

	# 		if 'es' in json_raw['result']['down']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_down_es'] = json_raw['result']['down']['es']  # increment
	# 		if 'attn' in json_raw['result']['down']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_down_attn'] = json_raw['result']['down']['attn']  # in dB
	# 		if 'snr' in json_raw['result']['down']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_down_snr'] = json_raw['result']['down']['snr']  # in dB
	# 		if 'rate' in json_raw['result']['down']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_down_rate'] = json_raw['result']['down']['rate']  # ATM rate in kbit/s
	# 		if 'hec' in json_raw['result']['down']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_down_hec'] = json_raw['result']['down']['hec']  # increment
	# 		if 'crc' in json_raw['result']['down']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_down_crc'] = json_raw['result']['down']['crc']  # increment
	# 		if 'ses' in json_raw['result']['down']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_down_ses'] = json_raw['result']['down']['ses']  # increment
	# 		if 'fec' in json_raw['result']['down']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_down_fec'] = json_raw['result']['down']['fec']  # increment
	# 		if 'maxrate' in json_raw['result']['down']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_down_maxrate'] = json_raw['result']['down']['maxrate']  # ATM max rate in kbit/s
	# 		if 'rtx_tx' in json_raw['result']['down']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_down_rtx_tx'] = json_raw['result']['down']['rtx_tx']  # G.INP on/off
	# 		if 'rtx_c' in json_raw['result']['down']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_down_rtx_c'] = json_raw['result']['down']['rtx_c']  # G.INP corrected
	# 		if 'rtx_uc' in json_raw['result']['down']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_down_rtx_uc'] = json_raw['result']['down']['rtx_uc']  # G.INP uncorrected

	# 		if 'es' in json_raw['result']['up']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_up_es'] = json_raw['result']['up']['es']
	# 		if 'attn' in json_raw['result']['up']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_up_attn'] = json_raw['result']['up']['attn']
	# 		if 'snr' in json_raw['result']['up']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_up_snr'] = json_raw['result']['up']['snr']
	# 		if 'rate' in json_raw['result']['up']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_up_rate'] = json_raw['result']['up']['rate']
	# 		if 'hec' in json_raw['result']['up']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_up_hec'] = json_raw['result']['up']['hec']
	# 		if 'crc' in json_raw['result']['up']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_up_crc'] = json_raw['result']['up']['crc']
	# 		if 'ses' in json_raw['result']['up']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_up_ses'] = json_raw['result']['up']['ses']
	# 		if 'fec' in json_raw['result']['up']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_up_fec'] = json_raw['result']['up']['fec']
	# 		if 'maxrate' in json_raw['result']['up']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_up_maxrate'] = json_raw['result']['up']['maxrate']
	# 		if 'rtx_tx' in json_raw['result']['up']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_up_rtx_tx'] = json_raw['result']['up']['rtx_tx']
	# 		if 'rtx_c' in json_raw['result']['up']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_up_rtx_c'] = json_raw['result']['up']['rtx_c']  # G.INP corrected
	# 		if 'rtx_uc' in json_raw['result']['up']: my_data[tag1+"."+tag2+"."+tag3+"."+'xdsl_up_rtx_uc'] = json_raw['result']['up']['rtx_uc']  # G.INP uncorrected



def lan_config():
	# Fetch JSON data
	json_raw = freebox_api.get_lan_config()

	__exportGenericJson('lan/config', json_raw)



def lan_interfaces():

	lMeasurementPath	=	"lan/interface"
	# # Fetch JSON data
	# json_raw = freebox_api.get_lan_interfaces()


	# if 'result' not in pJson:
	# 	return

	# log.debug( "json_raw = %s" % json_raw )


	# lTags = {
	# 	"name"	:	pMeasurementPath
	# }


	# # Setup hashtable for results
	# lFields	=	{}
	# # Add the JSON answer's content as fields
	# for lJsonTag in pJson['result']:
	# 	lFields[lJsonTag]	=	pJson['result'][lJsonTag]


	# __export(lTags, lFields)


	# Fetch JSON data
	sys_json_raw = freebox_api.get_lan_interfaces()
	
	if 'result' not in sys_json_raw:
		return

	lIfacesCount	=	len(sys_json_raw['result'])
	lIfaceNbr	=	0
	while lIfaceNbr < lIfacesCount:
		lTags = {
			"path"	:	lMeasurementPath
		}
		
		# Setup hashtable for results
		lFields	=	{}
		# Add the JSON answer's content as fields
		for lJsonKey in sys_json_raw['result'][lIfaceNbr]:
			lJsonValue	=	sys_json_raw['result'][lIfaceNbr][lJsonKey]

			if lJsonKey == 'name':
				# This data is considered as a tag
				lTags["iface_name"]	=	lJsonValue

			else:
				lFields[lJsonKey]	=	lJsonValue

		lIfaceNbr	=	lIfaceNbr + 1

		__export(lTags, lFields)



def lan_interfaces_hosts():

	lMeasurementPath	=	"lan/browser/interface/hosts"

	# liste des stations -X
	# API V8

	# API V8
	# chercher la liste des interfaces
	sys_json_raw = freebox_api.get_lan_interfaces()
	if 'result' not in sys_json_raw:
		return


	#
	# Set a list of known interfaces names
	#
	# lIfacesCount	=	len(sys_json_raw['result'])
	lInterfaceNamesList=[]

	for lInterfaceObj in sys_json_raw['result'] :
		lInterfaceNamesList.append(lInterfaceObj['name'])


	#
	# Iterate over interfaces and retrieve their data
	#
	for lInterfaceName in lInterfaceNamesList :

		sys_json_raw = freebox_api.get_lan_interface_hostsList(lInterfaceName)
		
		# If the request didn't return any data, continue to next interface
		if 'result' not in sys_json_raw:
			continue

		lTags = {
			"path"	:	lMeasurementPath
		}
		
		lHostsCount	=	len(sys_json_raw['result'])
		lHostNbr	=	0
		while lHostNbr < lHostsCount :

			# lTags['iface_name']	=	lInterfaceName # Already accessible in hosts data

			lHostNode	=	sys_json_raw['result'][lHostNbr]

			# log.debug("%s" % sys_json_raw['result'][lHostNbr])

			# log.debug("Host: %s (%s)" % 
			# 	(	lHostNode['id'],
			# 		lHostNode['default_name']	)	)

			#
			#	Iterate over available keys
			#
			##  @brief  Setup hashtable for results
			lFields	=	{}
			for lJsonKey in lHostNode:
				lJsonValue	=	lHostNode[lJsonKey]

				if	(	lJsonKey	==	'id'
					or	lJsonKey	==	'active'
					or	lJsonKey	==	'default_name'
					or	lJsonKey	==	'vendor_name'
					or	lJsonKey	==	'host_type'
					or	lJsonKey	==	'interface'
					or	lJsonKey	==	'persistent'
					or	lJsonKey	==	'primary_name'
					or	lJsonKey	==	'primary_name_manual'
					or	lJsonKey	==	'reachable'	):
					# This data is considered as a tag
					lTags[lJsonKey]	=	lJsonValue

				elif	lJsonKey	==	'names':
					lan_interfaces_host_names(lHostNode)

				elif	lJsonKey	==	'l2ident':
					lan_interfaces_host_l2ident(lHostNode)

				elif	lJsonKey	==	'l3connectivities':
					lan_interfaces_host_l3connectivities(lHostNode)

				elif	lJsonKey	==	'access_point':
					lan_interfaces_host_accessPoint(lHostNode)

				else:	# last_activity, last_time_reachable
					# log.debug("Unknown/unused key: lJsonKey = %s" % lJsonKey)
					lFields[lJsonKey]	=	lJsonValue


			# TODO continue clean here (then do CPU temp fetch)
			# if 'l3connectivities' in sys_json_raw['result'][lHostNbr]:
			# 		length_l3_conn = len(sys_json_raw['result'][lHostNbr]['l3connectivities'])
			# 		j=0
			# 		while j<length_l3_conn :
			# 			if sys_json_raw['result'][lHostNbr]['l3connectivities'][j]['addr'] != "" :
			# 				if 'id' in sys_json_raw['result'][lHostNbr]['l2ident']:
			# 					tag3=sys_json_raw['result'][lHostNbr]['l2ident']['id'] 
			# 					if sys_json_raw['result'][lHostNbr]['l3connectivities'][j]['af']=="ipv4":
			# 						my_data[tag1+"."+tag2+"."+tag3+"."+'addr']=sys_json_raw['result'][lHostNbr]['l3connectivities'][j]['addr']
			# 						my_data[tag1+"."+tag2+"."+tag3+"."+'last_activity']=datetime.fromtimestamp(sys_json_raw['result'][lHostNbr]['l3connectivities'][j]['last_activity']).strftime("%c")
			# 						if 'primary_name' in sys_json_raw['result'][lHostNbr]:my_data[tag1+"."+tag2+"."+tag3+"."+'primary_name']=sys_json_raw['result'][lHostNbr]['primary_name']
			# 						if 'host_type' in sys_json_raw['result'][lHostNbr]:my_data[tag1+"."+tag2+"."+tag3+"."+'host_type']=sys_json_raw['result'][lHostNbr]['host_type']
			# 						if 'active' in sys_json_raw['result'][lHostNbr]:my_data[tag1+"."+tag2+"."+tag3+"."+'active']=sys_json_raw['result'][lHostNbr]['active']
			# 			j=j+1

			__export(lTags, lFields)

			lHostNbr	=	lHostNbr + 1



def	lan_interfaces_host_accessPoint(pJsonInterfaceHostNode):

	lMeasurementPath	=	"lan/browser/interface/hosts/access_point"

	# If the request didn't return any data, continue to next interface
	if 'access_point' not in pJsonInterfaceHostNode:
		return

	lTags = {
		"path"	:	lMeasurementPath,
		"interface"	:	pJsonInterfaceHostNode['interface'],
		"id"	:	pJsonInterfaceHostNode['id'],
		"default_name"	:	pJsonInterfaceHostNode['default_name'],
		"primary_name"	:	pJsonInterfaceHostNode['primary_name']
	}

	lNodeAPData	=	pJsonInterfaceHostNode['access_point']

	# Setup hashtable for results
	lFields	=	{}
	# Add the JSON answer's content as fields
	# lConnectivitiesCount	=	len(lNodeL3Data)
	# lConnectivityNbr	=	0
	# while lConnectivityNbr < lConnectivitiesCount :
	for lJsonKey in lNodeAPData:
		lJsonValue	=	lNodeAPData[lJsonKey]

		if	(	lJsonKey	==	'connectivity_type'
			or	lJsonKey	==	'mac'
			or	lJsonKey	==	'type'
			or	lJsonKey	==	'uid'	):

			# This data is considered as a tag
			lTags[lJsonKey]	=	lJsonValue

		elif	(	lJsonKey	==	'ethernet_information'	):
			lTags['ethernet_information_duplex']	=	lJsonValue['duplex']
			lTags['ethernet_information_speed']	=	lJsonValue['speed']

			lFields['ethernet_information_link']	=	lJsonValue['link']

		elif	(	lJsonKey	==	'wifi_information'	):
			lTags['wifi_information_band']	=	lJsonValue['band']
			lTags['wifi_information_ssid']	=	lJsonValue['ssid']

			lFields['wifi_information_signal']	=	lJsonValue['signal']

		else:
			lFields[lJsonKey]	=	lJsonValue

	__export(lTags, lFields)

		# lConnectivityNbr	=	lConnectivityNbr + 1



def	lan_interfaces_host_l2ident(pJsonInterfaceHostNode):

	lMeasurementPath	=	"lan/browser/interface/hosts/l2ident"

	# If the request didn't return any data, continue to next interface
	if 'l2ident' not in pJsonInterfaceHostNode:
		return


	lTags = {
		"path"	:	lMeasurementPath,
		"interface"	:	pJsonInterfaceHostNode['interface'],
		"id"	:	pJsonInterfaceHostNode['id'],
		"default_name"	:	pJsonInterfaceHostNode['default_name'],
		"primary_name"	:	pJsonInterfaceHostNode['primary_name']
	}

	lNodeL2IdentData	=	pJsonInterfaceHostNode['l2ident']

	# Setup hashtable for results
	lFields	=	{}
	# Add the JSON answer's content as fields
	for lJsonKey in lNodeL2IdentData:
		lJsonValue	=	lNodeL2IdentData[lJsonKey]

		if	(	lJsonKey	==	'type'	):

			# This data is considered as a tag
			lTags[lJsonKey]	=	lJsonValue

		else:
			lFields[lJsonKey]	=	lJsonValue


	__export(lTags, lFields)



def	lan_interfaces_host_l3connectivities(pJsonInterfaceHostNode):

	lMeasurementPath	=	"lan/browser/interface/hosts/l3connectivities"

	# If the request didn't return any data, continue to next interface
	if 'l3connectivities' not in pJsonInterfaceHostNode:
		return

	lTags = {
		"path"	:	lMeasurementPath,
		"interface"	:	pJsonInterfaceHostNode['interface'],
		"id"	:	pJsonInterfaceHostNode['id'],
		"default_name"	:	pJsonInterfaceHostNode['default_name'],
		"primary_name"	:	pJsonInterfaceHostNode['primary_name']
	}

	lNodeL3Data	=	pJsonInterfaceHostNode['l3connectivities']

	# Setup hashtable for results
	lFields	=	{}
	# Add the JSON answer's content as fields
	lConnectivitiesCount	=	len(lNodeL3Data)
	lConnectivityNbr	=	0
	while lConnectivityNbr < lConnectivitiesCount :
		for lJsonKey in lNodeL3Data[lConnectivityNbr]:
			lJsonValue	=	lNodeL3Data[lConnectivityNbr][lJsonKey]

			if	(	lJsonKey	==	'active'
				or	lJsonKey	==	'af'
				or	lJsonKey	==	'reachable'	):

				# This data is considered as a tag
				lTags[lJsonKey]	=	lJsonValue

			else:
				lFields[lJsonKey]	=	lJsonValue

		__export(lTags, lFields)

		lConnectivityNbr	=	lConnectivityNbr + 1



def	lan_interfaces_host_names(pJsonInterfaceHostNode):

	lMeasurementPath	=	"lan/browser/interface/hosts/names"

	# If the request didn't return any data, continue to next interface
	if 'names' not in pJsonInterfaceHostNode:
		return

	lTags = {
		"path"	:	lMeasurementPath,
		"interface"	:	pJsonInterfaceHostNode['interface'],
		"id"	:	pJsonInterfaceHostNode['id'],
		"default_name"	:	pJsonInterfaceHostNode['default_name'],
		"primary_name"	:	pJsonInterfaceHostNode['primary_name']
	}

	lNodeNamesData	=	pJsonInterfaceHostNode['names']

	# Setup hashtable for results
	lFields	=	{}
	# Add the JSON answer's content as fields
	lNamesCount	=	len(lNodeNamesData)
	lNameNbr	=	0
	while lNameNbr < lNamesCount :
		for lJsonKey in lNodeNamesData[lNameNbr]:
			lJsonValue	=	lNodeNamesData[lNameNbr][lJsonKey]

			if	(	lJsonKey	==	'source'	):

				# This data is considered as a tag
				lTags[lJsonKey]	=	lJsonValue

			else:
				lFields[lJsonKey]	=	lJsonValue

		__export(lTags, lFields)

		lNameNbr	=	lNameNbr + 1



def	system():

	lMeasurementPath	=	"system"

	sys_json_raw = freebox_api.get_system()
	if 'result' not in sys_json_raw:
		return

	# log.debug( "sys_json_raw['result'] == %s" % sys_json_raw['result'])

	lTags = {
		"path"	:	lMeasurementPath,

		# "interface"	:	pJsonInterfaceHostNode['interface'],
		# "id"	:	pJsonInterfaceHostNode['id'],
		# "default_name"	:	pJsonInterfaceHostNode['default_name'],
		# "primary_name"	:	pJsonInterfaceHostNode['primary_name']
	}

	lNodeData	=	sys_json_raw['result']

	#
	#	Prepare tags and fields of default item
	#
	# Setup hashtable for results
	lFields	=	{}
	# Add the JSON answer's content as fields
	# lConnectivitiesCount	=	len(lNodeL3Data)
	# lConnectivityNbr	=	0
	# while lConnectivityNbr < lConnectivitiesCount :
	for lJsonKey in lNodeData:
		lJsonValue	=	lNodeData[lJsonKey]

		if	(	lJsonKey	==	'board_name'
			# or	lJsonKey	==	'firmware_version'
			or	lJsonKey	==	'mac'
			or	lJsonKey	==	'serial'	):

			# This data is considered as a tag
			lTags[lJsonKey]	=	lJsonValue

		else:
			# disk_status
			# uptime
			# uptime_val
			# user_main_storage
			# box_authenticated
			lFields[lJsonKey]	=	lJsonValue

	# Export default item
	__export(lTags, lFields)

	if	(	'fans'	in lNodeData	):
		system_fans(lTags, lNodeData)

	if	(	'model_info'	in lNodeData	):
		system_modelInfo(lTags, lNodeData)

	if	(	'sensors'	in lNodeData	):
		system_sensors(lTags, lNodeData)

		# lConnectivityNbr	=	lConnectivityNbr + 1



def	system_fans(pTags, pNodeSystem):

	lMeasurementPath	=	"system/fans"

	if 'fans' not in pNodeSystem:
		return

	lTags	=	pTags

	lTags['path']	=	lMeasurementPath


	lNodeData	=	pNodeSystem['fans']

	# Setup hashtable for results
	lFields	=	{}
	# Add the JSON answer's content as fields
	lFansCount	=	len(lNodeData)
	lFanNbr	=	0
	while lFanNbr < lFansCount :
		for lJsonKey in lNodeData[lFanNbr]:
			lJsonValue	=	lNodeData[lFanNbr][lJsonKey]

			if	(	lJsonKey	==	'id'
				or	lJsonKey	==	'name'	):

				# This data is considered as a tag
				lTags[lJsonKey]	=	lJsonValue

			else:
				lFields[lJsonKey]	=	lJsonValue

		__export(lTags, lFields)

		lFanNbr	=	lFanNbr + 1



def	system_modelInfo(pTags, pNodeSystem):

	lMeasurementPath	=	"system/model_info"

	if 'model_info' not in pNodeSystem:
		return

	lTags	=	pTags

	lTags['path']	=	lMeasurementPath


	lNodeData	=	pNodeSystem['model_info']

	# Setup hashtable for results
	lFields	=	{}
	# Add the JSON answer's content as fields
	for lJsonKey in lNodeData:
		lJsonValue	=	lNodeData[lJsonKey]

		# if	(	lJsonKey	==	'id'
		# 	or	lJsonKey	==	'name'	):

		# 	# This data is considered as a tag
		# 	lTags[lJsonKey]	=	lJsonValue

		# else:
		lFields[lJsonKey]	=	lJsonValue

	__export(lTags, lFields)




def	system_sensors(pTags, pNodeSystem):

	lMeasurementPath	=	"system/sensors"

	if 'sensors' not in pNodeSystem:
		return

	lTags	=	pTags

	lTags['path']	=	lMeasurementPath


	lNodeData	=	pNodeSystem['sensors']

	# Setup hashtable for results
	lFields	=	{}
	# Add the JSON answer's content as fields
	lSensorsCount	=	len(lNodeData)
	lSensorNbr	=	0
	while lSensorNbr < lSensorsCount :
		for lJsonKey in lNodeData[lSensorNbr]:
			lJsonValue	=	lNodeData[lSensorNbr][lJsonKey]

			if	(	lJsonKey	==	'id'
				or	lJsonKey	==	'name'	):

				# This data is considered as a tag
				lTags[lJsonKey]	=	lJsonValue

			else:
				lFields[lJsonKey]	=	lJsonValue

		__export(lTags, lFields)

		lSensorNbr	=	lSensorNbr + 1




	# 	if 'uptime_val' in sys_json_raw['result']:my_data[tag1+"."+tag2+"."+tag3+"."+'sys_uptime_val'] = sys_json_raw['result']['uptime_val']   # Uptime, in seconds
	# 	if 'uptime' in sys_json_raw['result']:my_data[tag1+"."+tag2+"."+tag3+"."+'uptime'] = sys_json_raw['result']['uptime']           # uptime in readable format ?

	# 	if 'firmware_version' in sys_json_raw['result']:my_data[tag1+"."+tag2+"."+tag3+"."+'firmware_version'] = sys_json_raw['result']['firmware_version']  # Firmware version  
	# 	if 'board_name' in sys_json_raw['result']:my_data[tag1+"."+tag2+"."+tag3+"."+'board_name'] = sys_json_raw['result']['board_name']
	# 	if 'disk_status' in sys_json_raw['result']:my_data[tag1+"."+tag2+"."+tag3+"."+'disk_status'] = sys_json_raw['result']['disk_status']
	# 	if 'user_main_storage' in sys_json_raw['result']:my_data[tag1+"."+tag2+"."+tag3+"."+'user_main_storage'] = sys_json_raw['result']['user_main_storage']
		

	# 	if 'mac' in sys_json_raw['result']:
	# 		if 'model_info' in sys_json_raw['result']:
	# 			if 'has_ext_telephony' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'has_ext_telephony'] = sys_json_raw['result']['model_info']['has_ext_telephony']
	# 			if 'has_ext_telephony' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'has_ext_telephony'] = sys_json_raw['result']['model_info']['has_ext_telephony']
	# 			if 'has_speakers_jack' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'has_speakers_jack'] = sys_json_raw['result']['model_info']['has_speakers_jack']
	# 			if 'wifi_type' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'wifi_type'] = sys_json_raw['result']['model_info']['wifi_type']
	# 			if 'pretty_name' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'pretty_name'] = sys_json_raw['result']['model_info']['pretty_name']
	# 			if 'customer_hdd_slots' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'customer_hdd_slots'] = sys_json_raw['result']['model_info']['customer_hdd_slots']
	# 			if 'name' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'name'] = sys_json_raw['result']['model_info']['name']
	# 			if 'has_speakers' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'has_speakers'] = sys_json_raw['result']['model_info']['has_speakers']
	# 			if 'internal_hdd_size' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'internal_hdd_size'] = sys_json_raw['result']['model_info']['internal_hdd_size']
	# 			if 'has_femtocell_exp' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'has_femtocell_exp'] = sys_json_raw['result']['model_info']['has_femtocell_exp']
	# 			if 'has_internal_hdd' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'has_internal_hdd'] = sys_json_raw['result']['model_info']['has_internal_hdd']
	# 			if 'has_dect' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'has_dect'] = sys_json_raw['result']['model_info']['has_dect']
				
	# 	if 'fans' in sys_json_raw['result']: # c'est une liste
	# 		i=1
	# 		for fan_object in sys_json_raw['result']['fans']:
	# 			tag2 = "Fan"
	# 			my_data[tag1+"."+tag2+"."+tag3+"."+'id'] = fan_object['id']
	# 			my_data[tag1+"."+tag2+"."+tag3+"."+'name'] = fan_object['name']
	# 			my_data[tag1+"."+tag2+"."+tag3+"."+'value'] = fan_object['value']
	# 			i=i+1
				
	# 	if 'sensors' in sys_json_raw['result']: # c'est une liste
	# 		i=1
	# 		for sensor_object in sys_json_raw['result']['sensors']:
	# 			tag2 = "Sensor"
	# 			tag3 = sensor_object['id']
	# 			my_data[tag1+"."+tag2+"."+tag3+"."+'id'] = sensor_object['id']
	# 			my_data[tag1+"."+tag2+"."+tag3+"."+'name'] = sensor_object['name']
	# 			my_data[tag1+"."+tag2+"."+tag3+"."+'value'] = sensor_object['value']
	# 			i=i+1