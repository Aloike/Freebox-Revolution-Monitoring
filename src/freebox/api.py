#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621


import hmac
import json
import requests
import sys

from hashlib import sha1

from . import credentials


# global ENDPOINT
g_freebox_hostname = ""

# global g_freebox_session_token
g_freebox_session_token = ""


def init(pFreeboxHostname, pAppId, pAppName, pDeviceName):
import logging
FORMAT = "[%(filename)s +%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

	# Needed to generate the endpoint string
	setHostname(pFreeboxHostname)

	# if credentials.read(__endpoint()) is not True:
	# 	credentials.create(pAppId, pAppName, pDeviceName)

	# assert credentials.read(__endpoint()) == True, "Can't read credentials! Has the application been registered?"
	credentials.read(__endpoint())

# ##############################################################################
# ##############################################################################

def __apiUrl(pUrl):
	retval = __endpoint()
	retval += pUrl

	return retval

# ##############################################################################
# ##############################################################################

def	__endpoint():
	# if g_freebox_hostname == "":
	assert g_freebox_hostname != "", "Hostname must have been defined!"

	retval="http://" + g_freebox_hostname + "/api/v8/"
	return retval


def __sendRequest_get(pApiUrl):

	global g_freebox_session_token

	lRequestUrl = __endpoint()
	lRequestUrl += pApiUrl

	if g_freebox_session_token == "":
		log.warning("No session token has been found!")

	headers = {
		'X-Fbx-App-Auth': g_freebox_session_token
	}

	r = requests.get(lRequestUrl, headers=headers)

	if r.status_code == 200:
		return r.json()
	elif r.status_code == 403:
		# print("%s::%s: Failed request: %s\n" % (__name__, __sendRequest_get.__name__, r.text))
		log.error("%s: Failed request: `%s`: %d: %s\n" % (__sendRequest_get.__name__, lRequestUrl, r.status_code, r.text))
	else:
		# print("%s::%s: Failed request: %s\n" % (__name__, __sendRequest_get.__name__, r.text))
		log.error("%s: Failed request: `%s`: %d: %s\n" % (__sendRequest_get.__name__, lRequestUrl, r.status_code, r.text))


def __sendRequest_post(pApiUrl, pData):
	lRequestUrl = __endpoint()
	lRequestUrl += pApiUrl

	r = requests.post(lRequestUrl, data=pData)

	if r.status_code == 200:
		return r.json()
	else:
		# print("%s: Failed request: %s\n" % __name__, r.text)
		# log.error("Failed request: `%s`" % ( r.text))
		log.error("%s: Failed request: `%s`: %d: %s\n" % (__sendRequest_get.__name__, lRequestUrl, r.status_code, r.text))


def challengeGet(freebox_app_id):

	# r = requests.get(api_url)

	# if r.status_code == 200:
	# 	return r.json()
	# else:
	# 	print("Failed request: %s\n" % r.text)
	return __sendRequest_get('login/authorize/' + freebox_app_id)


def get_connection_stats():
	lApiUrl = 'connection/'

	return __sendRequest_get(lApiUrl)


def get_connection_ftth():
	lApiUrl = 'connection/ftth/'

	return __sendRequest_get(lApiUrl)


def get_connection_xdsl():
	lApiUrl = 'connection/xdsl/'

	return __sendRequest_get(lApiUrl)


def get_lan_config():
	lApiUrl = 'lan/config/'

	return __sendRequest_get(lApiUrl)


def get_lan_interfaces():
	lApiUrl = 'lan/browser/interfaces/'

	return __sendRequest_get(lApiUrl)


# old name: get_interfaces_hosts
def get_lan_interface_hostsList(pInterface):
	lApiUrl	=	'lan/browser/'
	lApiUrl	+=	pInterface

	return __sendRequest_get(lApiUrl)


def get_storage_disk():
	lApiUrl = 'storage/disk/'

	return __sendRequest_get(lApiUrl)


def get_system():
	lApiUrl = 'system/'

	return __sendRequest_get(lApiUrl)


def get_switch_port_stats(pPort):
	# -P => update pour avec POP
	lApiUrl =	'switch/port/'
	lApiUrl	+=	str(pPort)
	lApiUrl	+=	'stats/'

	return __sendRequest_get(lApiUrl)


def get_switch_status():
	lApiUrl = 'switch/status/'

	return __sendRequest_get(lApiUrl)


# old name: get_wifi_statsx
def get_wifi_accessPointsList():
	lApiUrl = 'wifi/ap/'

	return __sendRequest_get(lApiUrl)


# old name:get_wifi_stats
def get_wifi_accessPoint_stations(pAccessPoint):
	# -P => update pour avec POP
	lApiUrl =	'wifi/ap/'
	lApiUrl	+=	str(pAccessPoint) + '/'
	lApiUrl	+=	'stations/'

	return __sendRequest_get(lApiUrl)


def	isRegistered():

	return credentials.exists()

# ##############################################################################
# ##############################################################################

def login_registerApplication(pAppId, pAppName, pAppVersion, pDeviceName):
	#global app_id,app_name,device_name
	if credentials.exists():
		if 	(	credentials.track_id()	is not None
			and	credentials.app_token()	is not None	):
			log.info("Already registered")
			return True

	log.info("Doing registration")


	#
	# Prepare the POST request content
	#
	headers = {'Content-type': 'application/json'}
	app_info = {
		'app_id': pAppId,
		'app_name': pAppName,
		'app_version': pAppVersion,
		'device_name': pDeviceName
	}
	json_payload = json.dumps(app_info)

	#
	# Post the authorization request
	#
	lApiUrl = __apiUrl( 'login/authorize/' )
	r = requests.post(lApiUrl, headers=headers, data=json_payload)
	register_infos = None

	if r.status_code == 200:
		register_infos = r.json()
	else:
		print('Failed registration: %s\n' % r.text)
		return False

	#
	# Store authentication infos
	#
	log.debug("register_infos = %s" % register_infos)
	lJsonRegisterInfos	=	register_infos['result']
	credentials.write(
		__endpoint(),
		pAppId,
		pAppName,
		pDeviceName,
		lJsonRegisterInfos['track_id'],
		lJsonRegisterInfos['app_token']
	)

	print("Don't forget to accept auth on the Freebox panel !")
	return True

# ##############################################################################
# ##############################################################################

def session_open(pAppId):

	global g_freebox_session_token

	lFreeboxAppToken	=	credentials.app_token()
	lFreeboxTrackId	=	credentials.track_id()


	# Fetch challenge
	resp = challengeGet(lFreeboxTrackId)
	challenge = resp['result']['challenge']

	# Generate session password
	if sys.version_info >= (3, 0):
		h = hmac.new(bytearray(lFreeboxAppToken, 'ASCII'), bytearray(challenge, 'ASCII'), sha1)
	else:
		h = hmac.new(lFreeboxAppToken, challenge, sha1)
	password = h.hexdigest()


	lApiUrl = 'login/session/'

	app_info = {
		'app_id': pAppId,
		'password': password
	}
	json_payload = json.dumps(app_info)

	retval = __sendRequest_post(lApiUrl, pData=json_payload)

	g_freebox_session_token = retval['result']['session_token']
	return retval

# ##############################################################################
# ##############################################################################

def setHostname(pHostname):
	global g_freebox_hostname
	g_freebox_hostname = pHostname

# ##############################################################################
# ##############################################################################
