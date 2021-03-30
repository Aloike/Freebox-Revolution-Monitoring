#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

import argparse
# import distutils
import distutils.util
import os

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

__config_options	=	{
	'app_id'	:	'fr.freebox.exporter.influx',
	'app_name'	:	'FbxExporterInfluxDB',
	'device_name'	:	'srv-timeseries',

	'freebox_hostname'	:	'mafreebox.freebox.fr',

	# If set to True, triggers a registration procedure.
	'application_register'	:	False,
	# If set to True, displays registration status then exits.
	'application_register_status'	:	False,

	'measurement_namePrefix'	:	'freebox',

	'export_all'	:	False,

	'export_application_infos'	:	True,
	'export_connection'	:	False,
	'export_lan_config'	:	False,
	'export_lan_interfaces'	:	False,
	'export_lan_interfaces_hosts'	:	False,
	'export_storage_disk'	:	False,
	'export_switch_ports_stats'	:	False,
	'export_switch_status'	:	False,
	'export_system'	:	False,
	'export_wifi_usage'	:	False

}

# ##############################################################################
# ##############################################################################

def	__configBooleanGet(pConfigKey):
	# https://stackoverflow.com/a/18472142
	lConfigValueStr	=	__configStringGet(pConfigKey)
	return bool(distutils.util.strtobool(lConfigValueStr))

# ##############################################################################
# ##############################################################################

def	__configStringGet(pConfigKey):
	return str(__config_options[pConfigKey])

# ##############################################################################
# ##############################################################################

def init():
	read_env()

# ##############################################################################
# ##############################################################################

def parse_args():

	# log.debug("Reading arguments...")

	# parser = argparse.ArgumentParser()
	parser = argparse.ArgumentParser(add_help=False)

	#helpgroup = parser.add_argument_group()

	#
	#	Declare misc. args
	#
	parser.add_argument(
		"-h",
		"--help",
		action="help",
		help="show this help message and exit"
	)


	#
	#	Declare application configuration args
	#

	parser.add_argument(
		'-d',
		'--device-name',
		default	=	__config_options['device_name'],
		dest	=	'device_name',
		metavar	=	'<device_name>',
		help	=	"Register to the Freebox using <device_name> as the"
					" device's name."
	)

	parser.add_argument(
		'-i',
		'--app-id',
		default	=	__config_options['app_id'],
		dest	=	'app_id',
		metavar	=	'<application_id>',
		help	=	"Register to the Freebox using <application_id> as the"
					" application's ID."
	)

	parser.add_argument(
		'-n',
		'--app-name',
		default	=	__config_options['app_name'],
		dest	=	'app_name',
		metavar	=	'<application_name>',
		help	=	"Register to the Freebox using <application_name> as the"
					" application's name."
	)

	parser.add_argument(
		'-f',
		'--freebox-hostname',
		default	=	__config_options['freebox_hostname'],
		dest	=	'freebox_hostname',
		metavar	=	'<freebox_hostname>',
		help	=	"Connect to the Freebox at address <freebox_hostname>."
	)

	parser.add_argument(
		'-m',
		'--measurement-name-prefix',
		default	=	__config_options['measurement_namePrefix'],
		dest	=	'measurement_namePrefix',
		metavar	=	'<measurement_namePrefix>',
		help	=	"Prefix generated measurements with <measurement_namePrefix>."
	)

	#
	#	Declare args related to registering
	#
	parser.add_argument(
		'-r',
		'--register',
		dest	=	'application_register',
		action	=	'store_true',
		help	=	"Register app with Freebox API"
	)

	parser.add_argument(
		'-s',
		'--register-status',
		dest	=	'application_register_status',
		action	=	'store_true',
		help	=	"Get register status"
	)


	#
	#	Declare export configuration args
	#

	# parser.add_argument('-f', '--format',
	#                     dest='format',
	#         metavar='format',
	#         default='graphite',
	#                     help="Specify output format between graphite and influxdb")

	# parser.add_argument('-e', '--endpoint',
	#                     dest='Endpoint',
	#         metavar='endpoint',
	#         default=config.FREEBOX_HOST,
	#                     help="Specify endpoint name or address")

	parser.add_argument(
		'-A',
		'--export-all',
		default	=	__config_options['export_all'],
		dest	=	'export_all',
		action	=	'store_true',
		help	=	"Export all available measurements."
	)

	parser.add_argument(
		'-a',
		'--export-application-infos',
		default	=	__config_options['export_application_infos'],
		dest	=	'export_application_infos',
		action	=	'store_true',
		help	=	"Show local application infos."
	)

	parser.add_argument(
		'-C',
		'--export-connection',
		default	=	__config_options['export_connection'],
		dest	=	'export_connection',
		action	=	'store_true',
		help	=	"Get and show connection informations (xDSL/FTTH)."
	)

	parser.add_argument(
		'-L',
		'--export-lan-config',
		default	=	__config_options['export_lan_config'],
		dest	=	'export_lan_config',
		action	=	'store_true',
		help	=	"Get and show LAN configuration."
	)

	parser.add_argument(
		'-I',
		'--export-lan-interfaces',
		default	=	__config_options['export_lan_interfaces'],
		dest	=	'export_lan_interfaces',
		action	=	'store_true',
		help	=	"Get and show LAN interfaces."
	)

	parser.add_argument(
		'-X',
		'--export-lan-interfaces-hosts',
		default	=	__config_options['export_lan_interfaces_hosts'],
		dest	=	'export_lan_interfaces_hosts',
		action	=	'store_true',
		help	=	"Get and show LAN interfaces hosts."
	)

	parser.add_argument(
		'-D',
		'--export-storage-disk',
		default	=	__config_options['export_storage_disk'],
		dest	=	'export_storage_disk',
		action	=	'store_true',
		help	=	"Get and show disk usage."
	)

	parser.add_argument(
		'-P',
		'--export-switch-ports-stats',
		default	=	__config_options['export_switch_ports_stats'],
		dest	=	'export_switch_ports_stats',
		action	=	'store_true',
		help	=	"Get and show switch ports statistics."
	)

	parser.add_argument(
		'-S',
		'--export-switch-status',
		default	=	__config_options['export_switch_status'],
		dest	=	'export_switch_status',
		action	=	'store_true',
		help	=	"Get and show switch status"
	)

	parser.add_argument(
		'-H',
		'--export-system',
		default	=	__config_options['export_system'],
		dest	=	'export_system',
		action	=	'store_true',
		help	=	"Get and show system status"
	)

	parser.add_argument(
		'-W',
		'--export-wifi-usage',
		default	=	__config_options['export_wifi_usage'],
		dest	=	'export_wifi_usage',
		action	=	'store_true',
		help	=	"Get and show WiFi usage."
	)


	#
	#	Parse arguments
	#
	lArgs	= parser.parse_args()

	__config_options['app_id']	=	lArgs.app_id
	__config_options['app_name']	=	lArgs.app_name

	__config_options['device_name']	=	lArgs.device_name

	__config_options['freebox_hostname']	=	lArgs.freebox_hostname

	__config_options['application_register']	=	lArgs.application_register
	__config_options['application_register_status']	=	lArgs.application_register_status

	__config_options['measurement_namePrefix']	=	lArgs.measurement_namePrefix

	__config_options['export_all']	=	lArgs.export_all

	__config_options['export_application_infos']	=	lArgs.export_application_infos
	__config_options['export_connection']	=	lArgs.export_connection
	__config_options['export_lan_config']	=	lArgs.export_lan_config
	__config_options['export_lan_interfaces']	=	lArgs.export_lan_interfaces
	__config_options['export_lan_interfaces_hosts']	=	lArgs.export_lan_interfaces_hosts
	__config_options['export_storage_disk']	=	lArgs.export_storage_disk
	__config_options['export_switch_ports_stats']	=	lArgs.export_switch_ports_stats
	__config_options['export_switch_status']	=	lArgs.export_switch_status
	__config_options['export_system']	=	lArgs.export_system
	__config_options['export_wifi_usage']	=	lArgs.export_wifi_usage

