#!/usr/bin/python3
#-*- coding: utf-8 -*-
# coding: utf-8
# pylint: disable=C0103,C0111,W0621

import os
import sys

if sys.version_info >= (3, 0):
    import configparser as configp
else:
    import ConfigParser as configp

# ##############################################################################
# ##############################################################################

##  @brief  This dictionnary contains credentials to login to the Freebox.
g_freebox_credentials	=	{}

# ##############################################################################
# ##############################################################################

def	_credentials_filePath():
	# script_dir = os.path.dirname(os.path.realpath(__file__))
	# cfg_file = os.path.join(script_dir, ".credentials")

	cfg_file = os.path.join(os.getcwd(), ".credentials")

	return cfg_file

# ##############################################################################
# ##############################################################################

def	app_token():
	return	g_freebox_credentials['app_token']

# ##############################################################################
# ##############################################################################
#
##  @brief  Create credentials keys.
#
def create(pAppId, pAppName, pDeviceName):

	# # Create the file parser
	# lCfgFile = configp.RawConfigParser()

	# # Load the credentials configuration
	# lCfgFileName	= _credentials_filePath()
	# lCfgFile.read(lCfgFileName)


	#
	#	Parse the credentials configuration file
	#
	global	g_freebox_credentials
	g_freebox_credentials	=	{}
	try:
		# lEndpoint	= __endpoint()
		# _ = lCfgFile.has_section(lEndpoint)

		# g_freebox_credentials.update(track_id= lCfgFile.get(lEndpoint, "track_id"))
		# g_freebox_credentials.update(app_token= lCfgFile.get(lEndpoint, "app_token"))

		# if lCfgFile.has_option(lEndpoint, "app_id"):
		# 		g_freebox_credentials.update(app_id= lCfgFile.get(lEndpoint, "app_id")) 
		# else:
		g_freebox_credentials.update(app_id= pAppId)

		# if lCfgFile.has_option(lEndpoint, "app_name"):
		# 		g_freebox_credentials.update(app_name= lCfgFile.get(lEndpoint, "app_name")) 
		# else:
		g_freebox_credentials.update(app_name= pAppName) 

		# if lCfgFile.has_option(lEndpoint, "device_name"):
		# 		g_freebox_credentials.update(device_name= lCfgFile.get(lEndpoint, "device_name")) 
		# else:
		g_freebox_credentials.update(device_name= pDeviceName)

	except configp.NoSectionError:
	# 	if pRegister:
	# 			return None
	# 	else:
				exit()

	return g_freebox_credentials

# ##############################################################################
# ##############################################################################

def	exists():
	global	g_freebox_credentials

	if not g_freebox_credentials:
		return False
	else:
		return True

# ##############################################################################
# ##############################################################################
#
##  @brief  Reads the credentials file and returns a Dictionnary containing
##          credentials values.
#
def read(pEndpoint):

	# Create the file parser
	lCfgFile = configp.RawConfigParser()

	# Load the credentials configuration
	lCfgFileName	= _credentials_filePath()
	lCfgFile.read(lCfgFileName)


	#
	#	Parse the credentials configuration file
	#
	global	g_freebox_credentials
	g_freebox_credentials	=	{}
	try:
		# lEndpoint	= __endpoint()
		_ = lCfgFile.has_section(pEndpoint)

		g_freebox_credentials.update(track_id= lCfgFile.get(pEndpoint, "track_id"))
		g_freebox_credentials.update(app_token= lCfgFile.get(pEndpoint, "app_token"))

		# if lCfgFile.has_option(lEndpoint, "app_id"):
		g_freebox_credentials.update(app_id= lCfgFile.get(pEndpoint, "app_id")) 
		# else:
		# 		g_freebox_credentials.update(app_id= pAppId)

		# if lCfgFile.has_option(lEndpoint, "app_name"):
		g_freebox_credentials.update(app_name= lCfgFile.get(pEndpoint, "app_name")) 
		# else:
		# 		g_freebox_credentials.update(app_name= pAppName) 

		# if lCfgFile.has_option(lEndpoint, "device_name"):
		g_freebox_credentials.update(device_name= lCfgFile.get(pEndpoint, "device_name")) 
		# else:
		# 		g_freebox_credentials.update(device_name= pDeviceName)


	except configp.NoSectionError:
	# 	# if pRegister:
	# 	# 		return None
	# 	# else:
	# 			# exit()
	# 	create()
		return False


	# return g_freebox_credentials
	return True

# ##############################################################################
# ##############################################################################

def	track_id():
	return	g_freebox_credentials['track_id']

# ##############################################################################
# ##############################################################################

def	write(pEndpoint, pAppId, pAppName, pDeviceName, pFbxTrackId, pFbxAppToken):#auth_infos):

	lEndpoint= pEndpoint

	lCfgFileName = _credentials_filePath()
	f = configp.RawConfigParser()

	f.add_section(lEndpoint)
	f.set(lEndpoint,	"app_id",		pAppId)
	f.set(lEndpoint,	"app_name",		pAppName)
	f.set(lEndpoint,	"device_name",	pDeviceName)
	f.set(lEndpoint,	"track_id",		pFbxTrackId)
	f.set(lEndpoint,	"app_token",	pFbxAppToken)

	#    with open(lCfgFileName, "ab") as authFile:
	with open(lCfgFileName, "a") as authFile:
		f.write(authFile)

# ##############################################################################
# ##############################################################################
