#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621


from __future__ import print_function
from __future__ import unicode_literals

import requests
import os
# import json
# import hmac
import time
import argparse
import sys
import time
from time import strftime, gmtime
from datetime import datetime
# from hashlib import sha1


# To install the latest version of Unidecode from the Python package index, use these commands:
# $ pip install unidecode
from unidecode import unidecode
#
# if sys.version_info >= (3, 0):
#     import configparser as configp
# else:
#     import ConfigParser as configp


import config
import freebox_export
import export.connection
import export.lan
import export.system
import export.switch
import freebox.api as freebox_api


import logging
FORMAT = "[%(filename)s +%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

#
# Freebox API SDK / Docs: http://dev.freebox.fr/sdk/os/login/
# version 8
#

VERSION = "1.0.0 2021/03/22"

# version 059
#         prise en compte api v8 (option -H en particulier)
#         meilleure prise en compte des autres plateforme que Fbox Rev.
#              avec en particulier meilleur traitement des listes de paramètres.

def get_creation_date(file):
    stat = os.stat(file)
    return stat.st_mtime 



def get_and_print_metrics(creds, s_switch, s_ports, s_sys, s_disk, s_lan, s_wifi, s_lan_interfaces, s_interfaces_hosts):
    #freebox_app_id = "fr.freebox.seximonitor"
    #freebox_app_id = "fr.freebox.grafanamonitor"
    freebox_app_id = creds['app_id']
    freebox_app_token = creds['app_token']
    freebox_track_id = creds['track_id']
    #

    # setup output dataformat, default Graphite

    # tag for influxdb
    # regle de nommage : mettre les informations (rx, tx, port 1, ...) dans les tags.
    # ne mettre que des noms de valeurs de variables generiques : bytes, bits, rate, bandwidth, firmware .....
    # les tags sont la pour donnner le contexte
    # cela permettra des tris et regroupements plus complets sous grafana
    # 3 tags séparé par des "."
    # chaque valeur aura donc un nom de la forme : tag1.tag2.tag3.valeur
    #
    tag1=tag2=tag3=""

    dataformat='influxdb'


    # Fetch session_token
    freebox_api.session_open(freebox_app_id, freebox_app_token, freebox_track_id )


    # Setup hashtable for results
    my_data = {}

    # Fetch connection stats
    json_raw = freebox_api.get_connection_stats()

    # log.debug( "json_raw = %s" % json_raw )


    #
    # General infos
    # #
    # # option -L
    # #
    # if s_lan:
    #     sys_json_raw = freebox_api.get_lan_config()
    #     tag1="Lan Config"
    #     tag2="NULL"
    #     tag3="NULL"
    #     if 'result' in sys_json_raw:
    #         if 'mode' in sys_json_raw['result']:my_data[tag1+"."+tag2+"."+tag3+"."+'lan_mode'] = sys_json_raw['result']['mode']
    #         if 'ip' in sys_json_raw['result']:my_data[tag1+"."+tag2+"."+tag3+"."+'lan_ip'] = sys_json_raw['result']['ip']
    #         if 'name' in sys_json_raw['result']:my_data[tag1+"."+tag2+"."+tag3+"."+'lan_name'] = sys_json_raw['result']['name']
    #         if 'name_dns' in sys_json_raw['result']:my_data[tag1+"."+tag2+"."+tag3+"."+'lan_name_dns'] = sys_json_raw['result']['name_dns']
    #         if 'name_mdns' in sys_json_raw['result']:my_data[tag1+"."+tag2+"."+tag3+"."+'lan_name_mdns'] = sys_json_raw['result']['name_mdns']
    #         if 'name_netbios' in sys_json_raw['result']:my_data[tag1+"."+tag2+"."+tag3+"."+'lan_name_netbios'] = sys_json_raw['result']['name_netbios']

    # #
    # # option -I
    # #   
    # if s_lan_interfaces:
    #     sys_json_raw = freebox_api.get_lan_interfaces()
        
    #     tag1="Interfaces"
    #     tag2="NULL"
    #     tag3="NULL"
        
    #     if 'result' in sys_json_raw:

    #         l=len(sys_json_raw['result'])
    #         i=0
    #         while i<l:
    #             tag2=("if#%s" % i)
    #             my_data[tag1+"."+tag2+"."+tag3+"."+'name']=sys_json_raw['result'][i]['name']
    #             my_data[tag1+"."+tag2+"."+tag3+"."+'host_count']=sys_json_raw['result'][i]['host_count']
    #             i=i+1

    # #
    # # liste des stations -X
    # # API V8

    #     if s_interfaces_hosts:
            
    #         # API V8
    #         # chercher la liste des interfaces
    #         sys_json_raw = freebox_api.get_lan_interfaces()
    #         if 'result' in sys_json_raw:
    #             l=len(sys_json_raw['result'])
    #             listeinterfaces=[]
    #             interf_objet = sys_json_raw['result']

    #             for intobject in interf_objet :
    #                 listeinterfaces.append(intobject['name'])

    #             for interface in listeinterfaces :
    #                 sys_json_raw = freebox_api.get_lan_interface_hostsList(interface)
    #                 if 'result' in sys_json_raw:
    #                     l=len(sys_json_raw['result'])
    #                     tag1="hosts_list"
    #                     k=0
    #                     while k<l :
    #                         tag2=interface
    #                         tag3="NULL"
    #                         if 'l3connectivities' in sys_json_raw['result'][k]:
    #                             length_l3_conn = len(sys_json_raw['result'][k]['l3connectivities'])
    #                             j=0
    #                             while j<length_l3_conn :
    #                                 if sys_json_raw['result'][k]['l3connectivities'][j]['addr'] != "" :
    #                                     if 'id' in sys_json_raw['result'][k]['l2ident']:
    #                                         tag3=sys_json_raw['result'][k]['l2ident']['id'] 
    #                                         if sys_json_raw['result'][k]['l3connectivities'][j]['af']=="ipv4":
    #                                             my_data[tag1+"."+tag2+"."+tag3+"."+'addr']=sys_json_raw['result'][k]['l3connectivities'][j]['addr']
    #                                             my_data[tag1+"."+tag2+"."+tag3+"."+'last_activity']=datetime.fromtimestamp(sys_json_raw['result'][k]['l3connectivities'][j]['last_activity']).strftime("%c")
    #                                             if 'primary_name' in sys_json_raw['result'][k]:my_data[tag1+"."+tag2+"."+tag3+"."+'primary_name']=sys_json_raw['result'][k]['primary_name']
    #                                             if 'host_type' in sys_json_raw['result'][k]:my_data[tag1+"."+tag2+"."+tag3+"."+'host_type']=sys_json_raw['result'][k]['host_type']
    #                                             if 'active' in sys_json_raw['result'][k]:my_data[tag1+"."+tag2+"."+tag3+"."+'active']=sys_json_raw['result'][k]['active']
    #                                 j=j+1
    #                         k=k+1

