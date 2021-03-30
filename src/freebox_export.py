#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

import application_config as config
import freebox.api as freebox_api


import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


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
