#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

import os

from datetime import datetime

import application_config as config
import freebox.api as freebox_api


import logging

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


	lOutput	= config.measurement_namePrefix()

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
	retval	+=	config.freebox_hostname()

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
			# 		lJsonL3ConnCount = len(sys_json_raw['result'][lHostNbr]['l3connectivities'])
			# 		j=0
			# 		while j<lJsonL3ConnCount :
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


def	storage_disk():

	#
	#	Fetch switch ports list to retrieve ports IDs
	#
	json_raw = freebox_api.get_storage_disk()
	log.debug("json_raw= %s" % json_raw)
	
	log.warn("Unimplemented method.")

	if 'result' not in json_raw:
		return

	# TODO:

	# tag1="Disque"
	# tag2="NULL"
	# tag3="NULL"
	
	# if json_raw['success'] :
	# 	i=1
	# 	for disk_object in json_raw['result']:
	# 		tag2 = "dd-" + str(i)
	# 		if 'idle_duration' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'idle_duration'] = disk_object['idle_duration']
	# 		if 'read_error_requests' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'read_error_requests'] = disk_object['read_error_requests']
	# 		if 'read_requests' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'read_requests'] = disk_object['read_requests']
	# 		if 'spinning' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'spinning'] = disk_object['spinning']
	# 		if 'table_type' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'table_type'] = disk_object['table_type']
	# 		if 'firmware' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'firmware'] = disk_object['firmware']
	# 		if 'type' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'type'] = disk_object['type']
	# 		if 'idle' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'idle'] = disk_object['idle']
	# 		if 'connector' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'connector'] = disk_object['connector']
	# 		if 'id' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'dd_id'] = disk_object['id']
	# 		if 'write_error_requests' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'write_error_requests'] = disk_object['write_error_requests']
	# 		if 'state' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'state'] = disk_object['state']
	# 		if 'write_requests' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'write_requests'] = disk_object['write_requests']
	# 		if 'total_bytes' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'total_bytes'] = disk_object['total_bytes']
	# 		if 'model' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'model'] = disk_object['model']
	# 		if 'active_duration' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'active_duration'] = disk_object['active_duration']
	# 		if 'temp' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'temp'] = disk_object['temp']
	# 		if 'serial' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'serial'] = disk_object['serial']
	# 		if 'id' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'disk_id'] = disk_object['id']
	# 		# partitions :
	# 		#
	# 		if disk_object['partitions'] :
	# 			j=1
	# 			for partition in disk_object['partitions'] :
	# 				tag3="Part-"+str(j)
	# 				my_data[tag1+"."+tag2+"."+tag3+"."+'partition#'] = j
	# 				if 'fstype' in partition : my_data[tag1+"."+tag2+"."+tag3+"."+'fstype'] = partition['fstype']
	# 				if 'disk_id' in partition : my_data[tag1+"."+tag2+"."+tag3+"."+'part_disk_id'] = partition['disk_id']
	# 				if 'total_bytes' in partition : my_data[tag1+"."+tag2+"."+tag3+"."+'total_bytes'] = partition['total_bytes']
	# 				if 'free_bytes' in partition : my_data[tag1+"."+tag2+"."+tag3+"."+'free_bytes'] = partition['free_bytes']
	# 				if 'used_bytes' in partition : my_data[tag1+"."+tag2+"."+tag3+"."+'used_bytes'] = partition['used_bytes']
	# 				if 'label' in partition : my_data[tag1+"."+tag2+"."+tag3+"."+'label'] = partition['label']
	# 				if 'id' in partition : my_data[tag1+"."+tag2+"."+tag3+"."+'part_id'] = partition['id']
	# 				if 'disk_id' in partition : my_data[tag1+"."+tag2+"."+tag3+"."+'part_disk_id'] = partition['disk_id']
					
	# 				j=j+1
	# 		i=i+1



def	switch_ports():

	#
	#	Fetch switch ports list to retrieve ports IDs
	#
	switch_json_raw = freebox_api.get_switch_status()
	
	if 'result' not in switch_json_raw:
		return

	# log.debug("switch_json_raw['result'] = %s" % switch_json_raw['result'])

	lPortsIdList=[]
	for lJsonObjectPort in switch_json_raw['result']:
		lPortsIdList.append( lJsonObjectPort['id'] )


	#
	#	Use the list of ports IDs to retrieve each port statistics
	#
	for lPortId in lPortsIdList :
		log.debug("+-- lPortId: %s", lPortId)

		switch_port_stats = freebox_api.get_switch_port_stats( lPortId )
		log.debug("    +-- switch_port_stats = %s" % switch_port_stats)
	
		if 'result' not in switch_json_raw:
			return

		log.warn("Unimplemented method.")