# #
# # option -H
# # updated for V8
#     if s_sys:
#         sys_json_raw = freebox_api.get_system()
        
#         tag1="System"
#         tag2="NULL"
#         tag3="NULL"        

#         if 'result' in sys_json_raw:
#             if 'uptime_val' in sys_json_raw['result']:my_data[tag1+"."+tag2+"."+tag3+"."+'sys_uptime_val'] = sys_json_raw['result']['uptime_val']   # Uptime, in seconds
#             if 'uptime' in sys_json_raw['result']:my_data[tag1+"."+tag2+"."+tag3+"."+'uptime'] = sys_json_raw['result']['uptime']           # uptime in readable format ?

#             if 'firmware_version' in sys_json_raw['result']:my_data[tag1+"."+tag2+"."+tag3+"."+'firmware_version'] = sys_json_raw['result']['firmware_version']  # Firmware version  
#             if 'board_name' in sys_json_raw['result']:my_data[tag1+"."+tag2+"."+tag3+"."+'board_name'] = sys_json_raw['result']['board_name']
#             if 'disk_status' in sys_json_raw['result']:my_data[tag1+"."+tag2+"."+tag3+"."+'disk_status'] = sys_json_raw['result']['disk_status']
#             if 'user_main_storage' in sys_json_raw['result']:my_data[tag1+"."+tag2+"."+tag3+"."+'user_main_storage'] = sys_json_raw['result']['user_main_storage']
            

