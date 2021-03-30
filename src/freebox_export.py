#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

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