# ##############################################################################
# ##############################################################################

def	read_env():


	#
	#	Iterate through configuration variables
	#
	for lKey in __config_options:
		# log.debug("+-- key : " + lKey )

		# Generate the environment variable from the uppercase configuration key
		lEnvVarName	=	str(lKey).upper()
		# log.debug("    +-- lEnvVarName : " + lEnvVarName )

		# Set the conviguration variable value; keep its current value by
		# default.
		__config_options[lKey]	=	os.getenv(
			lEnvVarName,
			__config_options[lKey]
		)

# ##############################################################################
# ##############################################################################

def	app_id():
	return __configStringGet('app_id')

# ##############################################################################
# ##############################################################################

def	app_name():
	return __configStringGet('app_name')

# ##############################################################################
# ##############################################################################

def	device_name():
	return __configStringGet('device_name')

# ##############################################################################
# ##############################################################################

def	application_register():
	return __configBooleanGet('application_register')

# ##############################################################################
# ##############################################################################

def	application_registerStatus():
	return __configBooleanGet('application_register_status')

# ##############################################################################
# ##############################################################################

def	freebox_hostname():
	return __configStringGet('freebox_hostname')

# ##############################################################################
# ##############################################################################

def	measurement_namePrefix():
	return __configStringGet('measurement_namePrefix')

# ##############################################################################
# ##############################################################################

def	export_all():
	return __configBooleanGet('export_all')

# ##############################################################################
# ##############################################################################

def	export_application_infos():
	return __configBooleanGet('export_application_infos')

# ##############################################################################
# ##############################################################################

def	export_connection():
	return __configBooleanGet('export_connection')

# ##############################################################################
# ##############################################################################

def	export_lan_config():
	return __configBooleanGet('export_lan_config')

# ##############################################################################
# ##############################################################################

def	export_lan_interfaces():
	return __configBooleanGet('export_lan_interfaces')

# ##############################################################################
# ##############################################################################

def	export_lan_interfaces_hosts():
	return __configBooleanGet('export_lan_interfaces_hosts')

# ##############################################################################
# ##############################################################################

def	export_storage_disk():
	return __configBooleanGet('export_storage_disk')

# ##############################################################################
# ##############################################################################

def	export_switch_ports_stats():
	return __configBooleanGet('export_switch_ports_stats')

# ##############################################################################
# ##############################################################################

def	export_switch_status():
	return __configBooleanGet('export_switch_status')

# ##############################################################################
# ##############################################################################

def	export_system():
	return __configBooleanGet('export_system')

# ##############################################################################
# ##############################################################################

def	export_wifi_usage():
	return __configBooleanGet('export_wifi_usage')

# ##############################################################################
# ##############################################################################