#             if 'mac' in sys_json_raw['result']:
#             	if 'model_info' in sys_json_raw['result']:
#             		if 'has_ext_telephony' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'has_ext_telephony'] = sys_json_raw['result']['model_info']['has_ext_telephony']
#             		if 'has_ext_telephony' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'has_ext_telephony'] = sys_json_raw['result']['model_info']['has_ext_telephony']
#             		if 'has_speakers_jack' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'has_speakers_jack'] = sys_json_raw['result']['model_info']['has_speakers_jack']
#             		if 'wifi_type' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'wifi_type'] = sys_json_raw['result']['model_info']['wifi_type']
#             		if 'pretty_name' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'pretty_name'] = sys_json_raw['result']['model_info']['pretty_name']
#             		if 'customer_hdd_slots' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'customer_hdd_slots'] = sys_json_raw['result']['model_info']['customer_hdd_slots']
#             		if 'name' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'name'] = sys_json_raw['result']['model_info']['name']
#             		if 'has_speakers' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'has_speakers'] = sys_json_raw['result']['model_info']['has_speakers']
#             		if 'internal_hdd_size' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'internal_hdd_size'] = sys_json_raw['result']['model_info']['internal_hdd_size']
#             		if 'has_femtocell_exp' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'has_femtocell_exp'] = sys_json_raw['result']['model_info']['has_femtocell_exp']
#             		if 'has_internal_hdd' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'has_internal_hdd'] = sys_json_raw['result']['model_info']['has_internal_hdd']
#             		if 'has_dect' in sys_json_raw['result']['model_info']:my_data[tag1+"."+tag2+"."+tag3+"."+'has_dect'] = sys_json_raw['result']['model_info']['has_dect']
            		
#             if 'fans' in sys_json_raw['result']: # c'est une liste
#                 i=1
#                 for fan_object in sys_json_raw['result']['fans']:
#                 	tag2 = "Fan"
#                 	my_data[tag1+"."+tag2+"."+tag3+"."+'id'] = fan_object['id']
#                 	my_data[tag1+"."+tag2+"."+tag3+"."+'name'] = fan_object['name']
#                 	my_data[tag1+"."+tag2+"."+tag3+"."+'value'] = fan_object['value']
#                 	i=i+1
                	
#             if 'sensors' in sys_json_raw['result']: # c'est une liste
#                 i=1
#                 for sensor_object in sys_json_raw['result']['sensors']:
#                 	tag2 = "Sensor"
#                 	tag3 = sensor_object['id']
#                 	my_data[tag1+"."+tag2+"."+tag3+"."+'id'] = sensor_object['id']
#                 	my_data[tag1+"."+tag2+"."+tag3+"."+'name'] = sensor_object['name']
#                 	my_data[tag1+"."+tag2+"."+tag3+"."+'value'] = sensor_object['value']
#                 	i=i+1
# #
# # option -S

#     if s_switch:
#         switch_json_raw = freebox_api.get_switch_status()
        
#         tag1="Switch"
#         tag2="NULL"
#         tag3="NULL" 
        
#         if 'result' in switch_json_raw:
#             for i in switch_json_raw['result']:
#                 # 0 down, 1 up
#                 tag2="link#"+str(i['id'])
#                 if i['link'] == "up" : my_data[tag1+"."+tag2+"."+tag3+"."+'Etat'] = 1
#                 else: my_data[tag1+"."+tag2+"."+tag3+"."+'Etat'] = 0
#                 # 0 auto, 1 10Base-T, 2 100Base-T, 3 1000Base-T
#                 # Fbox POP : ?? pour port#3 2.5G  ??
#                 # In fact the duplex is appended like 10BaseT-HD, 1000BaseT-FD, 1000BaseT-FD
#                 # So just is an "in" because duplex isn't really usefull
#                 if "10BaseT" in i['mode']:
#                     my_data[tag1+"."+tag2+"."+tag3+"."+'mode'] = 1
#                 elif "100BaseT" in i['mode']:
#                     my_data[tag1+"."+tag2+"."+tag3+"."+'mode'] = 2
#                 elif "1000BaseT" in i['mode']:
#                     my_data[tag1+"."+tag2+"."+tag3+"."+'mode'] = 3
#                 else:
#                     my_data[tag1+"."+tag2+"."+tag3+"."+'mode'] = 0  # auto