# 		
# 		tag1="Port#"+str(i)
# 		tag2="Rx"
# 		my_data[tag1+"."+tag2+"."+tag3+"."+'bytes_rate'] = switch_port_stats['result']['rx_bytes_rate']  # bytes/s (?)
# #           my_data[tag1+"."+tag2+"."+tag3+"."+'bytes'] = switch_port_stats['result']['rx_bytes']            # pas de rx_bytes dans l'api !
# 		tag2="Tx"
# 		my_data[tag1+"."+tag2+"."+tag3+"."+'bytes_rate'] = switch_port_stats['result']['tx_bytes_rate']
# 		my_data[tag1+"."+tag2+"."+tag3+"."+'bytes'] = switch_port_stats['result']['tx_bytes']



def	wifi_ap():

	lMeasurementPath	=	"wifi/ap/stations"
	lTags	=	{
		'path'	:	lMeasurementPath
	}


	#
	#	Fetch Wifi Access Points list to retrieve AP IDs
	#
	lJsonObjectWifiApListQuery = freebox_api.get_wifi_accessPointsList()
	# log.debug("lJsonObjectWifiApListQuery = %s" % lJsonObjectWifiApListQuery )
	
	if 'result' not in lJsonObjectWifiApListQuery:
		return

	if lJsonObjectWifiApListQuery['success'] != True:
		log.error("Get access points list failed!")
		return


	#
	#	Use access points IDs to get stations list
	#
	lJsonObjectWifiApList = lJsonObjectWifiApListQuery['result']
	for lJsonObjectWifiAp in lJsonObjectWifiApList :
		log.debug("+-- lJsonObjectWifiAp ID = %s" % lJsonObjectWifiAp['id'] )

		lTags['ap_id']	=	lJsonObjectWifiAp['id']

		# Get stations list
		lJsonApStationsQuery = freebox_api.get_wifi_accessPoint_stations(lJsonObjectWifiAp['id'])
		# log.debug("    +-- lJsonApStationsQuery = %s" % lJsonApStationsQuery )
		
		if 'result' not in lJsonApStationsQuery:
			continue


		lApStationsCount=len(lJsonApStationsQuery['result'])
		lApStationNbr=0

		while lApStationNbr < lApStationsCount :
			lJsonApStation	=	lJsonApStationsQuery['result'][lApStationNbr]

			if 'mac' not in lJsonApStation:
				continue

			lTags['station_mac']	=	lJsonApStation['mac']
			lTags['station_hostname']	=	lJsonApStation['hostname']

			lTags['station_rx_bytes']	=	lJsonApStation['rx_bytes']
			lTags['station_rx_rate']	=	lJsonApStation['rx_rate']
			lTags['station_tx_bytes']	=	lJsonApStation['tx_bytes']
			lTags['station_tx_rate']	=	lJsonApStation['tx_rate']


			if 'host' not in lJsonApStation:
				log.warn("No host in AP %s station %s (%s)" % 
				lTags['ap_id'],
				lTags['station_mac'],
				lJsonApStation['hostname']	)
				continue

			lJsonApStationHost	=	lJsonApStation['host']


			if (	'primary_name'	not in	lJsonApStationHost
				or	'primary_name'	==	""	):
				log.warn("No 'primary_name' in AP %s station %s (%s) host! Skipping." % 
				lTags['ap_id'],
				lTags['station_mac'],
				lJsonApStation['hostname']	)
				continue
			lTags['primary_name']	=	lJsonApStationHost['primary_name']


			if (	'interface'	not in	lJsonApStationHost
				or	'interface'	==	""	):
				log.warn("No 'interface' in AP %s station %s (%s) host! Skipping." % 
				lTags['ap_id'],
				lTags['station_mac'],
				lJsonApStation['hostname']	)
				continue
			lTags['interface']	=	lJsonApStationHost['interface']


			lTags['host_type']	=	lJsonApStationHost['host_type']



			lL3ConnCount = len(lJsonApStationHost['l3connectivities'])
			lL3ConnNbr=0
			# log.debug("lL3ConnCount = %s" % lL3ConnCount)
			while lL3ConnNbr < lL3ConnCount :
				log.debug( "L3 connectivity %s of %s" % 
					(str(lL3ConnNbr + 1), str(lL3ConnCount))	)

				lJsonL3Connectivity	=	lJsonApStationHost['l3connectivities'][lL3ConnNbr]

				if lJsonL3Connectivity['af'] != "ipv4":
					log.debug("Not an IPv4 connectivity; Skipping.")

				else:
					lFields	=	{}

					lFields['l3_addr']	=	lJsonL3Connectivity['addr']
					lFields['l3_reachable']	=	lJsonL3Connectivity['reachable']
					lFields['l3_active']	=	lJsonL3Connectivity['active']
					lFields['l3_last_activity']	=	lJsonL3Connectivity['last_activity']
					
					lFields['l3_last_activity_date']	=	datetime.fromtimestamp(lJsonL3Connectivity['last_activity']).strftime("%c")


					__export(lTags, lFields)

				lL3ConnNbr	=	lL3ConnNbr + 1

			lApStationNbr	=	lApStationNbr + 1
