#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621


import hmac
import json
import os
import requests
import sys

if sys.version_info >= (3, 0):
    import configparser as configp
else:
    import ConfigParser as configp

from hashlib import sha1


# global ENDPOINT
g_freebox_hostname = "toto"

# global g_freebox_session_token
g_freebox_session_token = ""


import logging
FORMAT = "[%(filename)s +%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)



# def init():
	# log.info("init")


def __apiUrl(pUrl):
	retval = __endpoint()
	retval += pUrl

	return retval


def	__endpoint():
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
		print("%s: Failed request: %s\n" % __name__, r.text)


def challengeGet(freebox_app_id):
	# api_url = '%s/login/authorize/%s' % (ENDPOINT, freebox_app_id)
	# api_url = __apiUrl('login/authorize/' + freebox_app_id)

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


def login_authGet(pRegister):

	lEndpoint = __endpoint()

	script_dir = os.path.dirname(os.path.realpath(__file__))
	cfg_file = os.path.join(script_dir, ".credentials")
	ret_args={}
	f = configp.RawConfigParser()
	f.read(cfg_file)

	try:
		_ = f.has_section(lEndpoint)

		ret_args.update(track_id= f.get(lEndpoint, "track_id"))
		ret_args.update(app_token= f.get(lEndpoint, "app_token"))

		if f.has_option(lEndpoint, "app_id"):
				ret_args.update(app_id= f.get(lEndpoint, "app_id")) 
		else:
				ret_args.update(app_id= app_id)

		if f.has_option(lEndpoint, "app_name"):
				ret_args.update(app_name= f.get(lEndpoint, "app_name")) 
		else:
				ret_args.update(app_name= app_name) 

		if f.has_option(lEndpoint, "device_name"):
				ret_args.update(device_name= f.get(lEndpoint, "device_name")) 
		else:
				ret_args.update(device_name= device_name)

	except configp.NoSectionError:
		if pRegister:
				return None
		else:
				exit()

	return ret_args


def login_registerApplication(creds, pAppId, pAppName, pAppVersion, pDeviceName):
    #global app_id,app_name,device_name
    if creds is not None:
        if 'track_id' in creds and 'app_token' in creds:
            print("Already registered, exiting")
            return

    print("Doing registration")
    headers = {'Content-type': 'application/json'}
    app_info = {
        'app_id': pAppId,
        'app_name': pAppName,
        'app_version': pAppVersion,
        'device_name': pDeviceName
    }
    json_payload = json.dumps(app_info)

    lApiUrl = __apiUrl( 'login/authorize/')
    r = requests.post(lApiUrl, headers=headers, data=json_payload)
    register_infos = None

    if r.status_code == 200:
        register_infos = r.json()
    else:
        print('Failed registration: %s\n' % r.text)

    login_authSet(pAppId, pAppName, pDeviceName, register_infos['result'])
    print("Don't forget to accept auth on the Freebox panel !")


def login_authSet(pAppId, pAppName, pDeviceName, auth_infos):

    lEndpoint= __endpoint()

    script_dir = os.path.dirname(os.path.realpath(__file__))
    cfg_file = os.path.join(script_dir, ".credentials")
    f = configp.RawConfigParser()

    f.add_section(lEndpoint)
    f.set(lEndpoint,	"track_id",		auth_infos['track_id'])
    f.set(lEndpoint,	"app_token",	auth_infos["app_token"])
    f.set(lEndpoint,	"app_id",		pAppId)
    f.set(lEndpoint,	"app_name",		pAppName)
    f.set(lEndpoint,	"device_name",	pDeviceName)

#    with open(cfg_file, "ab") as authFile:
    with open(cfg_file, "a") as authFile:
        f.write(authFile)


def session_open(freebox_app_id, pAppToken, pTrackId):

	global g_freebox_session_token


	# Fetch challenge
	resp = challengeGet(pTrackId)
	challenge = resp['result']['challenge']

	# Generate session password
	if sys.version_info >= (3, 0):
		h = hmac.new(bytearray(pAppToken, 'ASCII'), bytearray(challenge, 'ASCII'), sha1)
	else:
		h = hmac.new(pAppToken, challenge, sha1)
	password = h.hexdigest()


	lApiUrl = 'login/session/'

	app_info = {
		'app_id': freebox_app_id,
		'password': password
	}
	json_payload = json.dumps(app_info)

	retval = __sendRequest_post(lApiUrl, pData=json_payload)

	g_freebox_session_token = retval['result']['session_token']
	return retval


def setHostname(pHostname):
	global g_freebox_hostname
	g_freebox_hostname = pHostname