# #
# # Option -P
# #
# # Switch ports status
#     if s_ports:
    	 	        
#         tag1="Ports"
#         tag2="NULL"
#         tag3="NULL"
    
#         switch_json_raw = freebox_api.get_switch_status()
#         listeid=[]
#         if 'result' in switch_json_raw:
#             for i in switch_json_raw['result']:
#                 listeid.append(i['id'])

#         for i in listeid :  
#             switch_port_stats = freebox_api.get_switch_port_stats(i)
#             tag1="Port#"+str(i)
#             tag2="Rx"
#             my_data[tag1+"."+tag2+"."+tag3+"."+'bytes_rate'] = switch_port_stats['result']['rx_bytes_rate']  # bytes/s (?)
# #           my_data[tag1+"."+tag2+"."+tag3+"."+'bytes'] = switch_port_stats['result']['rx_bytes']            # pas de rx_bytes dans l'api !
#             tag2="Tx"
#             my_data[tag1+"."+tag2+"."+tag3+"."+'bytes_rate'] = switch_port_stats['result']['tx_bytes_rate']
#             my_data[tag1+"."+tag2+"."+tag3+"."+'bytes'] = switch_port_stats['result']['tx_bytes']

# #
# # Option -D
# # updated for V8 (liste de disque)
# # Fetch internal disk stats
#     if s_disk:
#         json_raw = freebox_api.get_storage_disk()
        
#         tag1="Disque"
#         tag2="NULL"
#         tag3="NULL"
        
#         if json_raw['success'] :
#             i=1
#             for disk_object in json_raw['result']:
#                 tag2 = "dd-" + str(i)
#                 if 'idle_duration' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'idle_duration'] = disk_object['idle_duration']
#                 if 'read_error_requests' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'read_error_requests'] = disk_object['read_error_requests']
#                 if 'read_requests' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'read_requests'] = disk_object['read_requests']
#                 if 'spinning' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'spinning'] = disk_object['spinning']
#                 if 'table_type' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'table_type'] = disk_object['table_type']
#                 if 'firmware' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'firmware'] = disk_object['firmware']
#                 if 'type' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'type'] = disk_object['type']
#                 if 'idle' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'idle'] = disk_object['idle']
#                 if 'connector' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'connector'] = disk_object['connector']
#                 if 'id' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'dd_id'] = disk_object['id']
#                 if 'write_error_requests' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'write_error_requests'] = disk_object['write_error_requests']
#                 if 'state' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'state'] = disk_object['state']
#                 if 'write_requests' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'write_requests'] = disk_object['write_requests']
#                 if 'total_bytes' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'total_bytes'] = disk_object['total_bytes']
#                 if 'model' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'model'] = disk_object['model']
#                 if 'active_duration' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'active_duration'] = disk_object['active_duration']
#                 if 'temp' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'temp'] = disk_object['temp']
#                 if 'serial' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'serial'] = disk_object['serial']
#                 if 'id' in disk_object:my_data[tag1+"."+tag2+"."+tag3+"."+'disk_id'] = disk_object['id']
#                 # partitions :
#                 #
#                 if disk_object['partitions'] :
#                    j=1
#                    for partition in disk_object['partitions'] :
#                        tag3="Part-"+str(j)
#                        my_data[tag1+"."+tag2+"."+tag3+"."+'partition#'] = j
#                        if 'fstype' in partition : my_data[tag1+"."+tag2+"."+tag3+"."+'fstype'] = partition['fstype']
#                        if 'disk_id' in partition : my_data[tag1+"."+tag2+"."+tag3+"."+'part_disk_id'] = partition['disk_id']
#                        if 'total_bytes' in partition : my_data[tag1+"."+tag2+"."+tag3+"."+'total_bytes'] = partition['total_bytes']
#                        if 'free_bytes' in partition : my_data[tag1+"."+tag2+"."+tag3+"."+'free_bytes'] = partition['free_bytes']
#                        if 'used_bytes' in partition : my_data[tag1+"."+tag2+"."+tag3+"."+'used_bytes'] = partition['used_bytes']
#                        if 'label' in partition : my_data[tag1+"."+tag2+"."+tag3+"."+'label'] = partition['label']
#                        if 'id' in partition : my_data[tag1+"."+tag2+"."+tag3+"."+'part_id'] = partition['id']
#                        if 'disk_id' in partition : my_data[tag1+"."+tag2+"."+tag3+"."+'part_disk_id'] = partition['disk_id']
                       
#                        j=j+1
#                 i=i+1
# #
# # Option -W
# # update for V8, prise en compte de la liste des AP.
# # Wifi stats
# #
#     if s_wifi:
        
#         sys_json_raw1 = freebox_api.get_wifi_accessPointsList()
#         if sys_json_raw1['success'] :
#             apwifilist = sys_json_raw1['result']
#             for ap in apwifilist : 
#                 sys_json_raw = freebox_api.get_wifi_accessPoint_stations(ap['id'])
#                 if 'result' in sys_json_raw:        
#                     l=len(sys_json_raw['result'])
#                     tag1="wifi_list"
#                     tag2=ap['name']
#                     # verifier qu'il n'y a pas de "." dans tag2 ! on les supprime
# #                    print("tag2 = ", tag2)
#                     j=0
#                     tagtemp = list(tag2)
#                     while  j < len(tagtemp):	
#                         if tagtemp[j] == ".": 
#                         	tagtemp[j] = ""
#                         j=j+1 
#                     tag2 = "".join(tagtemp)    
#                     tag3="NULL" 
#                     k=0

#                     while k<l :
#                        if 'mac' in sys_json_raw['result'][k]:
#                           tag3=sys_json_raw['result'][k]['mac']
#                           if 'host' in sys_json_raw['result'][k]:
#                               length_l3_conn = len(sys_json_raw['result'][k]['host']['l3connectivities'])
#                               if 'primary_name' in sys_json_raw['result'][k]['host']:
#                                    if sys_json_raw['result'][k]['host']['primary_name'] != "" : 
#                                          if 'interface' in sys_json_raw['result'][k]['host']:
#                                                if sys_json_raw['result'][k]['host']['interface'] != "" :
#                                                      m=0
#                                                      while m < length_l3_conn :
#                                                          if sys_json_raw['result'][k]['host']['l3connectivities'][m]['af'] == "ipv4":
#                                                              my_data[tag1+"."+tag2+"."+tag3+"."+'primary_name']=sys_json_raw['result'][k]['host']['primary_name']
#                                                              my_data[tag1+"."+tag2+"."+tag3+"."+'host_type']=sys_json_raw['result'][k]['host']['host_type']
#                                                              my_data[tag1+"."+tag2+"."+tag3+"."+'interface']=sys_json_raw['result'][k]['host']['interface']
#                                                              my_data[tag1+"."+tag2+"."+tag3+"."+'addripv4']=sys_json_raw['result'][k]['host']['l3connectivities'][m]['addr']
#                                                              my_data[tag1+"."+tag2+"."+tag3+"."+'reachable']=sys_json_raw['result'][k]['host']['l3connectivities'][m]['reachable']
#                                                              my_data[tag1+"."+tag2+"."+tag3+"."+'active']=sys_json_raw['result'][k]['host']['l3connectivities'][m]['active']
#                                                         # tx/rx bytes
#                                                              my_data[tag1+"."+tag2+"."+tag3+"."+'rx_bytes']=sys_json_raw['result'][k]['rx_bytes']
#                                                              my_data[tag1+"."+tag2+"."+tag3+"."+'rx_rate']=sys_json_raw['result'][k]['rx_rate']
#                                                              my_data[tag1+"."+tag2+"."+tag3+"."+'tx_bytes']=sys_json_raw['result'][k]['tx_bytes']
#                                                              my_data[tag1+"."+tag2+"."+tag3+"."+'tx_rate']=sys_json_raw['result'][k]['tx_rate']
#                                                              lasttimeactivity=sys_json_raw['result'][k]['host']['l3connectivities'][m]['last_activity']
#                                                              date_last_activity=datetime.fromtimestamp(lasttimeactivity)
#                                                              my_data[tag1+"."+tag2+"."+tag3+"."+'last_activity_date']=date_last_activity.strftime("%c")
#                                                              my_data[tag1+"."+tag2+"."+tag3+"."+'AP_ref']=ap['id']
#                                                          m=m+1   
#                        k=k+1

        
    
########################################################################################################################################################    
    # Switching between outputs formats 
    # c'est args.format qu'il faut utiliser, et non pas args.data_format.
    # if args.format == 'influxdb':
    if dataformat == 'influxdb' :

    # Prepping Influxdb Data format
        timestamp = int(time.time()) * 1000000
    
    # Output the information

        if tag1 == "": tag1="test-tag1"
        if tag2 == "": tag2="test-tag2"
        if tag3 == "": tag2="test-tag3"

#
# extraire les 3 tags
#
    # positions des 3 "." points séparateurs de tags

        for i in my_data:
            pos=[0,0,0]
            j=0
            k=0

            while  j < len(i):	
               if i[j] == ".":
                     pos[k]=j
                     k=k+1  
               j=j+1     
                 
            tag1=i[0:pos[0]]
            tag2=i[pos[0]+1:pos[1]]
            tag3=i[pos[1]+1:pos[2]]        	
#
# supprimer les blancs " " dans les tags par des "-"
#
            tag1=tag1.replace(" ","-")
            tag2=tag2.replace(" ","-")
            tag3=tag3.replace(" ","-")
        	


            # Add measurement name
            lOutputStr = config.INFLUXDB_MEASUREMENT

            # Add tags
            # lOutputStr  += ",endpoint=" + args.Endpoint
            lOutputStr  += "," + print_tag("endpoint", args.Endpoint)


            # Print the output string
            # TODO: print("%s" % (lOutputStr))


            if type(my_data[i]) == str:

# et dans le print on enlève les 3 tags de la partie my_data
# on va de pos[2]+1  à la fin de i
# je rajoute la suppression des accents
                my_data[i] = unidecode(my_data[i])
                print("%s,endpoint=%s,tag1=%s,tag2=%s,tag3=%s %s=\"%s\"" % (config.INFLUXDB_MEASUREMENT,args.Endpoint,tag1,tag2,tag3, i[pos[2]+1:], my_data[i]))
            else:         
                print("%s,endpoint=%s,tag1=%s,tag2=%s,tag3=%s %s=%s" % (config.INFLUXDB_MEASUREMENT,args.Endpoint,tag1,tag2,tag3, i[pos[2]+1:], my_data[i]))

    else:
    # Prepping Graphite Data format
        timestamp = int(time.time())

         # Output the information
        for i in my_data:
            print("freebox.%s %s %d" % (i, my_data[i], timestamp))


def print_tag(pTag, pValue):
    retval  = pTag + "="

    if type(pValue) == str:
        retval  +="\"" + pValue + "\""
    else:
        retval  += str(pValue)

    return retval



def register_status(creds):
    if not creds:
        print("Status: invalid config, auth not done.")
        print("Please run `%s --register` to register app." % sys.argv[0])
        return
    print("Status: auth already done")


def do_export(creds, s_switch, s_ports, s_sys, s_disk, s_lan, s_wifi, s_lan_interfaces, s_interfaces_hosts):
    #freebox_app_id = "fr.freebox.seximonitor"
    #freebox_app_id = "fr.freebox.grafanamonitor"
    freebox_app_id = creds['app_id']
    freebox_app_token = creds['app_token']
    freebox_track_id = creds['track_id']
    #

    # setup output dataformat, default Graphite

    # tag for influxdb
    # regle de nommage : mettre les informations (rx, tx, port 1, ...) dans les tags.
    # ne mettre que des noms de valeurs de variables generiques : bytes, bits, rate, bandwidth, firmware .....
    # les tags sont la pour donnner le contexte
    # cela permettra des tris et regroupements plus complets sous grafana
    # 3 tags séparé par des "."
    # chaque valeur aura donc un nom de la forme : tag1.tag2.tag3.valeur
    #
    # tag1=tag2=tag3=""

    # dataformat='influxdb'


    # Fetch session_token
    freebox_api.session_open(freebox_app_id, freebox_app_token, freebox_track_id )

    freebox_export.application_infos(__file__, VERSION)
    export.connection.all()

    #
    # option -L
    #
    if s_lan:
        export.lan.config()

    #
    # option -I
    #
    if s_lan_interfaces:
        freebox_export.lan_interfaces()

    #
    # option -X
    #
    if s_interfaces_hosts:
        freebox_export.lan_interfaces_hosts()

    #
    # option -H
    #
    if s_sys:
        export.system.all()

    #
    # option -S
    #
    if s_switch:
        export.switch.status()

    #
    # Option -P
    #
    # Switch ports status
    if s_ports:
        freebox_export.switch_ports()
        

    #
    # Option -D
    #
    # Fetch internal disk stats
    if s_disk:
        freebox_export.storage_disk()


    #
    # Option -W
    #
    # Wifi stats
    if s_wifi:
        freebox_export.wifi_ap()



# Main
if __name__ == '__main__':
    app_id='fr.freebox.grafanamonitor'
    app_name='GrafanaMonitor'   
    device_name='GrafanServer' 

    config.init()

    # freebox_api.init()


    parser = argparse.ArgumentParser(add_help=False)
    #helpgroup = parser.add_argument_group()
    parser.add_argument("-h", "--help", action="help", help="show this help message and exit")
    parser.add_argument('-s', '--register-status', dest='status', action='store_true', help="Get register status")
    parser.add_argument('-r', '--register', action='store_true', help="Register app with Freebox API")

    parser.add_argument('-n', '--appname',
                        dest='app_name',
            metavar='app_name',
                        help="Register with app_name")

    parser.add_argument('-i', '--appid',
                        dest='app_id',
            metavar='app_id',
                        help="Register with app_id")

    parser.add_argument('-d', '--devicename',
                        dest='device_name',
            metavar='device_name',
                        help="Register with device_name")

    parser.add_argument('-f', '--format',
                        dest='format',
            metavar='format',
            default='graphite',
                        help="Specify output format between graphite and influxdb")

    parser.add_argument('-e', '--endpoint',
                        dest='Endpoint',
            metavar='endpoint',
            default=config.FREEBOX_HOST,
                        help="Specify endpoint name or address")

    parser.add_argument('-S', '--switch-status',
                        dest='status_switch',
                        action='store_true',
                        help="Get and show switch status")

    parser.add_argument('-P', '--status-ports',
                        dest='status_ports',
                        action='store_true',
                        help="Get and show switch ports stats")

    parser.add_argument('-H', '--system',
                        dest='status_sys',
                        action='store_true',
                        help="Get and show system status")

    parser.add_argument('-D', '--internal-disk-usage',
                        dest='disk_usage',
                        action='store_true',
                        help="Get and show internal disk usage")

    parser.add_argument('-L', '--lan-config',
                        dest='lan_config',
                        action='store_true',
                        help="Get and show LAN config")

    parser.add_argument('-W', '--wifi-usage',
                        dest='wifi_usage',
                        action='store_true',
                        help="Get and show wifi usage")   

    parser.add_argument('-I', '--lan-interfaces',
                        dest='lan_interfaces',
                        action='store_true',
                        help="Get and show lan interfaces")                                                 

    parser.add_argument('-X', '--interfaces-hosts',
                        dest='interfaces_hosts',
                        action='store_true',
                        help="Get and show interfaces hosts") 
                        

    args = parser.parse_args()

    if args.app_id is not None:
      app_id=args.app_id

    if args.app_name is not None:
      app_name=args.app_name

    if args.device_name is not None:
      device_name=args.device_name


    # WARNING: Needs to be removed - Kept here for test purposes only!
    ENDPOINT="http://"+args.Endpoint+"/api/v8/"

    freebox_api.setHostname(args.Endpoint)


    auth = freebox_api.login_authGet(args.register)

    if args.register:
        freebox_api.login_registerApplication(auth, app_id, app_name, VERSION, device_name)
    elif args.status:
        register_status(auth)
    else:     
        # get_and_print_metrics(auth, args.status_switch, args.status_ports, args.status_sys, args.disk_usage, args.lan_config, args.wifi_usage, args.lan_interfaces, args.interfaces_hosts)
        do_export(auth, args.status_switch, args.status_ports, args.status_sys, args.disk_usage, args.lan_config, args.wifi_usage, args.lan_interfaces, args.interfaces_hosts)

